import csv
import numpy as np
import matplotlib.pyplot as plt

THRESHOLD = 50

base_path = 'C:/Users/jesus/vc-repo/cv_lab/practices/hough_transform/'

borders = np.loadtxt(f"{base_path}matriz_bordes_tic-tac-toe_png.csv", delimiter=',')
height, width = borders.shape

matrix_votes = np.zeros((height, width), dtype=int)
checked_borders = np.ones((height, width), dtype=bool)

checked_borders[borders == 1] = False
has_unchecked = np.any(borders == 1)

adjacent_border_counter = 0
def check_pixel(y, x):
    global adjacent_border_counter
    if borders[y, x] == 1 and not checked_borders[y, x]:
        adjacent_border_counter += 1
        trace_coordinates.append((y, x))
        coordinates_to_check.append((y, x))
        checked_borders[y, x] = True

while has_unchecked:
    trace_coordinates = []
    coordinates_to_check = []

    for y in range(height):
        if np.any(~checked_borders[y, :]):
            x = np.where(~checked_borders[y, :])[0][0]
            coordinates_to_check.append((y, x))
            checked_borders[y, x] = True
            break

    while coordinates_to_check:
        y, x = coordinates_to_check.pop(0)
        adjacent_border_counter = 0

        if y > 0:
            if x > 0:
                check_pixel(y - 1, x - 1)
            check_pixel(y - 1, x)
            if x < width - 1:
                check_pixel(y - 1, x + 1)

        if x > 0:
            check_pixel(y, x - 1)
        if x < width - 1:
            check_pixel(y, x + 1)

        if y < height - 1:
            if x > 0:
                check_pixel(y + 1, x - 1)
            check_pixel(y + 1, x)
            if x < width - 1:
                check_pixel(y + 1, x + 1)

        trace_coordinates.append((y, x))
        trace_coordinates = list(dict.fromkeys(trace_coordinates))
        matrix_votes[y, x] += adjacent_border_counter
        for coord in trace_coordinates:
            matrix_votes[coord] += 1

    has_unchecked = np.any(~checked_borders)

max_votes = np.max(matrix_votes)
max_votes_y, max_votes_x = np.unravel_index(np.argmax(matrix_votes), matrix_votes.shape)

print('Max votes:', max_votes)
print('X:', max_votes_x)
print('Y:', max_votes_y)

with open(f"{base_path}matriz_votos.csv", mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(matrix_votes)

# Mostrar la matriz de votos
plt.imshow(matrix_votes, cmap='hot', interpolation='nearest')
plt.show()