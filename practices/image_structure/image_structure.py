import csv

import cv2
from numpy import ndarray

import utils.utils as utils


def write_rgb_csv(image : ndarray, filename : str):
    height, width, _ = image.shape
    _channels = ['R', 'G', 'B']

    for i, channel in enumerate(_channels):
        channel_img = image[:, :, i]

        with open(f"{channel}_{filename}", mode="w") as csv_file:
            _csv = csv.writer(csv_file)
            _csv.writerows(channel_img)

        cv2.imshow(f"{channel}", channel_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def write_gray_csv(image : ndarray, filename : str):
    utils.write_csv(image=image, filename=filename, suffix='GRAY')
