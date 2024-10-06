import csv

import cv2
import numpy as np
from numpy import ndarray

import utils.utils


def write_intensity_csv(image: ndarray, filename: str) -> None:
    img_height, img_width = image.shape
    intensity = int(input('Intensity : '))
    if not -1 < intensity < 256:
        write_intensity_csv(image, filename)
    height = int(input('Height :'))
    width = int(input('Width :'))
    if not -1 < height < img_height and -1 < width < img_width:
        write_intensity_csv(image, filename)
    copy_img = image.copy()
    copy_img[height][width] = intensity / 255
    utils.utils.write_csv(filename=filename, suffix='INTENSITY', image=copy_img)


def write_copy_csv(image: ndarray, filename: str) -> None:
    copy = image.copy()
    with open(filename, mode="w") as csv_file:
        _csv = csv.writer(csv_file)
        _csv.writerows(copy)
    cv2.imshow("ORIGINAL", image)
    cv2.imshow("COPY", copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def write_negative_csv(image: ndarray, filename: str) -> None:
    copy = image.copy()
    copy = 1 - copy
    utils.utils.write_csv(filename, 'NEGATIVE', copy)


def write_increment_decrement_csv(image: ndarray, filename: str) -> None:
    copy = np.array(image.copy())
    height, width = copy.shape
    increment = int(input('Increment/decrement : '))
    increment = increment / 255

    temp_img = np.zeros((height, width))
    is_negative = False
    is_overgrown = False

    for i in range(0, height):
        for j in range(0, width):
            temp_img[i][j] = copy[i][j] + increment
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

    with open(filename, mode="w") as csv_file:
        _csv = csv.writer(csv_file)
        _csv.writerows(temp_img)
    cv2.imshow("ORIGINAL", image)
    cv2.imshow("INCREMENT/DECREMENT", temp_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def contrast_elongation(image: ndarray, factor: float, filename: str) -> None:
    copy = image.copy()
    media = np.mean(copy)
    contrast = np.clip((copy - media) * factor, 0, 1)
    with open(filename, mode="w") as csv_file:
        _csv = csv.writer(csv_file)
        _csv.writerows(contrast)
    cv2.imshow("ORIGINAL", copy)
    cv2.imshow("ELONGATION", contrast)
    cv2.waitKey(0)
    cv2.destroyAllWindows()