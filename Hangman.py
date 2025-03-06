import random

def elegir_palabra():
    # Lista de palabras para el juego
    palabras = ["python", "programacion", "ahorcado", "computadora", "teclado"]
    return random.choice(palabras)  # Elige una palabra al azar

def mostrar_tablero(palabra, letras_adivinadas):
    # Muestra el estado actual de la palabra con las letras adivinadas
    tablero = ""
    for letra in palabra:
        if letra in letras_adivinadas:
            tablero += letra + " "
        else:
            tablero += "_ "
    return tablero.strip()
    
#Reglamento del juego
def ahorcado():
    palabra = elegir_palabra()  
    letras_adivinadas = set()   
    intentos_restantes = 6      

    print("¡Bienvenido al juego del ahorcado!")
    print(mostrar_tablero(palabra, letras_adivinadas))

    while intentos_restantes > 0:
        letra = input("\nIngresa una letra: ").lower()  # Convierte la letra a minúscula

        if letra in letras_adivinadas:
            print("Ya has ingresado esa letra. Intenta con otra.")
            continue

        letras_adivinadas.add(letra)  # Agrega la letra al conjunto de letras adivinadas

        if letra in palabra:
            print("¡Correcto! La letra está en la palabra.")
        else:
            intentos_restantes -= 1
            print(f"Incorrecto. Te quedan {intentos_restantes} intentos.")

        # Muestra el estado actual del tablero
        tablero_actual = mostrar_tablero(palabra, letras_adivinadas)
        print(tablero_actual)

        # Verifica si el jugador ha adivinado la palabra completa
        if "_" not in tablero_actual:
            print("\n¡Felicidades! Has adivinado la palabra.")
            break

    if intentos_restantes == 0:
        print(f"\n¡Oh no! Te has quedado sin intentos. La palabra era: {palabra}")

# Ejecuta el juego
ahorcado()