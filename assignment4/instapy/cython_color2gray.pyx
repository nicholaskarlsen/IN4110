import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cpdef np.ndarray[np.uint8_t, ndim=2] cython_color2gray(np.ndarray[np.uint8_t, ndim=3] image):
    """
    Performs a contraction of an RGB image with a set of weights to produce a greyscale image.

    Arguments:
        image: Representation of an RGB image with shape (N,M,3) and integer entries in the interval [0,255]

    Returns:
        G: Representation of a greyscale image with shape (N,M) and integer entries in the interval [0,255]
    """
    cdef int i, j, N, M
    cdef np.ndarray[np.uint8_t, ndim=2] G 
    N = image.shape[0]
    M = image.shape[1]
    G = np.ndarray((N,M), dtype=np.uint8)
    for i in range(N):
        for j in range(M):
            G[i][j] = image[i][j][0] * 0.21 + image[i][j][1] * 0.72 + image[i][j][2] * 0.07
    return G
