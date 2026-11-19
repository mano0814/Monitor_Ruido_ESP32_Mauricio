import tkinter as tk
from modulo_gain import ModuloGain
from cliente_mqtt import ControladorMQTT


class BotonRedondeado(tk.Canvas):
    def __init__(self, parent, text, command, radius=15, width=160, height=40, bg_color="#333333", fg_color="#FFFFFF",
                 hover_color="#555555"):
        super().__init__(parent, width=width, height=height, bg="#1E1E1E", highlightthickness=0)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color

        self.id_rect1 = self.create_rectangle(radius, 0, width - radius, height, fill=bg_color, outline="")
        self.id_rect2 = self.create_rectangle(0, radius, width, height - radius, fill=bg_color, outline="")
        self.id_oval1 = self.create_oval(0, 0, radius * 2, radius * 2, fill=bg_color, outline="")
        self.id_oval2 = self.create_oval(width - radius * 2, 0, width, radius * 2, fill=bg_color, outline="")
        self.id_oval3 = self.create_oval(0, height - radius * 2, radius * 2, height, fill=bg_color, outline="")
        self.id_oval4 = self.create_oval(width - radius * 2, height - radius * 2, width, height, fill=bg_color,
                                         outline="")

        self.id_text = self.create_text(width / 2, height / 2, text=text, fill=fg_color, font=("Arial", 10, "bold"))

        for item in (self.id_rect1, self.id_rect2, self.id_oval1, self.id_oval2, self.id_oval3, self.id_oval4,
                     self.id_text):
            self.tag_bind(item, "<Button-1>", lambda e: self.command())
            self.tag_bind(item, "<Enter>", self.al_entrar)
            self.tag_bind(item, "<Leave>", self.al_salir)

    def al_entrar(self, event):
        for item in (self.id_rect1, self.id_rect2, self.id_oval1, self.id_oval2, self.id_oval3, self.id_oval4):
            self.itemconfig(item, fill=self.hover_color)

    def al_salir(self, event):
        for item in (self.id_rect1, self.id_rect2, self.id_oval1, self.id_oval2, self.id_oval3, self.id_oval4):
            self.itemconfig(item, fill=self.bg_color)


class MonitorAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Audio Profesional - Gain Staging")
        self.root.geometry("800x500")
        self.root.configure(bg="#121212")

        self.frame_menu = tk.Frame(self.root, bg="#1E1E1E", height=60)
        self.frame_menu.pack(side="top", fill="x")
        self.frame_menu.pack_propagate(False)

        self.contenedor_modulos = tk.Frame(self.root, bg="#121212")
        self.contenedor_modulos.pack(side="top", fill="both", expand=True, padx=20, pady=20)

        self.modulo_gain = ModuloGain(self.contenedor_modulos)
        self.modulo_activo = None

        self.crear_botones_menu()

        self.mqtt = ControladorMQTT("estudio/monitor/gain", self.procesar_dato_recibido)
        self.mqtt.iniciar()

    def procesar_dato_recibido(self, valor):
        if self.modulo_activo == self.modulo_gain:
            valor_limitado = min(max(valor, 0), 32768)
            angulo = 180 - (valor_limitado / 32768) * 180

            if valor >= 25000:
                estado = "rojo"
            elif valor >= 15000:
                estado = "amarillo"
            else:
                estado = "verde"

            self.root.after(0, self.modulo_gain.actualizar_estado, estado, angulo)

    def crear_botones_menu(self):
        self.btn_ambiente = BotonRedondeado(self.frame_menu, text="1. Ruido Ambiental",
                                            command=lambda: self.cambiar_modulo("ambiente"))
        self.btn_ambiente.pack(side="left", padx=15, pady=10)

        self.btn_gain = BotonRedondeado(self.frame_menu, text="2. Gain Staging",
                                        command=lambda: self.cambiar_modulo("gain"))
        self.btn_gain.pack(side="left", padx=15, pady=10)

        self.btn_datos = BotonRedondeado(self.frame_menu, text="3. Datos (CSV)",
                                         command=lambda: self.cambiar_modulo("datos"))
        self.btn_datos.pack(side="left", padx=15, pady=10)

    def cambiar_modulo(self, nombre_modulo):
        if self.modulo_activo:
            self.modulo_activo.ocultar()

        if nombre_modulo == "gain":
            self.modulo_gain.mostrar()
            self.modulo_activo = self.modulo_gain
        else:
            print(f"Módulo '{nombre_modulo}' no implementado aún.")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = MonitorAudioApp(ventana)
    ventana.mainloop()