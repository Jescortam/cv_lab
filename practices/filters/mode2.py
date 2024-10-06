import cv2
import numpy as np


def moda(vec):
    """Devuelve el valor que aparece con mayor frecuencia en el vector."""
    values, counts = np.unique(vec, return_counts=True)
    return values[np.argmax(counts)]


def aplicar_filtro_moda(imagen, kernel_size=3):
    """Aplica un filtro de moda a la imagen."""
    # Asegurarse de que el kernel_size es impar
    if kernel_size % 2 == 0:
        raise ValueError("El tamaño del kernel debe ser impar.")

    pad = kernel_size // 2
    # Añadir padding a la imagen
    imagen_padded = np.pad(imagen, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
    # Crear una imagen vacía para la salida
    imagen_filtrada = np.zeros_like(imagen)

    # Recorrer cada píxel de la imagen original
    for i in range(imagen.shape[0]):
        for j in range(imagen.shape[1]):
            # Extraer el vecindario
            vecindario = imagen_padded[i:i + kernel_size, j:j + kernel_size].reshape(-1, 3)
            # Aplicar la función de moda a cada canal
            imagen_filtrada[i, j] = [moda(vecindario[:, c]) for c in range(3)]

    return imagen_filtrada


imagen = cv2.imread('../../img/image.png')

# Aplicar filtro de moda
imagen_moda = aplicar_filtro_moda(imagen, kernel_size=5)

# Mostrar las imágenes
cv2.imshow('Original', imagen)
cv2.imshow('Filtrada con Moda', imagen_moda)
cv2.waitKey(0)
cv2.destroyAllWindows()
