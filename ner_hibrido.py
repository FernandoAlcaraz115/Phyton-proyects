# ---------------------------------------------------
# Importación de librerías
# ---------------------------------------------------

import spacy  # Librería de PLN (Procesamiento de Lenguaje Natural)
import tkinter as tk  # Librería para crear interfaces gráficas
from tkinter import messagebox, scrolledtext  # Componentes adicionales de Tkinter
import time  # Para medir tiempo de ejecución
import random  # Para generar colores aleatorios

# ---------------------------------------------------
# Inicializar SpaCy
# ---------------------------------------------------

# Carga el modelo pequeño en español.
# Incluye tokenización, POS tagging, dependencias y NER.
nlp = spacy.load("es_core_news_sm")

# Se agrega el componente "entity_ruler" al pipeline.
# Se coloca después del NER para que pueda sobrescribir entidades detectadas.
# overwrite_ents=True permite reemplazar entidades existentes.
nlp.add_pipe(
    "entity_ruler",
    after="ner",
    config={"overwrite_ents": True}
)

# Se obtiene el objeto entity_ruler recién agregado al pipeline.
ruler = nlp.get_pipe("entity_ruler")

# Se agregan patrones personalizados usando expresiones regulares.
# Cada patrón define:
# - label: tipo de entidad
# - pattern: cómo identificarla
ruler.add_patterns([
    # Detecta fechas en formato dd/mm/yyyy
    {"label": "DATE", "pattern": [{"TEXT": {"REGEX": r"\d{2}/\d{2}/\d{4}"}}]},
    # Detecta códigos médicos tipo MED-12345
    {"label": "MEDICAL_CODE", "pattern": [{"TEXT": {"REGEX": r"^MED-[0-9]{5}$"}}]},
    # Detecta números de serie tipo ABC-1234
    {"label": "SERIAL_NUMBER", "pattern": [{"TEXT": {"REGEX": r"[A-Z]{3}-[0-9]{4}$"}}]},
])

# ---------------------------------------------------
# Utilidades
# ---------------------------------------------------

# Diccionario global para almacenar colores por tipo de entidad.
# Clave: label de la entidad
# Valor: color hexadecimal generado aleatoriamente
entity_colors = {}

def get_color(label):
    """
    Devuelve un color hexadecimal asociado a un tipo de entidad.
    Si el label no tiene color asignado, genera uno nuevo.
    """
    if label not in entity_colors:
        # Genera un color claro (usando caracteres de 8 a F)
        entity_colors[label] = "#" + "".join(random.choice("89ABCDEF") for _ in range(6))
    return entity_colors[label]

# ---------------------------------------------------
# Función principal de análisis
# ---------------------------------------------------

def analizar_texto():
    """
    Toma el texto ingresado por el usuario,
    ejecuta el modelo SpaCy,
    resalta entidades detectadas,
    y muestra métricas de procesamiento.
    """

    # Obtiene el texto del widget de entrada
    texto = entrada_texto.get("1.0", tk.END).strip()

    # Si no hay texto, muestra advertencia y termina ejecución
    if not texto:
        messagebox.showwarning("Advertencia", "Ingresa un texto.")
        return

    # Habilita las cajas de texto para poder escribir en ellas
    texto_coloreado.config(state="normal")
    texto_coloreado.delete("1.0", tk.END)
    lista_entidades.config(state="normal")
    lista_entidades.delete("1.0", tk.END)

    # Mide tiempo de inicio
    start_time = time.time()

    # Procesa el texto con SpaCy
    doc = nlp(texto)

    # Mide tiempo final
    end_time = time.time()

    # Índice para controlar qué parte del texto ya fue insertada
    last_idx = 0

    # Recorre cada entidad detectada en el documento
    for ent in doc.ents:

        # Inserta texto normal (sin entidad) antes de la entidad actual
        texto_coloreado.insert(tk.END, texto[last_idx:ent.start_char])

        # Obtiene color para el tipo de entidad
        color = get_color(ent.label_)
        tag = ent.label_

        # Inserta el texto de la entidad con etiqueta visual
        texto_coloreado.insert(tk.END, ent.text, tag)

        # Configura visualmente el estilo del tag
        texto_coloreado.tag_config(tag, foreground=color, font=("Arial", 11, "bold"))

        # Agrega la entidad a la lista lateral
        lista_entidades.insert(tk.END, f"{ent.text} → {ent.label_}\n")

        # Actualiza índice al final de la entidad actual
        last_idx = ent.end_char

    # Inserta el texto restante después de la última entidad
    texto_coloreado.insert(tk.END, texto[last_idx:])

    # Actualiza métricas mostradas en la interfaz
    contador_var.set(f"Entidades detectadas: {len(doc.ents)}")
    tiempo_var.set(f"Tiempo de procesamiento: {(end_time - start_time)*1000:.2f} ms")

    # Deshabilita las cajas para evitar edición manual
    texto_coloreado.config(state="disabled")
    lista_entidades.config(state="disabled")

