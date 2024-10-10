import cv2
from numpy import ndarray

import utils.utils as utils


def hough_transform(image : ndarray) -> ndarray:
    pass


def __run__() -> None:
    image = cv2.imread('../../img/corn.jpeg')
    gray_image = utils.img_to_gray(image)
    cv2.imshow('image', gray_image)
    cv2.waitKey(0)


if __name__ == '__main__':
    __run__()
