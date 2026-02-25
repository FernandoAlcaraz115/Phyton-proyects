import tkinter as tk
from tkinter import messagebox
import random

def mover_boton_no(event):
    """
   
    """
    # Obtener el tamaño de la ventana y del botón
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    btn_width = btn_no.winfo_width()
    btn_height = btn_no.winfo_height()

    # Generar nuevas coordenadas aleatorias respetando los márgenes
    # Dejamos un margen de 50px para que no se salga de la pantalla
    new_x = random.randint(20, window_width - btn_width - 20)
    new_y = random.randint(20, window_height - btn_height - 20)

    # Mover el botón
    btn_no.place(x=new_x, y=new_y)

def accion_si():
    """
    Función que se ejecuta cuando ella dice que SÍ.
    """
    # Limpiamos los widgets anteriores
    lbl_pregunta.destroy()
    btn_si.destroy()
    btn_no.destroy()
    
    # Cambiamos el fondo y mostramos el mensaje de amor
    root.configure(bg='#ffdde2') # Un rosa más claro
    
    lbl_final = tk.Label(root, text="¡Sabía que dirías que sí!\nTE AMO ❤️😍💍", 
                         font=("Arial Rounded MT Bold", 24, "bold"), 
                         fg="#d6004f", bg='#ffdde2')
    lbl_final.pack(expand=True)
    
    # Permitimos cerrar la ventana ahora (opcional, pero recomendado tras el éxito)
    root.protocol("WM_DELETE_WINDOW", root.destroy)

def al_intentar_cerrar():
    """
    Evita que la ventana se cierre con la X.
    """
    messagebox.showwarning("¡Ups!", "No puedes escapar de esta pregunta... 🥺👉👈")

# --- Configuración de la Ventana Principal ---
root = tk.Tk()
root.title("Una pregunta importante... ❤️")
root.geometry("600x400")
root.configure(bg='#ffe6ea') # Fondo rosa pastel
root.resizable(False, False) # Evitar que redimensione la ventana

# Bloquear el botón de cerrar ventana (la X)
root.protocol("WM_DELETE_WINDOW", al_intentar_cerrar)

# --- Elementos de la Interfaz ---

# Etiqueta de la pregunta
lbl_pregunta = tk.Label(root, text="¿Quieres ser mi novia? 🌹", 
                        font=("Arial Rounded MT Bold", 26, "bold"), 
                        fg="#ff0055", bg='#ffe6ea')
lbl_pregunta.pack(pady=80)

# Botón SÍ
btn_si = tk.Button(root, text="¡SÍ! 😍", command=accion_si, 
                   font=("Arial", 14, "bold"), bg="#ff4d79", fg="white", 
                   activebackground="#ff0040", activeforeground="white",
                   relief="raised", bd=5, width=10)
btn_si.place(x=180, y=250)

# Botón NO
btn_no = tk.Button(root, text="No 😢", 
                   font=("Arial", 14, "bold"), bg="white", fg="black", 
                   relief="raised", bd=5, width=10)
btn_no.place(x=320, y=250)

# Vincular el evento del mouse: cuando el cursor "entra" al área del botón No
btn_no.bind('<Enter>', mover_boton_no)

# Iniciar la aplicación
root.mainloop()