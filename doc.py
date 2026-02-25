# ...existing code...
import cv2 

# cargar imagen original en gris y guardar copia sin modificar
img_orig = cv2.imread('color_house.png', 0)
if img_orig is None:
    print("Error: no se pudo cargar 'color_house.png'. Verifica la ruta y el nombre del archivo.")
    raise SystemExit(1)

# copia para mantener comportamiento vertical original (se mostrará como antes)
img = img_orig.copy()
cv2.imshow('Image Original', img)

# detección vertical (mantener el comportamiento original)
for row in range(len(img)):
    for col in range(len(img[row]) - 1):
        if abs(int(img[row][col]) - int(img[row][col + 1])) > 50:
            img[row][col] = 0
        else:
            img[row][col] = 255
cv2.imshow('Images verticales', img)

horiz = img_orig.copy()
rows = len(horiz)
cols = len(horiz[0])
for row in range(rows - 1):
    for col in range(cols):
        if abs(int(img_orig[row][col]) - int(img_orig[row + 1][col])) > 50:
            horiz[row][col] = 0
        else:
            horiz[row][col] = 255

cv2.imshow('Images horizontales', horiz)

cv2.waitKey(0)
cv2.destroyAllWindows()
# ...existing code...
