import numpy as np


def color2gray(image):
    """Performs a contraction of an RGB image with a set of weights to produce a greyscale image.

    In this implementation, all computations are performed in pure python, and Numpy arrays are only used to
    store the data.

    Arguments:
        image: Representation of an RGB image with shape (N,M,3) and integer entries in the interval [0,255]

    Returns:
        G: Representation of a greyscale image with shape (N,M) and integer entries in the interval [0,255]
    """
    weights=[0.21, 0.72, 0.07]
    N, M, _ = np.shape(image)
    # Initialize an empty array to store the black-white image. Entries may be non-zero!
    G = np.empty(shape=(N, M), dtype="uint8")
    for i in range(N):
        for j in range(M):
            G[i][j] = 0
            for k in range(3):
                G[i][j] += image[i][j][k] * weights[k]
    return G
