import cv2
import numpy as np
import matplotlib.pyplot as plt


def grayscale_np(image, weights=np.array([0.21, 0.72, 0.07])):
    """An RGB image (I) may be loosely thought of as a rank-3 tensor.
    Thus, to produce a black-white image (G), a rank-2 tensor we may perform a tensor contraction
    with the set of weights (W) in the following way;
        G[i][j] = I[i,j,k] * W[k]
    Where the Einstein summation convention is adopted, and repeated indices (k) are summed over.

    This computation is thus very efficiently implemented using the einsum functionality in numpy.
    """
    return np.einsum("ijk,k->ij", image, weights).astype("uint8")


# cv2.imwrite("rain_grayscale.jpeg", grayscale_np(image))

# from cython_color2gray import *
import cython_color2gray
import re
import timeit

image = cv2.imread("img/rain.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# print(cython_impl.color2gray(image.astype("uint8")))

num_runs = 3
avg_runtime = (
    timeit.timeit(
        "cython_color2gray.color2gray(image)", globals=locals(), number=num_runs
    )
    / num_runs
)

with open("reports/cython_report_color2gray.txt", "w") as file:
    file.write("Size of image: %ix%i\n" % (image.shape[1], image.shape[0]))
    file.write("Timing: %s\n" % __file__)
    file.write(
        "Average runtime running %s after %i runs: %.6f s\n"
        % (__file__, num_runs, avg_runtime)
    )

    # Fetch runtime of pure python implementation by parsing the report
    with open("reports/python_report_color2gray.txt", "r") as pfile:
        python_report_str = pfile.read()  # Store the entire file as a string
    # Expect a floating point number followed by an s. eg: 1337.123 s
    python_runtime = re.findall(r"\d.\d+ s", python_report_str)
    # re gives a list. Only interested in the first and only entry
    python_runtime = python_runtime[0]
    # split the string to get rid of the trailing "s"
    python_runtime = python_runtime.split(" ")[0]
    # finally the string to a flaot
    python_runtime = float(python_runtime)

    file.write("Average runtime running of cython_color2gray is ")
    if python_runtime > avg_runtime:
        file.write("%.3f times faster " % (python_runtime / avg_runtime))
    else:
        file.write("%.3f times slower" % (avg_runtime / python_runtime))
    file.write("than python_color2gray\n")

    # Fetch runtime of numpy implementation by parsing the report
    with open("reports/numpy_report_color2gray.txt", "r") as pfile:
        python_report_str = pfile.read()  # Store the entire file as a string
    # Same as above, except in a dense, single line to save space.
    python_runtime = float(re.findall(r"\d.\d+ s", python_report_str)[0].split(" ")[0])

    file.write("Average runtime running of cython_color2gray is ")
    if python_runtime > avg_runtime:
        file.write("%.3f times faster " % (python_runtime / avg_runtime))
    else:
        file.write("%.3f times slower " % (avg_runtime / python_runtime))
    file.write("than numpy_color2gray\n")

    # Fetch runtime of numba implementation by parsing the report
    with open("reports/numba_report_color2gray.txt", "r") as pfile:
        python_report_str = pfile.read()  # Store the entire file as a string
    # Same as above, except in a dense, single line to save space.
    python_runtime = float(re.findall(r"\d.\d+ s", python_report_str)[0].split(" ")[0])

    file.write("Average runtime running of cython_color2gray is ")
    if python_runtime > avg_runtime:
        file.write("%.3f times faster " % (python_runtime / avg_runtime))
    else:
        file.write("%.3f times slower " % (avg_runtime / python_runtime))
    file.write("than numba_color2gray\n")

    file.write("Timing performed using: timeit\n")
    # Add my comment here rather than writing it manually incase i overwrite the file later
    file.write("%s" % "-" * 80)
    file.write(
        """
Comment: 
    """
    )

# Save a copy of the image as a quick "unit test"
cv2.imwrite("img/rain_grayscale_cython.jpeg", cython_color2gray.color2gray(image))
