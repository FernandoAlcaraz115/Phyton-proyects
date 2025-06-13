import datetime
import random
import operator
import re
import sys
from colorama import Fore, Style, init

init(autoreset=True)

operations = {
    '**': operator.pow,
    '*': operator.mul,
    '/': operator.truediv,
    '+': operator.add,
    '-': operator.sub,
}

jokes = [
    "¿Por qué los programadores confunden Halloween con Navidad? Porque OCT 31 == DEC 25.",
    "¿Qué le dice un bit al otro? Nos vemos en el bus.",
    "¿Por qué el código estaba triste? Porque tenía demasiados bugs.",
    "¿Cómo se despiden los químicos? Ácido un placer.",
    "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!"
]

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

def chatbot():
    print(Fore.CYAN + "🤖 Chatbot Pro listo. Puedes pedirme la hora, fecha, hacer operaciones, o escuchar un chiste.")
    print("También puedo responder si me dices cómo te sientes. Escribe 'salir' para terminar.")

    while True:
        user_input = input(Fore.YELLOW + "\nTú: " + Style.RESET_ALL)
        limpio = limpiar_texto(user_input)

        if limpio in ["salir", "adios", "me voy"]:
            print(Fore.GREEN + "Bot: ¡Hasta pronto! 👋")
            break

        # Respuesta emocional
        respuesta_emocional = responder_emocion(limpio)
        if respuesta_emocional:
            print(Fore.GREEN + "Bot:", respuesta_emocional)
            continue

        # Respuestas generales
        if "hora" in limpio:
            print(Fore.GREEN + "Bot:", get_time())
        elif "fecha" in limpio or "dia" in limpio:
            print(Fore.GREEN + "Bot:", get_date())
        elif "chiste" in limpio:
            print(Fore.GREEN + "Bot:", tell_joke())
        elif any(palabra in limpio for palabra in ["hola", "buenas", "saludos"]):
            print(Fore.GREEN + "Bot: ¡Hola! ¿Cómo estás?")
        elif "gracias" in limpio:
            print(Fore.GREEN + "Bot: ¡Con gusto!")
        elif "como estas" in limpio:
            print(Fore.GREEN + "Bot: Estoy excelente, gracias por preguntar. ¿Y tú cómo estás?")
        elif "quien eres" in limpio:
            print(Fore.GREEN + "Bot: Soy un chatbot mejorado hecho en Python 😎")
        elif any(op in limpio for op in operations) or "resultado" in limpio or "cuanto es" in limpio:
            resultado, operacion = buscar_operacion(limpio)
            if resultado is not None:
                print(Fore.GREEN + f"Bot: El resultado de {operacion} es {resultado}")
            else:
                print(Fore.RED + "Bot: No entendí la operación. Intenta con algo como 'dame el resultado de 5 + 3'")
        else:
            print(Fore.RED + "Bot: No entendí eso. Puedes pedirme la hora, la fecha, una operación o un chiste.")

# Ejecutar chatbot
if __name__ == "__main__":
    try:
        chatbot()
    except KeyboardInterrupt:
        print(Fore.RED + "\nBot: ¡Hasta la próxima! 👋")
        sys.exit()
# Fin del código
# Este código es un chatbot simple que responde a preguntas sobre la hora, fecha, realiza operaciones matemáticas y cuenta chistes.