# ---------------------------------------------------
# Función para agregar nuevas entidades dinámicamente
# ---------------------------------------------------

def agregar_entidad():
    """
    Permite al usuario agregar una nueva entidad personalizada
    mediante una etiqueta y una expresión regular.
    """

    # Obtiene valores ingresados
    etiqueta = entrada_label.get().strip().upper()
    regex = entrada_regex.get().strip()

    # Valida que ambos campos estén completos
    if not etiqueta or not regex:
        messagebox.showerror("Error", "Campos incompletos.")
        return

    # Agrega nuevo patrón al EntityRuler
    ruler.add_patterns([
        {"label": etiqueta, "pattern": [{"TEXT": {"REGEX": regex}}]}
    ])

    # Notifica éxito
    messagebox.showinfo("Éxito", f"Entidad '{etiqueta}' agregada.")

    # Limpia campos de entrada
    entrada_label.delete(0, tk.END)
    entrada_regex.delete(0, tk.END)

# ---------------------------------------------------
# Mostrar pipeline actual
# ---------------------------------------------------

def mostrar_pipeline():
    """
    Muestra los componentes activos del pipeline de SpaCy.
    """
    messagebox.showinfo("Pipeline de SpaCy", "\n".join(nlp.pipe_names))

# ---------------------------------------------------
# Construcción de la Interfaz Gráfica
# ---------------------------------------------------

# Crear ventana principal
ventana = tk.Tk()
ventana.title("NER Híbrido – Versión Final Real")
ventana.geometry("900x720")

# ------------------- Sección de entrada -------------------

tk.Label(ventana, text="Texto a analizar", font=("Arial", 13, "bold")).pack(anchor="w", padx=10)

entrada_texto = scrolledtext.ScrolledText(ventana, height=5)
entrada_texto.pack(fill="x", padx=10, pady=5)

# Botón para ejecutar análisis
tk.Button(
    ventana, text="Analizar texto",
    command=analizar_texto,
    bg="#4CAF50", fg="white"
).pack(pady=8)

# ------------------- Texto resaltado -------------------

tk.Label(ventana, text="Texto con entidades resaltadas", font=("Arial", 13, "bold")).pack(anchor="w", padx=10)

texto_coloreado = scrolledtext.ScrolledText(ventana, height=6, state="disabled")
texto_coloreado.pack(fill="x", padx=10, pady=5)

# ------------------- Lista de entidades -------------------

tk.Label(ventana, text="Entidades detectadas", font=("Arial", 13, "bold")).pack(anchor="w", padx=10)

lista_entidades = scrolledtext.ScrolledText(ventana, height=6, state="disabled")
lista_entidades.pack(fill="x", padx=10, pady=5)

# ------------------- Métricas -------------------

frame_metricas = tk.Frame(ventana)
frame_metricas.pack(fill="x", padx=10, pady=5)

# Variables dinámicas para mostrar métricas
contador_var = tk.StringVar(value="Entidades detectadas: 0")
tiempo_var = tk.StringVar(value="Tiempo de procesamiento: 0 ms")

tk.Label(frame_metricas, textvariable=contador_var, font=("Arial", 11, "bold")).pack(side="left")
tk.Label(frame_metricas, textvariable=tiempo_var, font=("Arial", 11, "bold")).pack(side="right")

# Botón para mostrar pipeline
tk.Button(
    ventana, text="Mostrar pipeline",
    command=mostrar_pipeline,
    bg="#9C27B0", fg="white"
).pack(pady=5)

# ------------------- Agregar entidad personalizada ---------------------
tk.Label(ventana, text="Agregar nueva entidad personalizada", font=("Arial", 13, "bold")).pack(anchor="w", padx=10, pady=10)

frame = tk.Frame(ventana)
frame.pack(fill="x", padx=10)

tk.Label(frame, text="Nombre de la entidad:").grid(row=0, column=0, sticky="w")
entrada_label = tk.Entry(frame, width=30)
entrada_label.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Expresión regular:").grid(row=1, column=0, sticky="w")
entrada_regex = tk.Entry(frame, width=30)
entrada_regex.grid(row=1, column=1, padx=5)

tk.Button(
    ventana, text="Agregar entidad",
    command=agregar_entidad,
    bg="#2196F3", fg="white"
).pack(pady=10)

# Inicia el bucle principal de la interfaz
ventana.mainloop()