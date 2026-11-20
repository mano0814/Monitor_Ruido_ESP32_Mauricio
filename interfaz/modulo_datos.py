import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
from datetime import datetime


class ModuloDatos:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#121212")

        lbl_titulo = tk.Label(self.frame, text="HISTORIAL DE RUIDO AMBIENTAL", font=("Arial", 14, "bold"), bg="#121212",
                              fg="#FFFFFF")
        lbl_titulo.pack(pady=(20, 10))

        frame_botones = tk.Frame(self.frame, bg="#121212")
        frame_botones.pack(fill="x", padx=20, pady=5)

        btn_exportar = tk.Button(frame_botones, text="Exportar CSV", command=self.exportar_csv, bg="#333333",
                                 fg="white", relief="flat", padx=10, pady=5)
        btn_exportar.pack(side="left", padx=5)

        btn_importar = tk.Button(frame_botones, text="Importar CSV", command=self.importar_csv, bg="#333333",
                                 fg="white", relief="flat", padx=10, pady=5)
        btn_importar.pack(side="left", padx=5)

        btn_limpiar = tk.Button(frame_botones, text="Limpiar Tabla", command=self.limpiar_tabla, bg="#552222",
                                fg="white", relief="flat", padx=10, pady=5)
        btn_limpiar.pack(side="right", padx=5)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#252525", foreground="white", fieldbackground="#252525", borderwidth=0)
        style.configure("Treeview.Heading", background="#333333", foreground="white", font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", "#444444")])

        self.tree = ttk.Treeview(self.frame, columns=("hora", "sala", "rms", "dbfs", "estado"), show="headings",
                                 height=12)
        self.tree.heading("hora", text="Hora")
        self.tree.heading("sala", text="Sala (L x A x H)")
        self.tree.heading("rms", text="Valor RMS")
        self.tree.heading("dbfs", text="dBFS")
        self.tree.heading("estado", text="Estado")

        self.tree.column("hora", width=80, anchor="center")
        self.tree.column("sala", width=120, anchor="center")
        self.tree.column("rms", width=80, anchor="center")
        self.tree.column("dbfs", width=80, anchor="center")
        self.tree.column("estado", width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=15)

    def registrar_dato(self, sala, rms, dbfs, estado):
        hora = datetime.now().strftime("%H:%M:%S")
        self.tree.insert("", "end", values=(hora, sala, int(rms), f"{dbfs:.1f}", estado))
        self.tree.yview_moveto(1)

    def exportar_csv(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])
        if ruta:
            with open(ruta, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Hora", "Sala", "RMS", "dBFS", "Estado"])
                for fila in self.tree.get_children():
                    writer.writerow(self.tree.item(fila)["values"])

    def importar_csv(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if ruta:
            self.limpiar_tabla()
            with open(ruta, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if row:
                        self.tree.insert("", "end", values=row)

    def limpiar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)

    def ocultar(self):
        self.frame.pack_forget()