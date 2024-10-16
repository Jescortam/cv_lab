import cv2
import numpy as np
from cv2.typing import MatLike
from numpy import ndarray
import os
import csv


def write_csv(filename: str, suffix: str, image: ndarray):
    with open(filename, mode="w") as csv_file:
        _csv = csv.writer(csv_file)
        _csv.writerows(image)
    cv2.imshow(suffix, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def regularize(image: ndarray) -> ndarray:
    copy = np.array(image.copy())
    height, width = copy.shape
    temp_img = np.zeros((height, width))
    is_negative = False
    is_overgrown = False

    for i in range(0, height):
        for j in range(0, width):
            temp_img[i][j] = copy[i][j]
            if temp_img[i][j] > 1:
                is_overgrown = True
            elif temp_img[i][j] < 0:
                is_negative = True

    if is_negative:
        minimum = temp_img.min()
        absolute = np.absolute(minimum)
        for i in range(0, height):
            for j in range(0, width):
                temp_img[i][j] = temp_img[i][j] + absolute

    if is_overgrown:
        maximum = temp_img.max()
        for i in range(0, height):
            for j in range(0, width):
                temp_img[i][j] = temp_img[i][j] / np.absolute(maximum) * 1

    return temp_img


def img_to_gray(image: ndarray) -> ndarray:
    _height, _width, _ = image.shape
    gray_img = np.zeros((_height, _width))
    for i in range(0, _height):
        for j in range(0, _width):
            gray_img[i][j] = (image[i][j][0] * 0.33 + image[i][j][1] * 0.33 + image[i][j][2] * 0.33) / 255
    return gray_img


def clean_csv_files() -> None:
    filelist = [f for f in os.listdir(os.getcwd()) if f.endswith(".csv")]
    for f in filelist:
        os.remove(os.path.join(os.getcwd(), f))


def _is_border(y: int, x: int, neighborhoods: ndarray):
    height, width, _ = neighborhoods.shape()

    if y > 0:
        if x > 0 and neighborhoods[y][x] != neighborhoods[y - 1][x - 1]:
            return True
        if neighborhoods[y][x] != neighborhoods[y - 1][x]:
            return True
        if x < width - 1 and neighborhoods[y][x] != neighborhoods[y - 1][x + 1]:
            return True

    if x > 0 and neighborhoods[y][x] != neighborhoods[y][x - 1]:
        return True
    if x < width - 1 and neighborhoods[y][x] != neighborhoods[y][x + 1]:
        return True

    if y < height - 1:
        if x > 0 and neighborhoods[y][x] != neighborhoods[y + 1][x - 1]:
            return True
        if neighborhoods[y][x] != neighborhoods[y + 1][x]:
            return True
        if x < width - 1 and neighborhoods[y][x] != neighborhoods[y + 1][x + 1]:
            return True

    return False


def _has_uncolored(colored_matrix: ndarray[any, np.dtype[bool]]):
    return not np.all(colored_matrix)


def _when_pixel_applies_to_nb(y: int, x: int,
                              colored_matrix: ndarray[any, np.bool],
                              checked_matrix: ndarray[any, np.bool],
                              neighborhoods: ndarray[any, np.int32],
                              current_nb: int):

    colored_matrix[y][x] = True
    checked_matrix[y][x] = True
    neighborhoods[y][x] = current_nb
    pass


def find_borders(image: MatLike):
    THRESHOLD = 70
    height, width, _ = image.shape()
    gray_image = img_to_gray(image)

    colored_matrix = np.zeros((height, width), dtype=np.bool)
    # colored_matrix = [[False for _ in range(width)] for _ in range(height)]
    borders_matrix = np.zeros((height, width))

    # neighborhoods = [[None for _ in range(width)] for _ in range(height)]
    neighborhoods = np.empty((height, width), dtype=np.int32)
    current_nb = 0

    while _has_uncolored(colored_matrix):
        nb_pivot = None

        checked_matrix = np.copy(colored_matrix)
        matrix_to_check = []

        while len(matrix_to_check) != 0:
            y, x = matrix_to_check.pop(0)
            _when_pixel_applies_to_nb(y, x,
                                      colored_matrix,
                                      checked_matrix,
                                      neighborhoods)

        current_nb += 1

    for i, row in enumerate(neighborhoods):
        for j, pixel in enumerate(row):
            if _is_border(i, j, neighborhoods):
                borders_matrix[i][j] = 1

    decimal_matrix = np.zeros((height, width), dtype=np.float64)

    for i in range(height):
        for j in range(width):
            decimal_matrix[i][j] = gray_image[i][j] / 255
