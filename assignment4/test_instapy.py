import instapy
import numpy as np

def test_grayscale(test_img = "img/rain.jpg"):
    gs_python = instapy.grayscale_image(test_img, backend="python")
    gs_numpy = instapy.grayscale_image(test_img, backend="numpy")
    gs_numba = instapy.grayscale_image(test_img, backend="numba")
    gs_cython = instapy.grayscale_image(test_img, backend="cython")

    # Ensure that all of the images have the same dimensionality
    assert  np.shape(gs_python) == np.shape(gs_numpy) == np.shape(gs_numba) == np.shape(gs_cython)

    nrows, ncols = np.shape(gs_python)
    for i in range(nrows):
        for j in range(ncols):
            assert gs_python[i][j] == gs_numpy[i][j] 
            assert gs_python[i][j] == gs_numba[i][j] 
            assert gs_python[i][j] == gs_cython[i][j]

    return


def test_sepia(test_img = "img/rain.jpg"):
    s_python = instapy.sepia_image(test_img, backend="python")
    s_numpy = instapy.sepia_image(test_img, backend="numpy")
    s_numba = instapy.sepia_image(test_img, backend="numba")
    s_cython = instapy.sepia_image(test_img, backend="cython")

    # Ensure that all of the images have the same dimensionality
    assert  np.shape(s_python) == np.shape(s_numpy) == np.shape(s_numba) == np.shape(s_cython)

    nrows, ncols, _ = np.shape(s_python)
    for i in range(nrows):
        for j in range(ncols):
            for k in range(3):
                assert s_python[i][j][k] == s_numpy[i][j][k]
                assert s_python[i][j][k] == s_numba[i][j][k]
                assert s_python[i][j][k] == s_cython[i][j][k]

    return