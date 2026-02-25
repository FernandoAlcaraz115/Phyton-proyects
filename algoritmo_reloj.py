#Fernando Isai Alcaraz Méndez 22121344
#Luis Antonio Arguello Escutia 23121127

import tkinter as tk
from tkinter import messagebox


class Pagina:
    def __init__(self, id_pagina, referenciada=False):
        self.id = id_pagina
        self.referenciada = referenciada


class AlgoritmoReloj:
    def __init__(self, num_marcos):
        self.marcos = [None] * num_marcos
        self.puntero = 0
        self.fallos_pagina = 0
        self.aciertos = 0
        self.historial = []

    def buscar_pagina(self, id_pagina):
        for i, pagina in enumerate(self.marcos):
            if pagina and pagina.id == id_pagina:
                pagina.referenciada = True
                return True, i
        return False, None

    def encontrar_victima(self):
        while True:
            pagina = self.marcos[self.puntero]

            # Si el marco está vacío, se usa directamente
            if pagina is None:
                victima = self.puntero
                return victima, "marco_vacio", None

            # Si la página no está referenciada, se reemplaza
            if not pagina.referenciada:
                victima = self.puntero
                return victima, "no_referenciada", pagina.id
            else:
                # Le damos una segunda oportunidad y limpiamos el bit
                pagina.referenciada = False
                self.puntero = (self.puntero + 1) % len(self.marcos)

    def referenciar_pagina(self, id_pagina):
        resultado = {
            'pagina': id_pagina,
            'acierto': False,
            'reemplazo': None,
            'victima': None,
            'marco_reemplazo': None,
            'explicacion': ""
        }

        # Buscar si la página ya está en memoria
        encontrado, indice = self.buscar_pagina(id_pagina)

        if encontrado:
            self.aciertos += 1
            resultado['acierto'] = True
            resultado['explicacion'] = f"Página {id_pagina} ya estaba en marco {indice} (ACIERTO)"
            resultado['marco_reemplazo'] = indice
        else:
            self.fallos_pagina += 1
            indice_victima, motivo, pagina_victima = self.encontrar_victima()

            # Nueva página: cuando se carga, ya ha sido referenciada
            nueva_pagina = Pagina(id_pagina, referenciada=True)
            pagina_anterior = self.marcos[indice_victima]

            # Realizar reemplazo
            self.marcos[indice_victima] = nueva_pagina

            # Avanzar puntero solo una vez después del reemplazo
            self.puntero = (indice_victima + 1) % len(self.marcos)

            resultado['reemplazo'] = nueva_pagina.id
            resultado['victima'] = pagina_anterior.id if pagina_anterior else None
            resultado['marco_reemplazo'] = indice_victima

            if motivo == "marco_vacio":
                resultado['explicacion'] = f"Cargando página {id_pagina} en marco vacío {indice_victima}"
            else:
                resultado['explicacion'] = f"Reemplazando página {pagina_victima} por {id_pagina} en marco {indice_victima}"

        self.historial.append(resultado)
        return resultado


class SimuladorRelojGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🕒 Simulador del Algoritmo Reloj - Sistemas Operativos")

        self.config_frame = tk.Frame(root)
        self.config_frame.pack(pady=10)

        tk.Label(self.config_frame, text="Número de marcos:").grid(row=0, column=0)
        self.num_marcos_entry = tk.Entry(self.config_frame, width=5)
        self.num_marcos_entry.grid(row=0, column=1)
        self.num_marcos_entry.insert(0, "3")

        tk.Label(self.config_frame, text="Secuencia (ej: 7,0,1,2,0,3,0,4):").grid(row=0, column=2, padx=5)
        self.secuencia_entry = tk.Entry(self.config_frame, width=40)
        self.secuencia_entry.grid(row=0, column=3)
        self.secuencia_entry.insert(0, "7,0,1,2,0,3,0,4,2,3,0,3")

        self.iniciar_btn = tk.Button(self.config_frame, text="Inicializar Simulación", command=self.inicializar_simulacion)
        self.iniciar_btn.grid(row=0, column=4, padx=5)

        self.marcos_frame = tk.Frame(root)
        self.marcos_frame.pack(pady=10)

        self.info_text = tk.Text(root, height=10, width=80)
        self.info_text.pack(pady=5)

        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=5)

        self.anterior_btn = tk.Button(self.btn_frame, text="⬅ Paso Anterior", command=self.paso_anterior)
        self.anterior_btn.grid(row=0, column=0, padx=5)

        self.siguiente_btn = tk.Button(self.btn_frame, text="Paso Siguiente ➡", command=self.paso_siguiente)
        self.siguiente_btn.grid(row=0, column=1, padx=5)

        self.reiniciar_btn = tk.Button(self.btn_frame, text="🔁 Reiniciar", command=self.reiniciar_simulacion)
        self.reiniciar_btn.grid(row=0, column=2, padx=5)

        self.ejecutar_todo_btn = tk.Button(self.btn_frame, text="⚡ Ejecutar Todo", command=self.ejecutar_todo)
        self.ejecutar_todo_btn.grid(row=0, column=3, padx=5)

        self.stats_label = tk.Label(root, text="")
        self.stats_label.pack(pady=5)

        self.algoritmo = None
        self.secuencia = []
        self.paso_actual = 0

    def inicializar_simulacion(self):
        try:
            num_marcos = int(self.num_marcos_entry.get())
            secuencia_str = self.secuencia_entry.get()
            self.secuencia = [int(x.strip()) for x in secuencia_str.split(',')]
        except ValueError:
            messagebox.showerror("Error", "Verifica los datos ingresados.")
            return

        self.algoritmo = AlgoritmoReloj(num_marcos)
        self.paso_actual = 0
        self.algoritmo.fallos_pagina = 0
        self.algoritmo.aciertos = 0
        self.algoritmo.historial.clear()

        self.crear_marcos_visuales(num_marcos)
        self.actualizar_interfaz()
        messagebox.showinfo("Listo", "Simulación inicializada correctamente.")

    def crear_marcos_visuales(self, num_marcos):
        for widget in self.marcos_frame.winfo_children():
            widget.destroy()
        self.marco_labels = []
        for i in range(num_marcos):
            lbl = tk.Label(self.marcos_frame, text=f"Marco {i}\n[Vacío]", width=15, height=4, relief="solid", bg="lightgray")
            lbl.grid(row=0, column=i, padx=5)
            self.marco_labels.append(lbl)

    def actualizar_interfaz(self):
        for i, pagina in enumerate(self.algoritmo.marcos):
            lbl = self.marco_labels[i]
            if pagina:
                color = "lightgreen" if pagina.referenciada else "salmon"
                lbl.config(text=f"Marco {i}\nPágina: {pagina.id}\nReferenciada: {'Sí' if pagina.referenciada else 'No'}", bg=color)
            else:
                lbl.config(text=f"Marco {i}\n[Vacío]", bg="lightgray")

        puntero = self.algoritmo.puntero
        self.marco_labels[puntero].config(text=self.marco_labels[puntero]["text"] + "\n⬅ PUNTERO", bg="orange")

        self.stats_label.config(
            text=f"Referencias realizadas: {self.paso_actual} / {len(self.secuencia)} | ✅ Aciertos: {self.algoritmo.aciertos} | ❌ Fallos: {self.algoritmo.fallos_pagina}"
        )

    def paso_siguiente(self):
        if self.paso_actual >= len(self.secuencia):
            messagebox.showinfo("Fin", "Se completaron todas las referencias.")
            return

        id_pagina = self.secuencia[self.paso_actual]
        resultado = self.algoritmo.referenciar_pagina(id_pagina)
        self.paso_actual += 1

        self.actualizar_interfaz()
        self.info_text.insert(tk.END, f"Paso {self.paso_actual}: Referencia a página {id_pagina}\n{resultado['explicacion']}\n\n")
        self.info_text.see(tk.END)

    def paso_anterior(self):
        if self.paso_actual == 0:
            return
        self.paso_actual -= 1
        self.algoritmo = AlgoritmoReloj(len(self.marco_labels))
        for i in range(self.paso_actual):
            self.algoritmo.referenciar_pagina(self.secuencia[i])
        self.actualizar_interfaz()

    def ejecutar_todo(self):
        while self.paso_actual < len(self.secuencia):
            self.paso_siguiente()

    def reiniciar_simulacion(self):
        if self.algoritmo:
            self.algoritmo.fallos_pagina = 0
            self.algoritmo.aciertos = 0
            self.algoritmo.historial.clear()
        self.info_text.delete(1.0, tk.END)
        self.paso_actual = 0
        self.actualizar_interfaz()


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorRelojGUI(root)
    root.mainloop()
