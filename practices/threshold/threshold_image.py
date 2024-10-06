import numpy as np


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


#Basado en entropia
def calculate_threshold_based_on_entropy(image):
    unique, counts = np.unique(image, return_counts=True)
    total_pixels = image.size
    probabilities = counts / total_pixels

    # Se calcula la entropía para cada posible umbral
    best_threshold = None
    max_entropy = -np.inf

    for threshold in range(unique.min(), unique.max()):
        # Dividir las intensidades en dos grupos basados en el umbral
        background_probs = probabilities[unique <= threshold]
        foreground_probs = probabilities[unique > threshold]

        if background_probs.size == 0 or foreground_probs.size == 0:
            continue

        # Se calcula la entropía para el fondo y para el objeto
        background_entropy = -np.sum(background_probs * np.log2(background_probs + np.finfo(float).eps))
        foreground_entropy = -np.sum(foreground_probs * np.log2(foreground_probs + np.finfo(float).eps))

        # Se calcula la entropía total como la suma de ambas entropías
        total_entropy = background_entropy + foreground_entropy

        # Actualizar el mejor umbral si se encuentra una entropía total mayor
        if total_entropy > max_entropy:
            max_entropy = total_entropy
            best_threshold = threshold

    return best_threshold


#Valle global
def find_global_valley_threshold_corrected(image):
    unique, counts = np.unique(image.ravel(), return_counts=True)
    total_pixels = image.size

    # Crear el histograma de la imagen
    histogram, bin_edges = np.histogram(image, bins=np.arange(257), density=True)

    # Se calcula la función de coste para cada umbral potencial
    best_threshold = None
    min_cost = np.inf

    for threshold in range(1, 256):
        # histograma en dos partes
        hist_background = histogram[:threshold]
        hist_foreground = histogram[threshold:]

        # Se calcula las probabilidades acumuladas para el fondo y el objeto
        omega_background = np.sum(hist_background)
        omega_foreground = np.sum(hist_foreground)

        if omega_background == 0 or omega_foreground == 0:
            continue

        # Asegurar que las dimensiones de los arrays coinciden para las operaciones
        mu_background = np.sum(hist_background * np.arange(threshold)) / omega_background
        mu_foreground = np.sum(hist_foreground * np.arange(threshold, 256)) / omega_foreground

        # Se calcula la varianza entre clases(o su inversa como coste)
        variance_between = omega_background * omega_foreground * (mu_background - mu_foreground) ** 2

        # Buscar el mínimo de la varianza entre clases(máximo de la inversa)
        if variance_between < min_cost:
            min_cost = variance_between
            best_threshold = threshold

    return best_threshold


def main():
    matrix = [[178, 38, 124, 72, 198],
              [246, 164, 3, 55, 133],
              [222, 171, 242, 173, 214],
              [246, 171, 196, 143, 79],
              [180, 248, 25, 150, 161]]

    matriz = np.array(matrix)

    matriz_valle = find_global_valley_threshold_corrected(matriz)
    matriz_entropia = calculate_threshold_based_on_entropy(matriz)
    matrix_variances = calculate_threshold_based_on_variance(matriz, num_thresholds=3)

    print("valle: ", matriz_valle)
    print("entropia: ", matriz_entropia)
    print("variance: ", matrix_variances)


if __name__ == "__main__":
    main()
