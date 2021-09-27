import numpy as np 
import cv2

import python_color2gray
import python_color2sepia
import numpy_color2gray
import numpy_color2sepia
import numba_color2gray
import numba_color2sepia
import cython_color2gray
import cython_color2sepia




def grayscale_image(input_filename, output_filename=None, backend="numpy"):
    color2gray_backends = {
    "python"    : python_color2gray.color2gray,
    "numpy"     : numpy_color2gray.color2gray,
    "numba"     : numba_color2gray.color2gray,
    "cython"    : cython_color2gray.color2gray
    }
    color2gray = color2gray_backends[backend]
    img = cv2.imread("img/rain.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gs_img = color2gray(img)

    if output_filename is not None:
        cv2.imwrite(output_filename, gs_img)

    return gs_img

def sepia_image(input_filename, output_filename=None, backend="numpy"):
    color2sepia_backends = {
    "python"    : python_color2sepia.color2sepia,
    "numpy"     : numpy_color2sepia.color2sepia,
    "numba"     : numba_color2sepia.color2sepia,
    "cython"    : cython_color2sepia.color2sepia
    }
    color2sepia = color2sepia_backends[backend]
    img = cv2.imread("img/rain.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    s_img = color2sepia(img)

    if output_filename is not None:
        # cv2 expects BGR representation, so convert from RGB -> BGR
        s_img_BGR = cv2.cvtColor(s_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_filename, s_img_BGR)

    return s_img