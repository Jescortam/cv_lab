import numpy as np
from tkinter import filedialog
from numpy import ndarray


def ransac_method(votes_matrix : ndarray, m_max : int):
    pass


def __run__():
    votes_matrix = np.loadtxt(filedialog.askopenfilename())
    m_max = int(input('Minimum votes number'))
    ransac_method(votes_matrix, m_max)


if __name__ == '__main__':
    __run__()