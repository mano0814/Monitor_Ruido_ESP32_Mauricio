import tkinter as tk
import math


class ModuloAmbiente:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#1E1E1E")

        self.umbral_moderado = 2500
        self.umbral_ruidoso = 6000
        self.escala_visual_max = 15000

        self.pico_max = 0.0
        self.suma_lecturas = 0.0
        self.conteo_lecturas = 0
        self.midiendo = False
        self.dimensiones = ""

        self.frame_setup = tk.Frame(self.frame, bg="#1E1E1E")
        self.frame_medicion = tk.Frame(self.frame, bg="#1E1E1E")

        lbl_setup = tk.Label(self.frame_setup, text="DIMENSIONES DE LA SALA", font=("Arial", 14, "bold"), bg="#1E1E1E",
                             fg="#FFFFFF")
        lbl_setup.pack(pady=(50, 20))

        frame_inputs = tk.Frame(self.frame_setup, bg="#1E1E1E")
        frame_inputs.pack(pady=10)

        tk.Label(frame_inputs, text="Largo (m):", bg="#1E1E1E", fg="white", font=("Arial", 10)).grid(row=0, column=0,
                                                                                                     padx=5, pady=10)
        self.entry_largo = tk.Entry(frame_inputs, width=10, bg="#333333", fg="white", insertbackground="white",
                                    font=("Arial", 12), justify="center")
        self.entry_largo.grid(row=0, column=1, padx=5, pady=10)
        self.entry_largo.insert(0, "3.0")

        tk.Label(frame_inputs, text="Ancho (m):", bg="#1E1E1E", fg="white", font=("Arial", 10)).grid(row=1, column=0,
                                                                                                     padx=5, pady=10)
        self.entry_ancho = tk.Entry(frame_inputs, width=10, bg="#333333", fg="white", insertbackground="white",
                                    font=("Arial", 12), justify="center")
        self.entry_ancho.grid(row=1, column=1, padx=5, pady=10)
        self.entry_ancho.insert(0, "4.0")

        tk.Label(frame_inputs, text="Alto (m):", bg="#1E1E1E", fg="white", font=("Arial", 10)).grid(row=2, column=0,
                                                                                                    padx=5, pady=10)
        self.entry_alto = tk.Entry(frame_inputs, width=10, bg="#333333", fg="white", insertbackground="white",
                                   font=("Arial", 12), justify="center")
        self.entry_alto.grid(row=2, column=1, padx=5, pady=10)
        self.entry_alto.insert(0, "2.5")

        btn_iniciar = tk.Button(self.frame_setup, text="Continuar a Medición", command=self.iniciar_medicion,
                                bg="#00E676", fg="black", font=("Arial", 10, "bold"), relief="flat", padx=20, pady=8)
        btn_iniciar.pack(pady=30)

        self.frame_setup.pack(fill="both", expand=True)

        self.lbl_titulo = tk.Label(self.frame_medicion, text="MONITOR DE RUIDO AMBIENTAL", font=("Arial", 14, "bold"),
                                   bg="#1E1E1E", fg="#FFFFFF")
        self.lbl_titulo.pack(pady=(20, 5))

        self.lbl_subtitulo = tk.Label(self.frame_medicion,
                                      text="Evalúa el silencio de la sala antes de iniciar la grabación",
                                      font=("Arial", 10), bg="#1E1E1E", fg="#AAAAAA")
        self.lbl_subtitulo.pack(pady=(0, 10))

        self.frame_estado = tk.Frame(self.frame_medicion, bg="#252525", padx=20, pady=15)
        self.frame_estado.pack(fill="x", padx=60, pady=10)

        self.lbl_estado = tk.Label(self.frame_estado, text="ESPERANDO LECTURA...", font=("Arial", 16, "bold"),
                                   bg="#252525", fg="#888888")
        self.lbl_estado.pack()

        self.lbl_detalle = tk.Label(self.frame_estado, text="Mantén la sala en silencio para medir el ruido base",
                                    font=("Arial", 10), bg="#252525", fg="#CCCCCC")
        self.lbl_detalle.pack(pady=(5, 0))

        self.ancho_barra = 600
        self.alto_barra = 32
        self.canvas_barra = tk.Canvas(self.frame_medicion, width=self.ancho_barra, height=self.alto_barra, bg="#121212",
                                      highlightthickness=1, highlightbackground="#333333")
        self.canvas_barra.pack(pady=20)
        self.rect_nivel = self.canvas_barra.create_rectangle(0, 0, 0, self.alto_barra, fill="#00E676", outline="")

        self.frame_metricas = tk.Frame(self.frame_medicion, bg="#1E1E1E")
        self.frame_metricas.pack(pady=10)

        self.lbl_rms = self.crear_tarjeta_metrica(self.frame_metricas, "NIVEL ACTUAL", "0", 0)
        self.lbl_dbfs = self.crear_tarjeta_metrica(self.frame_metricas, "NIVEL RELATIVO", "-90.3 dBFS", 1)
        self.lbl_promedio = self.crear_tarjeta_metrica(self.frame_metricas, "PROMEDIO SALA", "0", 2)
        self.lbl_pico = self.crear_tarjeta_metrica(self.frame_metricas, "PICO MÁXIMO", "0", 3)

        self.frame_botones_med = tk.Frame(self.frame_medicion, bg="#1E1E1E")
        self.frame_botones_med.pack(pady=15)

        self.btn_reiniciar = tk.Button(self.frame_botones_med, text="Reiniciar Medición",
                                       command=self.reiniciar_estadisticas, font=("Arial", 10, "bold"), bg="#333333",
                                       fg="#FFFFFF", relief="flat", padx=15, pady=8)
        self.btn_reiniciar.pack(side="left", padx=10)

        self.btn_volver = tk.Button(self.frame_botones_med, text="Cambiar Dimensiones", command=self.volver_setup,
                                    font=("Arial", 10, "bold"), bg="#333333", fg="#FFFFFF", relief="flat", padx=15,
                                    pady=8)
        self.btn_volver.pack(side="left", padx=10)

    def iniciar_medicion(self):
        l = self.entry_largo.get()
        a = self.entry_ancho.get()
        h = self.entry_alto.get()
        self.dimensiones = f"{l}x{a}x{h}m"
        self.frame_setup.pack_forget()
        self.frame_medicion.pack(fill="both", expand=True)
        self.midiendo = True

    def volver_setup(self):
        self.midiendo = False
        self.reiniciar_estadisticas()
        self.frame_medicion.pack_forget()
        self.frame_setup.pack(fill="both", expand=True)

    def crear_tarjeta_metrica(self, parent, titulo, valor_inicial, columna):
        tarjeta = tk.Frame(parent, bg="#252525", width=140, height=70)
        tarjeta.grid(row=0, column=columna, padx=8)
        tarjeta.pack_propagate(False)

        lbl_t = tk.Label(tarjeta, text=titulo, font=("Arial", 8, "bold"), bg="#252525", fg="#AAAAAA")
        lbl_t.pack(pady=(10, 2))

        lbl_v = tk.Label(tarjeta, text=valor_inicial, font=("Arial", 13, "bold"), bg="#252525", fg="#FFFFFF")
        lbl_v.pack()
        return lbl_v

    def actualizar_lectura(self, valor):
        if not self.midiendo:
            return

        if valor > self.pico_max:
            self.pico_max = valor
        self.suma_lecturas += valor
        self.conteo_lecturas += 1
        promedio = self.suma_lecturas / self.conteo_lecturas

        dbfs = 20 * math.log10(max(valor, 1) / 32768.0)
        valor_visual = min(max(valor, 0), self.escala_visual_max)
        ancho_actual = (valor_visual / self.escala_visual_max) * self.ancho_barra

        if valor >= self.umbral_ruidoso:
            color = "#FF1744"
            estado_texto = "AMBIENTE RUIDOSO"
            detalle_texto = "No recomendado grabar: exceso de ruido de fondo"
        elif valor >= self.umbral_moderado:
            color = "#FFEA00"
            estado_texto = "RUIDO MODERADO"
            detalle_texto = "Precaución: ruido ambiental perceptible en el micrófono"
        else:
            color = "#00E676"
            estado_texto = "ÓPTIMO PARA GRABAR"
            detalle_texto = "Piso de ruido bajo: sala silenciosa"

        self.canvas_barra.coords(self.rect_nivel, 0, 0, ancho_actual, self.alto_barra)
        self.canvas_barra.itemconfig(self.rect_nivel, fill=color)

        self.lbl_estado.config(text=estado_texto, fg=color)
        self.lbl_detalle.config(text=detalle_texto)
        self.lbl_rms.config(text=f"{int(valor)}")
        self.lbl_dbfs.config(text=f"{dbfs:.1f} dBFS")
        self.lbl_promedio.config(text=f"{int(promedio)}")
        self.lbl_pico.config(text=f"{int(self.pico_max)}")

    def reiniciar_estadisticas(self):
        self.pico_max = 0.0
        self.suma_lecturas = 0.0
        self.conteo_lecturas = 0
        self.canvas_barra.coords(self.rect_nivel, 0, 0, 0, self.alto_barra)
        self.lbl_estado.config(text="ESPERANDO LECTURA...", fg="#888888")
        self.lbl_detalle.config(text="Mantén la sala en silencio para medir el ruido base")
        self.lbl_rms.config(text="0")
        self.lbl_dbfs.config(text="-90.3 dBFS")
        self.lbl_promedio.config(text="0")
        self.lbl_pico.config(text="0")

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)

    def ocultar(self):
        self.frame.pack_forget()