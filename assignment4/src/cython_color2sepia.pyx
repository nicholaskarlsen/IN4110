import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
cpdef np.ndarray[np.uint8_t, ndim=3] color2sepia(np.ndarray[np.uint8_t, ndim=3] image):
    cdef int i, j, k, l, N, M
    cdef float pixel
    cdef np.ndarray[np.uint8_t, ndim=3] G 
    cdef np.ndarray[np.float64_t, ndim=2] W
    W = np.array([
        [0.393, 0.769, 0.189], 
        [0.349, 0.686, 0.168], 
        [0.272, 0.534, 0.131]
    ])

    N = image.shape[0]
    M = image.shape[1]
    S = np.ndarray((N,M,3), dtype=np.uint8)

    for i in range(N):
        for j in range(M):
            for k in range(3):
                pixel = 0.0
                for l in range(3):
                    pixel += image[i][j][l] * W[k][l]
                # Avoid overflows by truncating at 255
                S[i][j][k] = min(pixel, 255)
    return S
