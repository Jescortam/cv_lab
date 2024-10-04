import numpy as np
from numpy import ndarray

import utils.utils


def shift_horizontally(image : ndarray, filename : str, is_left=True):
    proportions = get_horizontal_proportions(image, is_left)

    if is_left:
        for i in range(image.shape[0]):
            for j in range(1, image.shape[1]):
                image[i, j] = image[i, j - 1] / proportions[i][j - 1]
    else:
        for i in range(image.shape[0]):
            for j in range(image.shape[1] - 2, -1, -1):
                image[i, j] = image[i, j + 1] / proportions[i][j]

    utils.utils.write_csv(filename=filename, image=image, suffix="SHIFTING_H")


def shift_vertical( src, is_top=True):
    image = src.astype(np.float32)
    proportions = get_vertical_proportions(image, is_top)

    if is_top:
        for i in range(1, src.shape[0]):
            for j in range(src.shape[1]):
                image[i, j] = image[i - 1, j] / proportions[i - 1][j]
    else:
        for i in range(src.shape[0] - 2, -1, -1):
            for j in range(src.shape[1]):
                image[i, j] = image[i + 1, j] / proportions[i][j]

    return np.clip(image, 0, 255).astype(np.uint8)


def shift_from_top_left( src, is_reversed=False):
    image = src.astype(np.float32)
    proportions = get_proportions_from_top_left(image, is_reversed)

    if not is_reversed:
        for i in range(1, src.shape[0]):
            for j in range(1, src.shape[1]):
                image[i, j] = image[i - 1, j - 1] / proportions[i - 1][j - 1]
    else:
        for i in range(src.shape[0] - 2, -1, -1):
            for j in range(src.shape[1] - 2, -1, -1):
                image[i, j] = image[i + 1, j + 1] / proportions[i][j]

    return np.clip(image, 0, 255).astype(np.uint8)


def shift_from_top_right( src, is_reversed=False):
    image = src.astype(np.float32)
    proportions = get_proportions_from_top_right(image, is_reversed)

    if not is_reversed:
        for i in range(1, src.shape[0]):
            for j in range(src.shape[1] - 2, -1, -1):
                image[i, j] = image[i - 1, j + 1] / proportions[i - 1][j]
    else:
        for i in range(src.shape[0] - 2, -1, -1):
            for j in range(1, src.shape[1]):
                image[i, j] = image[i + 1, j - 1] / proportions[i][j - 1]

    return np.clip(image, 0, 255).astype(np.uint8)


def get_horizontal_proportions( image, is_left=True):
    proportions = np.ones((image.shape[0], image.shape[1] - 1))

    for i in range(image.shape[0]):
        if is_left:
            for j in range(1, image.shape[1]):
                proportions[i][j - 1] = image[i, j] / (image[i, j - 1] + 1e-5)
        else:
            for j in range(image.shape[1] - 2, -1, -1):
                proportions[i][j] = image[i, j] / (image[i, j + 1] + 1e-5)

    return proportions


def get_vertical_proportions( image, is_top=True):
    proportions = np.ones((image.shape[0] - 1, image.shape[1]))

    if is_top:
        for i in range(1, image.shape[0]):
            proportions[i - 1] = image[i] / (image[i - 1] + 1e-5)
    else:
        for i in range(image.shape[0] - 2, -1, -1):
            proportions[i] = image[i] / (image[i + 1] + 1e-5)

    return proportions


def get_proportions_from_top_left( image, is_reverse=False):
    proportions = np.ones((image.shape[0] - 1, image.shape[1] - 1))

    if not is_reverse:
        for i in range(1, image.shape[0]):
            for j in range(1, image.shape[1]):
                proportions[i - 1][j - 1] = image[i, j] / (image[i - 1, j - 1] + 1e-5)
    else:
        for i in range(image.shape[0] - 2, -1, -1):
            for j in range(image.shape[1] - 2, -1, -1):
                proportions[i][j] = image[i, j] / (image[i + 1, j + 1] + 1e-5)

    return proportions


def get_proportions_from_top_right( image, is_reversed=False):
    proportions = np.ones((image.shape[0] - 1, image.shape[1] - 1))

    if not is_reversed:
        for i in range(1, image.shape[0]):
            for j in range(image.shape[1] - 2, -1, -1):
                proportions[i - 1][j] = image[i, j] / (image[i - 1, j + 1] + 1e-5)
    else:
        for i in range(image.shape[0] - 2, -1, -1):
            for j in range(1, image.shape[1]):
                proportions[i][j - 1] = image[i, j] / (image[i + 1, j - 1] + 1e-5)

    return proportions


def merge_to_color(gray_src, color_dest):
    gray_image = gray_src.astype(np.float32) / 255.0
    color_image = color_dest.astype(np.float32)

    for i in range(color_image.shape[0]):
        for j in range(color_image.shape[1]):
            intensity = gray_image[i, j]
            color_image[i, j] /= (intensity / (1.0 / 3.0) + 1e-5)

    return np.clip(color_image, 0, 255).astype(np.uint8)
