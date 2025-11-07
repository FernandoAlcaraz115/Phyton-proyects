import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import datetime
import random
import operator
import re

# Operaciones matemáticas
operations = {
    '**': operator.pow,
    '*': operator.mul,
    '/': operator.truediv,
    '+': operator.add,
    '-': operator.sub,
}

# Chistes
jokes = [
    "¿Por qué los programadores confunden Halloween con Navidad? Porque OCT 31 == DEC 25.",
    "¿Qué le dice un bit al otro? Nos vemos en el bus.",
    "¿Por qué el código estaba triste? Porque tenía demasiados bugs.",
    "¿Cómo se despiden los químicos? Ácido un placer.",
    "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!"
]

# Datos curiosos
facts = [
    "¿Sabías que los pulpos tienen tres corazones?",
    "Un día en Venus dura más que un año en Venus.",
    "Los tiburones existen desde antes que los árboles.",
    "Las abejas pueden reconocer rostros humanos.",
    "El corazón de una ballena azul puede pesar más de 180 kg."
]

# Corrección de errores comunes
correcciones = {
    "grasias": "gracias",
    "ora": "hora",
    "fechaa": "fecha",
    "holaa": "hola",
    "chistee": "chiste",
    "operasion": "operación",
    "resutado": "resultado",
    "cuanto": "cuánto",
    "comoo": "cómo"
}

def corregir_errores(texto):
    palabras = texto.split()
    corregidas = [correcciones.get(palabra, palabra) for palabra in palabras]
    return ' '.join(corregidas)

def limpiar_texto(texto):
    texto = texto.lower().strip()
    texto = corregir_errores(texto)
    texto = re.sub(r'[¿?¡!.,;:]', '', texto)
    return texto

def get_time():
    now = datetime.datetime.now()
    return f"La hora actual es {now.strftime('%H:%M:%S')}."

def get_date():
    today = datetime.date.today()
    return f"La fecha de hoy es {today.strftime('%d/%m/%Y')}."

def tell_joke():
    return random.choice(jokes)

def random_fact():
    return random.choice(facts)

def buscar_operacion(texto):
    for symbol in sorted(operations, key=len, reverse=True):
        pattern = rf'(-?\d+(?:\.\d+)?)\s*{re.escape(symbol)}\s*(-?\d+(?:\.\d+)?)'
        match = re.search(pattern, texto)
        if match:
            a, b = float(match.group(1)), float(match.group(2))
            try:
                resultado = operations[symbol](a, b)
                return resultado, f"{a} {symbol} {b}"
            except Exception as e:
                return f"Error al calcular: {e}", None
    return None, None

def responder_emocion(texto):
    if any(palabra in texto for palabra in ["estoy bien", "todo bien", "muy bien"]):
        return "¡Qué gusto que te encuentres bien! 😊 Puedes pedirme la hora, la fecha, una operación o un chiste."
    elif any(palabra in texto for palabra in ["estoy mal", "muy mal", "me siento mal", "triste"]):
        return "Lamento que te sientas así 😢. Si quieres distraerte, puedo contarte un chiste o decirte la hora."
    elif any(palabra in texto for palabra in ["más o menos", "mas o menos", "normal", "ahí voy"]):
        return "Entiendo, a veces hay días así. Si necesitas algo, ¡estoy aquí para ayudarte!"
    return None

def convertir_unidades(texto):
    match = re.search(r'(\d+\.?\d*)\s*(km|kilometros|celsius|°c|kg)', texto)
    if match:
        cantidad = float(match.group(1))
        unidad = match.group(2)
        if unidad in ["km", "kilometros"]:
            millas = round(cantidad * 0.621371, 2)
            return f"{cantidad} kilómetros son aproximadamente {millas} millas."
        elif unidad in ["celsius", "°c"]:
            fahrenheit = round(cantidad * 9/5 + 32, 2)
            return f"{cantidad}°C son aproximadamente {fahrenheit}°F."
        elif unidad == "kg":
            libras = round(cantidad * 2.20462, 2)
            return f"{cantidad} kg son aproximadamente {libras} libras."
    return None

def responder_preguntas_frecuentes(texto):
    if "quien eres" in texto:
        return "Soy un chatbot en Python, diseñado para ayudarte y entretenerte. 😎"
    if "que puedes hacer" in texto:
        return "Puedo darte la hora, fecha, contar chistes, hacer operaciones, decirte un dato curioso y convertir unidades. ¡Pruébame!"
    if "eres inteligente" in texto:
        return "¡Estoy aprendiendo más cada día! 🤖"
    if "cumpleaños" in texto:
        return "¡Feliz cumpleaños! 🎉 Espero que tengas un día increíble."
    return None

