import numpy as np


def python_color2sepia(image):
    W = np.array(
        [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]],
        dtype=np.float64,
    )
    N, M, _ = np.shape(image)
    S = np.empty(shape=(N, M, 3), dtype="uint8")
    for i in range(N):
        for j in range(M):
            for k in range(3):
                pixel = 0
                for l in range(3):
                    pixel += image[i][j][l] * W[k][l]
                # Avoid overflows by truncating at 255
                S[i][j][k] = min(pixel, 255)
    return S
