import numpy as np
from instapy import *


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
    gs_python = python_color2gray(rand_img)
    gs_numpy = numpy_color2gray(rand_img)
    gs_numba = numba_color2gray(rand_img)
    gs_cython = cython_color2gray(rand_img)
    # Ensure that all of the images have the same dimensionality
    assert (
        np.shape(gs_python)
        == np.shape(gs_numpy)
        == np.shape(gs_numba)
        == np.shape(gs_cython)
    )
    # Use a tolerance of +/- 1 to account for numerical instabilities
    np.testing.assert_allclose(gs_python, gs_numpy, atol=1)
    np.testing.assert_allclose(gs_python, gs_numba, atol=1)
    np.testing.assert_allclose(gs_python, gs_cython, atol=1)

    # Test a random pixel
    i = np.random.randint(0, nrows - 1)
    j = np.random.randint(0, ncols - 1)

    gs_pix = (
        rand_img[i][j][0] * 0.21 + rand_img[i][j][1] * 0.72 + rand_img[i][j][2] * 0.07
    )
    # Tolerance of +/- 1 to account for numerical instabilities
    assert abs(gs_pix - gs_python[i][j]) <= 1
    assert abs(gs_pix - gs_numpy[i][j]) <= 1
    assert abs(gs_pix - gs_numba[i][j]) <= 1
    assert abs(gs_pix - gs_cython[i][j]) <= 1

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
    s_python = python_color2sepia(rand_img)
    s_numpy = numpy_color2sepia(rand_img)
    s_numba = numba_color2sepia(rand_img)
    s_cython = cython_color2sepia(rand_img)
    # Ensure that all of the images have the same dimensionality
    assert (
        np.shape(s_python)
        == np.shape(s_numpy)
        == np.shape(s_numba)
        == np.shape(s_cython)
    )
    # Use a tolerance of +/- 1 to account for numerical instabilities
    np.testing.assert_allclose(s_python, s_numpy, atol=1)
    np.testing.assert_allclose(s_python, s_numba, atol=1)
    np.testing.assert_allclose(s_python, s_cython, atol=1)

    # Test a random pixel
    i = np.random.randint(0, nrows - 1)
    j = np.random.randint(0, ncols - 1)
    # Apply the sepia filter manually to this single pixel
    sepia_pix = np.zeros(3, dtype=np.uint8)
    sepia_matrix = [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]
    for k in range(3):
        pix = 0
        for l in range(3):
            pix += rand_img[i][j][l] * sepia_matrix[k][l]
        # Avoid overflows by truncating above 255
        sepia_pix[k] = min(pix, 255)

    np.testing.assert_allclose(sepia_pix, s_python[i][j][:], atol=1)
    np.testing.assert_allclose(sepia_pix, s_numpy[i][j][:], atol=1)
    np.testing.assert_allclose(sepia_pix, s_numba[i][j][:], atol=1)
    np.testing.assert_allclose(sepia_pix, s_cython[i][j][:], atol=1)

    return
