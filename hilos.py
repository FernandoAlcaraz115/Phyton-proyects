import threading

contador = 0
lock = threading.Lock()

def incrementar():
    global contador
    for _ in range(1000):
        with lock:
            contador += 1

hilos = []
for _ in range(5):
    hilo = threading.Thread(target=incrementar)
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()

print("Valor final del contador:", contador)

