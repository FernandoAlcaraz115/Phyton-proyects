import time
import os

def reloj():
    try:
        while True:
            
            hora_actual = time.strftime("%H:%M:%S")
            
            os.system('cls' if os.name == 'nt' else 'clear')
          
            print("Reloj en Tiempo Real")
            print("--------------------")
            print(f"    {hora_actual}    ")
            
            time.sleep(1)
    except KeyboardInterrupt:
     
        print("\nReloj detenido.")


reloj()
