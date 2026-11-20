import tkinter as tk
import math


class ModuloGain:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#121212")

        self.lbl_titulo = tk.Label(self.frame, text="MEDIDOR DE GANANCIA (VU METER)", font=("Arial", 14, "bold"),
                                   bg="#121212", fg="white")
        self.lbl_titulo.pack(pady=(30, 20))

        self.canvas = tk.Canvas(self.frame, width=400, height=200, bg="#121212", highlightthickness=0)
        self.canvas.pack()

        self.canvas.create_arc(50, 50, 350, 350, start=0, extent=60, outline="#FF1744", width=25, style="arc")
        self.canvas.create_arc(50, 50, 350, 350, start=60, extent=60, outline="#FFEA00", width=25, style="arc")
        self.canvas.create_arc(50, 50, 350, 350, start=120, extent=60, outline="#00E676", width=25, style="arc")

        self.centro_x = 200
        self.centro_y = 200
        self.largo_aguja = 130

        self.aguja = self.canvas.create_line(self.centro_x, self.centro_y, self.centro_x - self.largo_aguja,
                                             self.centro_y, fill="white", width=3, arrow=tk.LAST)
        self.base_aguja = self.canvas.create_oval(self.centro_x - 12, self.centro_y - 12, self.centro_x + 12,
                                                  self.centro_y + 12, fill="#555555", outline="#333333")

        self.frame_semaforo = tk.Frame(self.frame, bg="#121212")
        self.frame_semaforo.pack(pady=10)

        self.canvas_sem = tk.Canvas(self.frame_semaforo, width=200, height=60, bg="#121212", highlightthickness=1,
                                    highlightbackground="#333333")
        self.canvas_sem.pack()

        self.luz_verde = self.canvas_sem.create_oval(30, 15, 60, 45, fill="#003300", outline="")
        self.luz_amarilla = self.canvas_sem.create_oval(85, 15, 115, 45, fill="#333300", outline="")
        self.luz_roja = self.canvas_sem.create_oval(140, 15, 170, 45, fill="#330000", outline="")

    def actualizar_estado(self, estado, angulo):
        rad = math.radians(angulo)
        x = self.centro_x + self.largo_aguja * math.cos(rad)
        y = self.centro_y - self.largo_aguja * math.sin(rad)

        self.canvas.coords(self.aguja, self.centro_x, self.centro_y, x, y)

        self.canvas_sem.itemconfig(self.luz_verde, fill="#00E676" if estado == "verde" else "#003300")
        self.canvas_sem.itemconfig(self.luz_amarilla, fill="#FFEA00" if estado == "amarillo" else "#333300")
        self.canvas_sem.itemconfig(self.luz_roja, fill="#FF1744" if estado == "rojo" else "#330000")

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)

    def ocultar(self):
        self.frame.pack_forget()