def procesar_input():
    user_text = entrada.get()
    entrada.delete(0, tk.END)
    if not user_text.strip():
        return

    agregar_mensaje(f"Tú: {user_text}")

    limpio = limpiar_texto(user_text)

    if limpio in ["salir", "adios", "me voy"]:
        agregar_mensaje("Bot: ¡Hasta pronto! 👋")
        ventana.quit()
        return

    respuesta = responder_emocion(limpio)
    if respuesta:
        agregar_mensaje(f"Bot: {respuesta}")
        return

    # Respuestas a preguntas frecuentes
    respuesta = responder_preguntas_frecuentes(limpio)
    if respuesta:
        agregar_mensaje(f"Bot: {respuesta}")
        return

    # Conversión de unidades
    respuesta = convertir_unidades(limpio)
    if respuesta:
        agregar_mensaje(f"Bot: {respuesta}")
        return

    # Dato curioso
    if any(p in limpio for p in ["dato curioso", "sorprendeme", "cuentame algo", "curioso"]):
        agregar_mensaje(f"Bot: {random_fact()}")
        return

    # Hora y fecha
    if "hora" in limpio:
        agregar_mensaje(f"Bot: {get_time()}")
    elif "fecha" in limpio or "dia" in limpio:
        agregar_mensaje(f"Bot: {get_date()}")
    # Chistes
    elif "chiste" in limpio or "broma" in limpio:
        agregar_mensaje(f"Bot: {tell_joke()}")
    # Saludos
    elif any(p in limpio for p in ["hola", "buenas", "saludos", "hey"]):
        agregar_mensaje("Bot: ¡Hola! ¿Cómo estás?")
    # Agradecimientos
    elif "gracias" in limpio:
        agregar_mensaje("Bot: ¡Con gusto!")
    # ¿Cómo estás?
    elif "como estas" in limpio:
        agregar_mensaje("Bot: Estoy excelente, gracias por preguntar. ¿Y tú cómo estás?")
    # Operaciones matemáticas
    elif any(op in limpio for op in operations) or "resultado" in limpio or "cuanto es" in limpio or "calcula" in limpio:
        resultado, operacion = buscar_operacion(limpio)
        if resultado is not None:
            agregar_mensaje(f"Bot: El resultado de {operacion} es {resultado}")
        else:
            agregar_mensaje("Bot: No entendí la operación. Intenta con algo como 'dame el resultado de 5 + 3'")
    else:
        agregar_mensaje("Bot: No entendí eso. Puedes pedirme la hora, la fecha, una operación, un chiste o un dato curioso.")

def agregar_mensaje(mensaje):
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, mensaje + "\n")
    chat.config(state=tk.DISABLED)
    chat.see(tk.END)

def limpiar_chat():
    chat.config(state=tk.NORMAL)
    chat.delete(1.0, tk.END)
    chat.config(state=tk.DISABLED)

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Chatbot Pro")
ventana.geometry("600x400")
ventana.configure(bg="#1e1e1e")

chat = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, state=tk.DISABLED, font=("Segoe UI", 11), bg="#2e2e2e", fg="#ffffff")
chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

frame_entrada = tk.Frame(ventana, bg="#1e1e1e")
frame_entrada.pack(pady=5, fill=tk.X, padx=10)

entrada = tk.Entry(frame_entrada, font=("Segoe UI", 11), bg="#3c3c3c", fg="#ffffff", insertbackground="white")
entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10))
entrada.bind("<Return>", lambda event: procesar_input())

# Botón para enviar el mensaje
boton_enviar = ttk.Button(frame_entrada, text="Enviar", command=procesar_input)
boton_enviar.pack(side=tk.RIGHT)

# Botón para limpiar el chat
boton_limpiar = ttk.Button(ventana, text="Limpiar chat", command=limpiar_chat)
boton_limpiar.pack(pady=2)

# Mensaje de bienvenida
agregar_mensaje("Bot: 🤖 Chatbot Pro listo. Puedes pedirme la hora, fecha, operaciones, un chiste o un dato curioso.\nTambién puedo responder si me dices cómo te sientes.")

# Ejecutar app
ventana.mainloop()

# Fin del código
# Este código es un chatbot simple que responde a preguntas sobre la hora, fecha, realiza operaciones matemáticas y cuenta chistes.