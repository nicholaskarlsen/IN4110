import numpy as np
import cv2
import timeit

from .python_color2gray import python_color2gray
from .python_color2sepia import python_color2sepia
from .numpy_color2gray import numpy_color2gray
from .numpy_color2sepia import numpy_color2sepia
from .numba_color2gray import numba_color2gray
from .numba_color2sepia import numba_color2sepia

from cython_color2gray import cython_color2gray
from cython_color2sepia import cython_color2sepia


def grayscale_image(input_filename, output_filename=None, scale=None, backend=None):
    """
    Applies a grayscale filter to an image. May also optionally resize and save the image.

    Arguments:
        input_filename: Filename of the image you wish to apply a filter to
        output_filename: Filename of the output file if you wish to store the transformed image.
            If set to None, the image will not be written to file.
        scale: optional scalefactor to apply to the image prior to applying the filter
        backend: Choose which of the backends to utilize. If None is set, default to Numpy.

    Returns:
        grayscale_img
    """
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
        new_width = int(img.shape[1] * scale)
        new_height = int(img.shape[0] * scale)
        new_dim = (new_width, new_height)
        img = cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA)

    grayscale_img = color2gray(img)

    if output_filename is not None:
        cv2.imwrite(output_filename, grayscale_img)

    return grayscale_img


def sepia_image(
    input_filename, output_filename=None, scale=None, backend=None, level=1.0
):
    """
    Applies a sepia filter to an image. May also optionally resize and save the image.

    Arguments:
        input_filename: Filename of the image you wish to apply a filter to
        output_filename: Filename of the output file if you wish to store the transformed image.
            If set to None, the image will not be written to file.
        scale: optional scalefactor to apply to the image prior to applying the filter
        backend: Choose which of the backends to utilize. If None is set, default to Numpy.
        level: Intensity of the sepia filter from 0.0 (no filter) to 1.0 (full intensity).

    Returns:
        sepia_img
    """
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
        new_width = int(img.shape[1] * scale)
        new_height = int(img.shape[0] * scale)
        new_dim = (new_width, new_height)
        img = cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA)

    sepia_img = color2sepia(img, level=level)

    if output_filename is not None:
        # cv2 expects BGR representation, so convert from RGB -> BGR
        sepia_img_BGR = cv2.cvtColor(sepia_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_filename, sepia_img_BGR)

    return sepia_img


def benchmark_grayscale_img(
    input_filename, scale=None, backend=None, level=1.0, num_runs=3
):
    """
    Times the provided implementation on a given image that is optionally downscaled beforehand.

    Arguments:
        input_filename: Filename of the image you wish to apply a filter to
        scale: optional scalefactor to apply to the image prior to applying the filter.
        backend: Choose which of the backends to utilize. If None is set, default to Numpy.
        num_runs: number of times to run the filter algorithm for the benchmark.
    """
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
        new_width = int(img.shape[1] * scale)
        new_height = int(img.shape[0] * scale)
        new_dim = (new_width, new_height)
        img = cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA)

    runtime = (
        timeit.timeit("color2gray(img)", globals=locals(), number=num_runs) / num_runs
    )

    print("Average time over %i runs: %.2e s" % (num_runs, runtime))

    return


def benchmark_sepia_img(
    input_filename, scale=None, backend=None, level=1.0, num_runs=3
):
    """
    Times the provided implementation on a given image that is optionally downscaled beforehand.

    Arguments:
        input_filename: Filename of the image you wish to apply a filter to
        scale: optional scalefactor to apply to the image prior to applying the filter.
        backend: Choose which of the backends to utilize. If None is set, default to Numpy.
        level: Intensity of the sepia filter from 0.0 (no filter) to 1.0 (full intensity).
        num_runs: number of times to run the filter algorithm for the benchmark.
    """

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
        new_width = int(img.shape[1] * scale)
        new_height = int(img.shape[0] * scale)
        new_dim = (new_width, new_height)
        img = cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA)

    runtime = (
        timeit.timeit(
            "color2sepia(img, level=level)", globals=locals(), number=num_runs
        )
        / num_runs
    )

    print("Average time over %i runs: %.2e s" % (num_runs, runtime))

    return
