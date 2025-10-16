import threading
import time 

semaforo = threading.Semaphore(1)

def acceder_recurso(id_hilo):
    with semaforo:
        print(f"Hilo {id_hilo} ha accedido al recurso en {time.strftime('%X')}.")
        time.sleep(2)  # Simula trabajo con el recurso
        print(f"Hilo {id_hilo} liberando el recurso en {time.strftime('%X')}.")

hilos = []
for i in range(6):
    hilo = threading.Thread(target=acceder_recurso, args=(i,))
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()