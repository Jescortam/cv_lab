import cv2

import utils.utils as utils


def ransac_method():
    pass


def __run__():
    image = cv2.imread('../../img/corn.jpeg')
    gray_image = utils.img_to_gray(image)
    cv2.imshow('image', gray_image)
    cv2.waitKey(0)


if __name__ == '__main__':
    __run__()