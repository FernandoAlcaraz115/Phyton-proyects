import os
import random
import time

try:
    import colorama
    colorama.init()
    GREEN = colorama.Fore.GREEN
    RESET = colorama.Style.RESET_ALL
except ImportError:
    GREEN = "\033[32m"
    RESET = "\033[0m"

# Constantes
LIMITE_CARRERA = 97
LONGITUD_PISTA = 115

def buses(n1, n2):
    output = []
    output.append(LONGITUD_PISTA * "-")
    output.append((n1 * " ") + "_______________  " + ((100 - n1) * " ") + "|")
    output.append((n1 * " ") + "|__|__|__|__|__|___ " + ((97 - n1) * " ") + "|")
    output.append((n1 * " ") + "|    Fernando     |)" + ((96 - n1) * " ") + "|")
    output.append((n1 * " ") + "|~~~@~~~~~~~~~@~~~|)" + ((95 - n1) * " ") + "|")
    output.append(LONGITUD_PISTA * "_")
    output.append((n2 * " ") + "_______________  " + ((100 - n2) * " ") + "|")
    output.append((n2 * " ") + "|__|__|__|__|__|___ " + ((97 - n2) * " ") + "|")
    output.append((n2 * " ") + "|     Julian      |)" + ((96 - n2) * " ") + "|")
    output.append((n2 * " ") + "|~~~@~~~~~~~~~@~~~|)" + ((95 - n2) * " ") + "|")
    output.append(LONGITUD_PISTA * "_")
    return "\n".join(output)

def main():
    a = 0
    b = 0
    gano = None

    os.system("cls" if os.name == "nt" else "clear")
    presentacion = """
        <<<<<<<<<<< Carrera de buses de Fernando :D >>>>>>>>>>
            Fernando vs Julian """
    print(presentacion)
    time.sleep(3)

    while a < LIMITE_CARRERA and b < LIMITE_CARRERA:
        c = random.randint(1, 2)
        if c == 1:
            a += 1
        if c == 2:
            b += 1
        os.system("cls" if os.name == "nt" else "clear")
        print(buses(a, b))
        time.sleep(0.07)

    if a >= LIMITE_CARRERA:
        gano = "Fernando"
    if b >= LIMITE_CARRERA:
        gano = "Julian"

    print(f"{GREEN}GANÓ LA CARRERA: {gano}{RESET}")

if __name__ == "__main__":
    main()