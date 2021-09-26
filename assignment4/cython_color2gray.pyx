import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cpdef np.ndarray[np.uint8_t, ndim=2] color2gray(np.ndarray[np.uint8_t, ndim=3] image):
    cdef int i, j, N, M
    cdef np.ndarray[np.uint8_t, ndim=2] G 
    N = np.shape(image)[0]
    M = np.shape(image)[1]
    G = np.ndarray((N,M), dtype=np.uint8)
    for i in range(N):
        for j in range(M):
            G[i][j] = image[i][j][0] * 0.21 + image[i][j][1] * 0.72 + image[i][j][2] * 0.07
    return G
