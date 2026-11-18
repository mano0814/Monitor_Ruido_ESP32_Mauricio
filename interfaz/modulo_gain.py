import tkinter as tk
import math


class ModuloGain:
    def __init__(self, parent_frame):
        self.frame = tk.Frame(parent_frame, bg="#121212")

        tk.Label(self.frame, text="MEDIDOR DE GANANCIA (VU METER)",
                 font=("Arial", 14, "bold"), fg="#FFFFFF", bg="#121212").pack(pady=20)

        self.canvas_medidor = tk.Canvas(self.frame, width=300, height=160, bg="#121212", highlightthickness=0)
        self.canvas_medidor.pack(pady=10)

        self.canvas_medidor.create_arc(20, 20, 280, 280, start=140, extent=40, outline="#FF0000", width=15, style="arc")
        self.canvas_medidor.create_arc(20, 20, 280, 280, start=105, extent=35, outline="#FFFF00", width=15, style="arc")
        self.canvas_medidor.create_arc(20, 20, 280, 280, start=75, extent=30, outline="#00FF00", width=15, style="arc")
        self.canvas_medidor.create_arc(20, 20, 280, 280, start=40, extent=35, outline="#FFFF00", width=15, style="arc")
        self.canvas_medidor.create_arc(20, 20, 280, 280, start=0, extent=40, outline="#FF0000", width=15, style="arc")

        self.aguja = self.canvas_medidor.create_line(150, 150, 150, 40, fill="#FFFFFF", width=3, arrow=tk.LAST)
        self.canvas_medidor.create_oval(140, 140, 160, 160, fill="#333333", outline="#555555")

        self.frame_luces = tk.Frame(self.frame, bg="#1E1E1E", bd=2, relief="sunken", padx=20, pady=10)
        self.frame_luces.pack(pady=10)

        self.luz_roja = tk.Canvas(self.frame_luces, width=40, height=40, bg="#1E1E1E", highlightthickness=0)
        self.luz_roja.pack(side="left", padx=15)
        self.id_roja = self.luz_roja.create_oval(5, 5, 35, 35, fill="#440000", outline="#220000")

        self.luz_amarilla = tk.Canvas(self.frame_luces, width=40, height=40, bg="#1E1E1E", highlightthickness=0)
        self.luz_amarilla.pack(side="left", padx=15)
        self.id_amarilla = self.luz_amarilla.create_oval(5, 5, 35, 35, fill="#444400", outline="#222200")

        self.luz_verde = tk.Canvas(self.frame_luces, width=40, height=40, bg="#1E1E1E", highlightthickness=0)
        self.luz_verde.pack(side="left", padx=15)
        self.id_verde = self.luz_verde.create_oval(5, 5, 35, 35, fill="#004400", outline="#002200")

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)

    def ocultar(self):
        self.frame.pack_forget()

    def actualizar_estado(self, estado, angulo):
        rad = math.radians(angulo)
        x2 = 150 + 110 * math.cos(rad)
        y2 = 150 - 110 * math.sin(rad)
        self.canvas_medidor.coords(self.aguja, 150, 150, x2, y2)

        self.luz_roja.itemconfig(self.id_roja, fill="#440000")
        self.luz_amarilla.itemconfig(self.id_amarilla, fill="#444400")
        self.luz_verde.itemconfig(self.id_verde, fill="#004400")

        if estado == "rojo":
            self.luz_roja.itemconfig(self.id_roja, fill="#FF0000")
        elif estado == "amarillo":
            self.luz_amarilla.itemconfig(self.id_amarilla, fill="#FFFF00")
        elif estado == "verde":
            self.luz_verde.itemconfig(self.id_verde, fill="#00FF00")