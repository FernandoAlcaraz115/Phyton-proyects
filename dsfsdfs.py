import tkinter as tk
from tkinter import messagebox

class page:
    def __init__(self, num):
        self.num = num
        self.bit = True

pageStreamRaw = "37565432435986567484576786"
pageStream = []
for i in pageStreamRaw:
    pageStream.append(int(i))

reloj = [page(0), page(0), page(0), page(0), page(0), page(0)]
counter = 0
pos = 0  # puntero

#####################################################
root = tk.Tk()
root.title("Algoritmo del Reloj (versión simple)")
root.geometry("720x400")

# etiquetas del reloj
labels = []
for i in range(len(reloj)):
    lbl = tk.Label(root, text=f"{reloj[i].num} | bit: {int(reloj[i].bit)}",
                   font=("Arial", 12), width=10, height=2, relief="solid")
    lbl.grid(row=0, column=i, padx=5, pady=10)
    labels.append(lbl)

# punteros debajo
pointers = []
for i in range(len(reloj)):
    lbl = tk.Label(root, text=" ", font=("Arial", 14))
    lbl.grid(row=1, column=i)
    pointers.append(lbl)

# etiqueta de mensaje
mensaje = tk.Label(root, text="Presiona 'Siguiente paso' para empezar", font=("Arial", 12), fg="blue")
mensaje.grid(row=2, column=0, columnspan=6, pady=10)



def actualizar_display():
    """Actualiza los cuadros y puntero visualmente"""
    for i in range(len(reloj)):
        color = "#a0f0a0" if reloj[i].bit else "#f0a0a0"
        labels[i].config(text=f"{reloj[i].num} | bit: {int(reloj[i].bit)}", bg=color)
    for i in range(len(pointers)):
        if i == (pos - 1) % len(pointers):
            pointers[i].config(text="⬆️")
        else:
            pointers[i].config(text=" ")

def paso():
    global counter, pos

    if counter >= len(pageStream):
        messagebox.showinfo("Fin", "Ya no hay más páginas en el flujo.")
        boton.config(state="disabled")
        return

    actual = pageStream[counter]
    mensaje_texto = ""

    # verificar si ya está en el reloj
    if (reloj[0].num == actual or reloj[1].num == actual or reloj[2].num == actual or
        reloj[3].num == actual or reloj[4].num == actual or reloj[5].num == actual):

        mensaje_texto = f"El valor {actual} ya estaba en el reloj."
        # marcar el bit correspondiente
        for p in reloj:
            if p.num == actual:
                p.bit = True

    else:
        # buscar cuál reemplazar
        while True:
            if reloj[pos].bit:
                reloj[pos].bit = False
                pos = (pos + 1) % len(reloj)
            else:
                mensaje_texto = f"Se reemplaza {reloj[pos].num} por {actual}"
                reloj[pos].num = actual
                reloj[pos].bit = True
                pos = (pos + 1) % len(reloj)
                break

    counter += 1
    mensaje.config(text=mensaje_texto)
    actualizar_display()

# botón siguiente paso
boton = tk.Button(root, text="➡️ Siguiente paso", font=("Arial", 12, "bold"), command=paso)
boton.grid(row=3, column=0, columnspan=6, pady=20)

actualizar_display()

root.mainloop()
