import threading
import time
import random

buffer = []
CAPACIDAD_BUFFER = 5
condicion = threading.Condition()

def productor():
    for i in range(10):
        with condicion:
            while len(buffer) >= CAPACIDAD_BUFFER:
                condicion.wait()               # paréntesis faltantes
            item = f"item-{i}"
            buffer.append(item)
            print(f"Productor produjo: {item} . Buffer: {buffer}")
            condicion.notify_all()           # mejor notify_all() para despertar a todos
        time.sleep(random.uniform(0.1, 0.5))  # pasar parámetros a uniform()

def consumidor():
    for i in range(10):
        with condicion:
            while len(buffer) == 0:
                condicion.wait()
            item = buffer.pop(0)
            print(f"Consumidor consumió: {item} . Buffer: {buffer}")
            condicion.notify_all()
        time.sleep(random.uniform(0.1, 0.5))

def main():
    hilo_productor = threading.Thread(target=productor, name="Productor")
    hilo_consumidor = threading.Thread(target=consumidor, name="Consumidor")

    hilo_productor.start()
    hilo_consumidor.start()

    # Esperar a que terminen
    hilo_productor.join()
    hilo_consumidor.join()

if __name__ == "__main__":
    main()
