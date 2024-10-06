import numpy as np
from pprint import pprint


def calculate_threshold_based_on_variance(image, num_thresholds):
    # Se calcula la frecuencia de cada intensidad de píxel
    unique, counts = np.unique(image, return_counts=True)
    frequencies = dict(zip(unique, counts))

    # Se calcula la probabilidad de cada intensidad
    total_pixels = image.size
    probabilities = {k: v / total_pixels for k, v in frequencies.items()}

    # Inicializar listas para los umbrales y las varianzas
    best_thresholds = []
    max_variances = []

    # Se calcula los intervalos de intensidad
    interval_size = 256 // num_thresholds
    thresholds = [interval_size * (i + 1) for i in range(num_thresholds - 1)]

    for threshold in thresholds:
        # Inicializar variables para el cálculo del umbral actual
        best_threshold = None
        max_variance = 0

        for t in range(1, threshold):
            # Dividir las intensidades en dos grupos basados en el umbral
            background = {k: probabilities[k] for k in probabilities if k <= t}
            foreground = {k: probabilities[k] for k in probabilities if k > t}

            # Se calcula pesos (probabilidades totales) de los fondos y formas
            weight_background = sum(background.values())
            weight_foreground = sum(foreground.values())

            if weight_background == 0 or weight_foreground == 0:
                continue

            # Se calcula medias de cada grupo
            mean_background = sum(k * v for k, v in background.items()) / weight_background
            mean_foreground = sum(k * v for k, v in foreground.items()) / weight_foreground

            # Se calcula varianza entre clases
            variance_between = weight_background * weight_foreground * (mean_background - mean_foreground) ** 2

            # Aqui se actualiza el mejor umbral si se encuentra una varianza mayor
            if variance_between > max_variance:
                max_variance = variance_between
                best_threshold = t

        # Agregar el mejor umbral y la máxima varianza a las listas
        best_thresholds.append(best_threshold)
        max_variances.append(max_variance)

    return best_thresholds, max_variances


def main():
    # Crear una matriz de imagen de ejemplo
    image_matrix = np.random.randint(0, 256, size=(10, 10))

    # Se calcula umbrales y varianzas para 3, 5, 8 y 16 tonos
    num_thresholds = [3, 5, 8, 16]
    thresholds_dict = {}
    variances_dict = {}

    for num in num_thresholds:
        thresholds, variances = calculate_threshold_based_on_variance(image_matrix, num)
        thresholds_dict[num] = thresholds
        variances_dict[num] = variances

    print("Umbrales calculados:")
    pprint(thresholds_dict)

    print("\nVarianzas máximas:")
    pprint(variances_dict)


if __name__ == "__main__":
    main()
