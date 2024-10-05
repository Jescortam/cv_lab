import cv2
import numpy as np


def obtener_submatriz(img, x, y, xF, yF):
    # Límites para la submatriz
    fila_inicio = max(0, x)
    fila_fin = min(len(img), xF)
    col_inicio = max(0, y)
    col_fin = min(len(img[0]), yF)

    # Extraer la submatriz
    submatriz = img[fila_inicio:fila_fin, col_inicio:col_fin]

    return submatriz


def calcular_moda(arreglo):
    # Diccionario para contar la frecuencia de cada elemento en el arreglo
    conteo = {}
    for elemento in arreglo:
        conteo[elemento] = conteo.get(elemento, 0) + 1

    # Encontrar el numero de veces maximo, en el que se repite algun elemento
    frecuencia_maxima = max(conteo.values())

    modas = [elemento for elemento, frecuencia in conteo.items() if frecuencia == frecuencia_maxima]

    # Calcular el promedio de las modas si hay más de una
    if len(modas) > 1:
        suma_modas = sum(modas)
        promedio_modas = suma_modas / len(modas)
        moda = int(promedio_modas)
    else:
        moda = modas[0]  # Si solo hay una moda

    return moda


def dispersion_valores(arreglo, promedio):
    arreglo_nuevo = arreglo.copy()

    for i in range(len(arreglo_nuevo)):
        valorA = int(arreglo_nuevo[i])
        arreglo_nuevo[i] = abs(((valorA - promedio) * 100) / promedio)

    arreglo_dispersiones = arreglo_nuevo

    return arreglo_dispersiones


def cambiar_valores(arreglo_dispersiones, arreglo, moda):
    for i in range(len(arreglo_dispersiones)):
        if arreglo_dispersiones[i] > 10:
            arreglo[i] = moda
            #print("se cambio")

    arregloF = arreglo

    return arregloF


def convertir_arreglo_a_matriz(arreglo, forma_original):
    matriz = np.reshape(arreglo, forma_original)
    return matriz


def integrar_matriz_original(matriz_final, matriz_original, x, y):
    xF, yF = x + matriz_final.shape[0], y + matriz_final.shape[1]
    matriz_original[x:xF, y:yF] = matriz_final
    return matriz_original


def matriz_inicial(img):
    max_x, max_y = img.shape

    while True:
        x = int(input("Ingrese la coordenada de inicio x: "))
        y = int(input("Ingrese la coordenada de inicio y: "))
        xF = int(input("Ingrese la coordenada del final x: "))
        yF = int(input("Ingrese la coordenada del final y: "))

        if x >= 0 and x < max_x and x < xF and y >= 0 and y < max_y and y < yF and xF > x and xF <= max_x and yF > y and yF <= max_y:
            break  # Si todo esta bien, sale del while
        else:
            print(
                "Las coordenadas están fuera de los límites de la imagen o las iniciales son mayores que las finales. Inténtelo de nuevo.")

    return x, y, xF, yF


img = cv2.imread("../../img/image.png", 0)
np.set_printoptions(threshold=np.inf)
cv2.imshow("Imagen original", img)

x, y, xF, yF = matriz_inicial(img)

# Se obtiene el pedazo de la matriz
submatriz = obtener_submatriz(img, x, y, xF, yF)

#Se convierte a arreglo
arreglo = np.ravel(submatriz)

# Sacar el promedio
suma_valores = sum(arreglo)
cantidad_elementos = len(arreglo)
promedio = suma_valores / cantidad_elementos
print("El promedio es", promedio)

# Sacar la moda
moda = calcular_moda(arreglo)
print("La moda del arreglo es:", moda)

# Sacar la dispersion de cada valor
arreglo_dispersiones = dispersion_valores(arreglo, promedio)
#print("El arreglo de dispersiones es:", arreglo_dispersiones)

# Arreglo ya corregido
arregloF = cambiar_valores(arreglo_dispersiones, arreglo, moda)
#print(arregloF)

# Aqui se convierte el arreglo final de nuevo a una matriz
matriz_final = convertir_arreglo_a_matriz(arregloF, submatriz.shape)

imagenModificada = integrar_matriz_original(matriz_final, img, x, y)


cv2.imshow("Imagen modificada", imagenModificada)

cv2.waitKey(0)
cv2.destroyAllWindows()
