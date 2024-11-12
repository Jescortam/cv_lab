import csv
import math
import numpy as np
import matplotlib.pyplot as plt

image_filename = 'tic-tac-toe_png'
border_matrix_path = f'C:/Users/jesus/vc-repo/cv_lab/practices/borders/matriz_bordes_{image_filename}.csv'
base_path = 'C:/Users/jesus/vc-repo/cv_lab/practices/hough_transform/'

# Load the matrix of borders
borders = np.loadtxt(border_matrix_path, delimiter=',')
height, width = borders.shape

num_borders = np.sum(borders)

adjacent_border_counter = 0

# Initialize matrix for storing votes
matrix_votes = np.zeros((height, width), dtype=int)

# Initialize checked_borders as True (unchecked)
checked_borders = np.ones((height, width), dtype=bool)

# Check if there are any unchecked borders
has_unchecked = np.any(borders == 1)

def check_pixel(y, x):
    global adjacent_border_counter
    if borders[y, x] == 1:
        adjacent_border_counter += 1
        if checked_borders[y, x]:
            return
        trace_coordinates.append((y, x))
        coordinates_to_check.append((y, x))
        checked_borders[y, x] = False

iterations_count = 0

while has_unchecked:
    trace_coordinates = []
    coordinates_to_check = []

    if iterations_count % 100 == 0:
        # Number of pixels visited and progress
        num_visited = np.sum(~checked_borders)
        print(f"Neighborhood progress: {math.floor(100 * num_visited / num_borders)}%; Iteration: {iterations_count}")

    # Find first unchecked coordinate and mark it
    unchecked_coords = np.argwhere(checked_borders)
    if unchecked_coords.size > 0:
        i, j = unchecked_coords[0]
        coordinates_to_check.append((i, j))
        checked_borders[i, j] = False

    while coordinates_to_check:
        y, x = coordinates_to_check.pop(0)
        adjacent_border_counter = 0

        # Explore neighbors
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width:
                    check_pixel(ny, nx)

        # Ensure uniqueness of trace_coordinates (no duplicates)
        trace_coordinates = list(set(trace_coordinates))

        # Update matrix votes based on traced coordinates
        matrix_votes[y, x] += adjacent_border_counter
        for coordinate in trace_coordinates:
            matrix_votes[coordinate[0], coordinate[1]] += 1

    # Update the has_unchecked flag after processing one batch of coordinates
    has_unchecked = np.any(checked_borders)

    iterations_count += 1

# Save the results to a CSV file
with open(f"{base_path}matriz_votos_{image_filename}.csv", mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerows(matrix_votes.tolist())

# Display the result using a heatmap
plt.imshow(matrix_votes, cmap='hot', interpolation='nearest')
plt.show()
