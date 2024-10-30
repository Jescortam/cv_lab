import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread('../../img/somewhere_in_time.jpg', 0)  # Cargar en escala de grises

# Aplicar un filtro de desenfoque para reducir el ruido
blurred = cv2.medianBlur(image, 5)

# Detectar círculos usando la transformada de Hough
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 50, param1=80, param2=20, minRadius=3, maxRadius=25)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # Dibujar el círculo detectado
        cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)

# Mostrar la imagen con los círculos detectados
cv2.imshow('Detected Ellipses', image)
cv2.waitKey(0)