import numpy as np


def color2gray(image):
    """Performs a contraction of an RGB image with a set of weights to produce a greyscale image.
    In mathematical notation, this contraction is written as
    grayscale_image_{i,j} = image_{i,j,k} weights_{k}
    where the repeated indices are summed over (einstein notation)

    Arguments:
        image: Representation of an RGB image with shape (N,M,3) and integer entries in the interval [0,255]

    Returns:
        Representation of a greyscale image with shape (N,M) and integer entries in the interval [0,255]
    """
    weights = np.array([0.21, 0.72, 0.07])
    return np.tensordot(image, weights, axes=(2, 0)).astype("uint8")
