import instapy
import numpy as np

def test_grayscale(test_img = "img/rain.jpg", ntrials=10):
    gs_python = instapy.grayscale_image(test_img, backend="python")
    gs_numpy = instapy.grayscale_image(test_img, backend="numpy")
    gs_numba = instapy.grayscale_image(test_img, backend="numba")
    gs_cython = instapy.grayscale_image(test_img, backend="cython")

    # Ensure that all of the images have the same dimensionality
    assert  np.shape(gs_python) == np.shape(gs_numpy) == np.shape(gs_numba) == np.shape(gs_cython)

    nrows, ncols = np.shape(gs_python)
    for i in np.random.choice(range(nrows), size=ntrials, replace=False):
        for j in np.random.choice(range(ncols), size=ntrials, replace=False):
            assert gs_python[i][j] == gs_numpy[i][j] 
            assert gs_python[i][j] == gs_numba[i][j] 
            assert gs_python[i][j] == gs_cython[i][j]

    return
