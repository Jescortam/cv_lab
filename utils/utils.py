import numpy as np
from numpy import ndarray
import os


def regularize(image : ndarray) -> ndarray:
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


def img_to_gray(image : ndarray) -> ndarray:
    _height, _width, _ = image.shape
    gray_img = np.zeros((_height, _width))
    for i in range(0, _height):
        for j in range(0, _width):
            gray_img[i][j] = (image[i][j][0] * 0.33 + image[i][j][1] * 0.33 + image[i][j][2] * 0.33) / 255
    return gray_img


def clean_csv_files() -> None:
    filelist = [ f for f in os.listdir(os.getcwd()) if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(os.getcwd(), f))
