import numpy as np
import cv2

from .python_color2gray import python_color2gray
from .python_color2sepia import python_color2sepia
from .numpy_color2gray import numpy_color2gray
from .numpy_color2sepia import numpy_color2sepia
from .numba_color2gray import numba_color2gray
from .numba_color2sepia import numba_color2sepia

from cython_color2gray import cython_color2gray
from cython_color2sepia import cython_color2sepia


def grayscale_image(input_filename, output_filename=None, scale=None, backend=None):
    # If no backend is chosen, default to numpy
    if backend is None:
        backend = "numpy"

    color2gray_backends = {
        "python": python_color2gray,
        "numpy": numpy_color2gray,
        "numba": numba_color2gray,
        "cython": cython_color2gray,
    }
    color2gray = color2gray_backends[backend]

    img = cv2.imread(input_filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if scale != None:
        img = cv2.resize(img, None, fx=scale, fy=scale)

    grayscale_img = color2gray(img)

    if output_filename is not None:
        cv2.imwrite(output_filename, grayscale_img)

    return grayscale_img


def sepia_image(
    input_filename, output_filename=None, scale=None, backend=None, level=1.0
):
    # If no backend is chosen, default to numpy
    if backend is None:
        backend = "numpy"

    color2sepia_backends = {
        "python": python_color2sepia,
        "numpy": numpy_color2sepia,
        "numba": numba_color2sepia,
        "cython": cython_color2sepia,
    }
    color2sepia = color2sepia_backends[backend]

    img = cv2.imread(input_filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if scale != None:
        img = cv2.resize(img, None, fx=scale, fy=scale)

    sepia_img = color2sepia(img, level=level)

    if output_filename is not None:
        # cv2 expects BGR representation, so convert from RGB -> BGR
        sepia_img_BGR = cv2.cvtColor(sepia_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_filename, sepia_img_BGR)

    return sepia_img
