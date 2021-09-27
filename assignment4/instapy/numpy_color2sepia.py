import numpy as np


def numpy_color2sepia(image, level=1.0):
    """
    Applies a sepia filter to an array representation of an RGB image. The level of the sepia filter
    may also be adjusted.

    Arguments:
        image: 3D Array with dimensions (N, M, 3)
        level: level of the sepia filter, must be in the interval [0,1]
    
    Returns:
        S: 3D Array with the same dimensions as the input image that has been transformed with the filter
    """
    assert 0.0 <= level <= 1.0
    W = np.array(
        [
            [
                0.393 + 0.607 * (1.0 - level),
                0.769 - 0.760 * (1.0 - level),
                0.189 - 0.189 * (1.0 - level),
            ],
            [
                0.349 - 0.349 * (1.0 - level),
                0.686 + 0.314 * (1.0 - level),
                0.168 - 0.168 * (1.0 - level),
            ],
            [
                0.272 - 0.272 * (1.0 - level),
                0.534 - 0.534 * (1.0 - level),
                0.131 + 0.869 * (1.0 - level),
            ],
        ],
        dtype=np.float64,
    )
    S = image.dot(W.T)
    S = np.minimum(255, S)
    S = S.astype("uint8")
    return S
