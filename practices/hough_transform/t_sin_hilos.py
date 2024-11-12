import csv
import numpy as np
import matplotlib.pyplot as plt
import time

THRESHOLD = 50

base_path = 'C:/Users/jesus/vc-repo/cv_lab/practices/hough_transform/'

borders = np.loadtxt(f"{base_path}matriz_bordes_tic-tac-toe_png.csv", delimiter=',')
height, width = borders.shape

# Inicialización de matrices
matrix_votes_1 = np.zeros((height, width), dtype=int)
checked_borders_1 = np.ones((height, width), dtype=bool)

matrix_votes_2 = np.zeros((height, width), dtype=int)
checked_borders_2 = np.ones((height, width), dtype=bool)

matrix_votes_avg = np.zeros((height, width), dtype=float)  # Matriz para el promedio

# Función para revisar los píxeles
adjacent_border_counter = 0
def check_pixel(y, x, borders, checked_borders, trace_coordinates, coordinates_to_check):
    global adjacent_border_counter
    if borders[y, x] == 1 and not checked_borders[y, x]:
        adjacent_border_counter += 1
        trace_coordinates.append((y, x))
        coordinates_to_check.append((y, x))
        checked_borders[y, x] = True

# Función que implementa el algoritmo de búsqueda desde la esquina superior izquierda
def implementacion_1():
    global matrix_votes_1, checked_borders_1
    print("Iniciando Implementación 1 (Superior Izquierda)...")
    start_time = time.time()
    
    checked_borders_1[borders == 1] = False
    has_unchecked_1 = np.any(borders == 1)

    while has_unchecked_1:
        trace_coordinates = []
        coordinates_to_check = []

        for y in range(height):
            if np.any(~checked_borders_1[y, :]):
                x = np.where(~checked_borders_1[y, :])[0][0]
                coordinates_to_check.append((y, x))
                checked_borders_1[y, x] = True
                break

        while coordinates_to_check:
            y, x = coordinates_to_check.pop(0)
            adjacent_border_counter = 0

            if y > 0:
                if x > 0:
                    check_pixel(y - 1, x - 1, borders, checked_borders_1, trace_coordinates, coordinates_to_check)
                check_pixel(y - 1, x, borders, checked_borders_1, trace_coordinates, coordinates_to_check)
                if x < width - 1:
                    check_pixel(y - 1, x + 1, borders, checked_borders_1, trace_coordinates, coordinates_to_check)

            if x > 0:
                check_pixel(y, x - 1, borders, checked_borders_1, trace_coordinates, coordinates_to_check)
            if x < width - 1:
                check_pixel(y, x + 1, borders, checked_borders_1, trace_coordinates, coordinates_to_check)

            if y < height - 1:
                if x > 0:
                    check_pixel(y + 1, x - 1, borders, checked_borders_1, trace_coordinates, coordinates_to_check)
                check_pixel(y + 1, x, borders, checked_borders_1, trace_coordinates, coordinates_to_check)
                if x < width - 1:
                    check_pixel(y + 1, x + 1, borders, checked_borders_1, trace_coordinates, coordinates_to_check)

            trace_coordinates.append((y, x))
            trace_coordinates = list(dict.fromkeys(trace_coordinates))
            matrix_votes_1[y, x] += adjacent_border_counter
            for coord in trace_coordinates:
                matrix_votes_1[coord] += 1

        has_unchecked_1 = np.any(~checked_borders_1)

    end_time = time.time()
    print(f"Implementación 1 completada en {end_time - start_time:.2f} segundos.")

# Función que implementa el algoritmo de búsqueda desde la esquina inferior derecha
def implementacion_2():
    global matrix_votes_2, checked_borders_2
    print("Iniciando Implementación 2 (Inferior Derecha)...")
    start_time = time.time()
    
    checked_borders_2[borders == 1] = False
    has_unchecked_2 = np.any(borders == 1)

    while has_unchecked_2:
        trace_coordinates = []
        coordinates_to_check = []

        for y in range(height-1, -1, -1):  # Iterar de abajo hacia arriba
            if np.any(~checked_borders_2[y, :]):
                x = np.where(~checked_borders_2[y, :])[0][-1]  # Buscar el primer borde desde la derecha
                coordinates_to_check.append((y, x))
                checked_borders_2[y, x] = True
                break

        while coordinates_to_check:
            y, x = coordinates_to_check.pop(0)
            adjacent_border_counter = 0

            if y > 0:
                if x > 0:
                    check_pixel(y - 1, x - 1, borders, checked_borders_2, trace_coordinates, coordinates_to_check)
                check_pixel(y - 1, x, borders, checked_borders_2, trace_coordinates, coordinates_to_check)
                if x < width - 1:
                    check_pixel(y - 1, x + 1, borders, checked_borders_2, trace_coordinates, coordinates_to_check)

            if x > 0:
                check_pixel(y, x - 1, borders, checked_borders_2, trace_coordinates, coordinates_to_check)
            if x < width - 1:
                check_pixel(y, x + 1, borders, checked_borders_2, trace_coordinates, coordinates_to_check)

            if y < height - 1:
                if x > 0:
                    check_pixel(y + 1, x - 1, borders, checked_borders_2, trace_coordinates, coordinates_to_check)
                check_pixel(y + 1, x, borders, checked_borders_2, trace_coordinates, coordinates_to_check)
                if x < width - 1:
                    check_pixel(y + 1, x + 1, borders, checked_borders_2, trace_coordinates, coordinates_to_check)

            trace_coordinates.append((y, x))
            trace_coordinates = list(dict.fromkeys(trace_coordinates))
            matrix_votes_2[y, x] += adjacent_border_counter
            for coord in trace_coordinates:
                matrix_votes_2[coord] += 1

        has_unchecked_2 = np.any(~checked_borders_2)

    end_time = time.time()
    print(f"Implementación 2 completada en {end_time - start_time:.2f} segundos.")

# Función para calcular el promedio entre las dos matrices
def calcular_promedio():
    global matrix_votes_avg
    print("Calculando promedio...")
    start_time = time.time()
    
    matrix_votes_avg = (matrix_votes_1 + matrix_votes_2) / 2

    end_time = time.time()
    print(f"Promedio calculado en {end_time - start_time:.2f} segundos.")

# Iniciar las implementaciones secuenciales
print("Iniciando procesamiento secuencial...")
start_time = time.time()

# Implementación 1
implementacion_1()

# Implementación 2
implementacion_2()

# Calcular el promedio después de ambas implementaciones
calcular_promedio()

end_time = time.time()
print(f"Procesamiento secuencial completo en {end_time - start_time:.2f} segundos.")

# Mostrar los resultados de las tres implementaciones
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Implementación 1
axes[0].imshow(matrix_votes_1, cmap='hot', interpolation='nearest')
axes[0].set_title('Implementación 1: Superior Izquierda')

# Implementación 2
axes[1].imshow(matrix_votes_2, cmap='hot', interpolation='nearest')
axes[1].set_title('Implementación 2: Inferior Derecha')

# Promedio
axes[2].imshow(matrix_votes_avg, cmap='hot', interpolation='nearest')
axes[2].set_title('Promedio entre Implementaciones')

plt.show()

# Guardar las matrices de votos y el promedio en archivos CSV
with open(f"{base_path}matriz_votos_1.csv", mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(matrix_votes_1)

with open(f"{base_path}matriz_votos_2.csv", mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(matrix_votes_2)

with open(f"{base_path}matriz_votos_promedio.csv", mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(matrix_votes_avg)
