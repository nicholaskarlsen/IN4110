import numpy as np
import cv2
from numba import njit


@njit
def color2grey(image, weights=np.array([0.21, 0.72, 0.07])):
    """Performs a contraction of an RGB image to greyscale. The contraction is performed using a set of
    weights which may be optionally changed by the user.

    In this implementation, all computations are performed in pure python, and Numpy arrays are only used to
    store the data.

    Arguments:
        image: Representation of an RGB image with shape (N,M,3) and integer entries in the interval [0,255]
        weights: Weights to used in summation when contracting the RGB layer to greyscale

    Returns:
        G: Representation of a greyscale image with shape (N,M) and integer entries in the interval [0,255]
    """
    N, M, _ = image.shape
    # Initialize an empty array to store the black-white image. Entries may be non-zero!
    G = np.empty(shape=(N, M), dtype="uint8")
    for i in range(N):
        for j in range(M):
            G[i][j] = 0
            for k in range(3):
                G[i][j] += image[i][j][k] * weights[k]
    return G


if __name__ == "__main__":
    import timeit
    import re

    image = cv2.imread("img/rain.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    num_runs = 100
    avg_runtime = (
        timeit.timeit("color2grey(image)", globals=locals(), number=num_runs) / num_runs
    )

    with open("reports/%s_report_color2gray.txt" % __file__.split("_")[0], "w") as file:
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

        file.write("Average runtime running of numba_color2gray is ")
        if python_runtime > avg_runtime:
            file.write("%.3f times faster " % (python_runtime / avg_runtime))
        else:
            file.write("%.3f times slower" % (avg_runtime / python_runtime))
        file.write("than python_color2gray\n")

        # Fetch runtime of numpy implementation by parsing the report
        with open("reports/numpy_report_color2gray.txt", "r") as pfile:
            python_report_str = pfile.read()  # Store the entire file as a string
        # Same as above, except in a dense, single line to save space.
        python_runtime = float(
            re.findall(r"\d.\d+ s", python_report_str)[0].split(" ")[0]
        )

        file.write("Average runtime running of numba_color2gray is ")
        if python_runtime > avg_runtime:
            file.write("%.3f times faster " % (python_runtime / avg_runtime))
        else:
            file.write("%.3f times slower " % (avg_runtime / python_runtime))
        file.write("than numpy_color2gray\n")

        file.write("Timing performed using: timeit\n")
        # Add my comment here rather than writing it manually incase i overwrite the file later
        file.write("%s" % "-" * 80)
        file.write(
            """
Comment: In this case, the implementation using Numba and Numby quite similar performance with
Numpy winning out by a factor 2. However, the numba code is literally a copy-paste of the
python implementation and the @njit decorator is responsible for the entirety of the performance
increase. 

In contrast, the numpy implementation required me to re-formulate the computation in a way which 
adheres to the numpy way of doing things. 

However, in this case numpy also offers the most elegant solution to the problem, requiring only 
a single line of code.
"""
        )

    # Save a copy of the image as a quick "unit test"
    cv2.imwrite("img/rain_grayscale_numba.jpeg", color2grey(image))
