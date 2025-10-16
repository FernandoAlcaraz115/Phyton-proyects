import threading
import time
import random

barrera = threading.Barrier(3)

def tarea(id_hilo):
    print(f"Hilo {id_hilo} completo la fase 1 qa las {time.strftime('%X')}.")
    time.sleep(random.uniform(0.5, 2.0))  # Simula trabajo con tiempo variable
    barrera.wait()
    
    