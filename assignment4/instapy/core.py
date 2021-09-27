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


def apply_filter(filter_func, input_filename, scale=None):
    img = cv2.imread(input_filename)
    if scale != None:
        img = cv2.resize(img, None, fx=scale, fy=scale)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    filtered_img = filter_func(img)
    return filtered_img


def grayscale_image(input_filename, output_filename=None, scale=None, backend=None):
    if backend is None:
        backend = "numpy"

    color2gray_backends = {
        "python": python_color2gray,
        "numpy": numpy_color2gray,
        "numba": numba_color2gray,
        "cython": cython_color2gray,
    }
    gs_img = apply_filter(
        filter_func=color2gray_backends[backend],
        input_filename=input_filename,
        scale=scale,
    )

    if output_filename is not None:
        cv2.imwrite(output_filename, gs_img)

    return gs_img


def sepia_image(input_filename, output_filename=None, scale=None, backend=None):
    if backend is None:
        backend = "numpy"

    color2sepia_backends = {
        "python": python_color2sepia,
        "numpy": numpy_color2sepia,
        "numba": numba_color2sepia,
        "cython": cython_color2sepia
    }
    s_img = apply_filter(
        filter_func=color2sepia_backends[backend],
        input_filename=input_filename,
        scale=scale,
    )

    if output_filename is not None:
        # cv2 expects BGR representation, so convert from RGB -> BGR
        s_img_BGR = cv2.cvtColor(s_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_filename, s_img_BGR)

    return s_img
