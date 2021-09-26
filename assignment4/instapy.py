import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("rain.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def grayscale_np(image, weights=np.array([0.21, 0.72, 0.07])):
    """An RGB image (I) may be loosely thought of as a rank-3 tensor.
    Thus, to produce a black-white image (G), a rank-2 tensor we may perform a tensor contraction
    with the set of weights (W) in the following way;
        G[i][j] = I[i,j,k] * W[k]
    Where the Einstein summation convention is adopted, and repeated indices (k) are summed over.

    This computation is thus very efficiently implemented using the einsum functionality in numpy.
    """
    return np.einsum("ijk,k->ij", image, weights).astype("uint8")


# cv2.imwrite("rain_grayscale.jpeg", grayscale_np(image))

from cython_color2gray import hello

hello()
