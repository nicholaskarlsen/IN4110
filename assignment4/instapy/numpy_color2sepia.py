import numpy as np


def numpy_color2sepia(image):
    W = np.array(
        [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]],
        dtype=np.float64,
    )
    S = image.dot(W.T)
    S = np.minimum(255, S)
    S = S.astype("uint8")
    return S
