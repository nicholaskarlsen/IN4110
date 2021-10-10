from .core import (
    grayscale_image,
    sepia_image,
    benchmark_sepia_img,
    benchmark_grayscale_img,
)
from .python_color2gray import python_color2gray
from .python_color2sepia import python_color2sepia
from .numpy_color2gray import numpy_color2gray
from .numpy_color2sepia import numpy_color2sepia
from .numba_color2gray import numba_color2gray
from .numba_color2sepia import numba_color2sepia
from cython_color2gray import cython_color2gray
from cython_color2sepia import cython_color2sepia
