import numpy as np
import instapy
import python_color2gray
import python_color2sepia
import numpy_color2gray
import numpy_color2sepia
import numba_color2gray
import numba_color2sepia
import cython_color2gray
import cython_color2sepia


def test_grayscale(nrows=200, ncols=200):
    """
    Checks for self-consistency between all 4 implementations of the grayscale filters. First, the shapes
    of the filtered images are checked to be equal. Then, each image is checked to be equal to a tolerance
    of +/- 1 for each pixel value. This tolerance is needed because each implementation may handle the
    lossy double to uint8 cast slightly differently.
    The test is performed on a randomly generated array representation of an RGB image

    Arguments:
        nrows: Number of rows in the randomly generated test image
        ncols: Numeber of columns in the randomly generated test image
    """
    rand_img = np.random.randint(0, 255, size=[nrows, ncols, 3], dtype=np.uint8)
    gs_python = python_color2gray.color2gray(rand_img)
    gs_numpy = numpy_color2gray.color2gray(rand_img)
    gs_numba = numba_color2gray.color2gray(rand_img)
    gs_cython = cython_color2gray.color2gray(rand_img)
    # Ensure that all of the images have the same dimensionality
    assert (
        np.shape(gs_python)
        == np.shape(gs_numpy)
        == np.shape(gs_numba)
        == np.shape(gs_cython)
    )

    np.testing.assert_allclose(gs_python, gs_numpy, atol=1)
    np.testing.assert_allclose(gs_python, gs_numba, atol=1)
    np.testing.assert_allclose(gs_python, gs_cython, atol=1)

    return


def test_sepia(nrows=200, ncols=200):
    """
    Checks for self-consistency between all 4 implementations of the grayscale filters. First, the shapes
    of the filtered images are checked to be equal. Then, each image is checked to be equal to a tolerance
    of +/- 1 for each pixel value. This tolerance is needed because each implementation may handle the
    lossy double to uint8 cast slightly differently.
    The test is performed on a randomly generated array representation of an RGB image

    Arguments:
        nrows: Number of rows in the randomly generated test image
        ncols: Numeber of columns in the randomly generated test image
    """
    rand_img = np.random.randint(0, 255, size=[nrows, ncols, 3], dtype=np.uint8)
    s_python = python_color2sepia.color2sepia(rand_img)
    s_numpy = numpy_color2sepia.color2sepia(rand_img)
    s_numba = numba_color2sepia.color2sepia(rand_img)
    s_cython = cython_color2sepia.color2sepia(rand_img)
    # Ensure that all of the images have the same dimensionality
    assert (
        np.shape(s_python)
        == np.shape(s_numpy)
        == np.shape(s_numba)
        == np.shape(s_cython)
    )

    np.testing.assert_allclose(s_python, s_numpy, atol=1)
    np.testing.assert_allclose(s_python, s_numba, atol=1)
    np.testing.assert_allclose(s_python, s_cython, atol=1)

    return
