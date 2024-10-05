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

def calcular_mediana(arreglo):
    arregloOrdenado = sorted(arreglo)
    n = len(arregloOrdenado)

    if n % 2 == 0:
        indiceMedio1 = n // 2 - 1
        indiceMedio2 = n // 2
        n1 = arregloOrdenado[indiceMedio1]
        n2 = arregloOrdenado[indiceMedio2]
        nuevo = int(n1)
        nuevo2 = int(n2)
        rs = nuevo + nuevo2

        mediana = (rs) // 2
    else:
        # Si hay un número impar de elementos, la mediana es el número en el medio
        indiceMedio = n // 2
        mediana = arregloOrdenado[indiceMedio]

    return mediana

def dispersion_valores(arreglo, promedio):
    arregloNuevo = arreglo.copy()

    for i in range(len(arregloNuevo)):
        valorA = int(arregloNuevo[i])
        arregloNuevo[i] = abs(((valorA - promedio) * 100) / promedio)

    arregloDisp = arregloNuevo

    return arregloDisp

def cambiar_valores(arregloDisp, arreglo, mediana):
    for i in range(len(arregloDisp)):
        if arregloDisp[i] > 10:
            arreglo[i] = mediana
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

        if x >= 0 and x < max_x and x<xF and y >= 0 and y < max_y and y<yF and xF > x and xF <= max_x and yF > y and yF <= max_y:
            break  # Si todo esta bien, sale del while
        else:
            print("Las coordenadas están fuera de los límites de la imagen o las iniciales son mayores que las finales. Inténtelo de nuevo.")

    return x, y, xF, yF


img = cv2.imread("../../img/somewhere_in_time.jpg", 0)
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

# Sacar la mediana
mediana = calcular_mediana(arreglo)
print("La mediana del arreglo es:", mediana)

# Sacar la dispersion de cada valor
arregloDisp = dispersion_valores(arreglo, promedio)
# Arreglo ya corregido
arregloF = cambiar_valores(arregloDisp, arreglo, mediana)

# Aqui se convierte el arreglo final de nuevo a una matriz
matriz_final = convertir_arreglo_a_matriz(arregloF, submatriz.shape)

imagenModificada = integrar_matriz_original(matriz_final, img, x, y)


cv2.imshow("Imagen modificada", imagenModificada)

cv2.waitKey(0)
cv2.destroyAllWindows()