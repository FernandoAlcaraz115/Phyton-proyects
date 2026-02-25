import cv2

# 1. Crear un objeto de captura de video
# El número 0 indica la cámara predeterminada. Si tienes otras cámaras, prueba con 1, 2, etc.
cap = cv2.VideoCapture(0)

# 2. Verificar si la cámara se abrió correctamente
if not cap.isOpened():
    print("Error al abrir la cámara")
    exit()

# 3. Bucle para capturar y mostrar fotogramas
while True:
    # Lee un fotograma de la cámara
    ret, frame = cap.read()

    # Si el fotograma no se leyó correctamente (ret es False), salir del bucle
    if not ret:
        print("No se pudo recibir fotograma (fin del stream?). Saliendo ...")
        break

    # 4. Mostrar el fotograma en una ventana llamada 'Webcam'
    cv2.imshow('Webcam', frame)

    # 5. Romper el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# 6. Liberar la cámara y cerrar todas las ventanas al terminar
cap.release()
cv2.destroyAllWindows()

