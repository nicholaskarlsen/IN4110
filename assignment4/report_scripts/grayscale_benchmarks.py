"""
Script that benchmarks and generates the all of the reports for the grayscale filter implementations
"""

import cv2
import numpy as np
import re
import timeit
from instapy import (
    python_color2gray,
    numpy_color2gray,
    numba_color2gray,
    cython_color2gray,
)

IMG_DIR = "../img/"
REPORT_DIR = "../reports/"


def get_runtime_from_report(fn):
    """
    Parses a report file and fetches its runtime with a bit of regex. Looks for something in the form:
    "123.345 s" which will only occur once in each report file.

    Arguments:
        fn: Filename of file to parse

    Returns:
        runtime: Runtime of the implementation from its report file
    """
    # Fetch runtime of pure python implementation by parsing the report
    with open(fn, "r") as file:
        report_str = file.read()  # Store the entire file as a string
    # Expect a floating point number followed by an s. eg: 1337.123 s
    runtime = re.findall(r"\d.\d+ s", report_str)
    # re gives a list. Only interested in the first and only entry
    runtime = runtime[0]
    # split the string to get rid of the trailing "s"
    runtime = runtime.split(" ")[0]
    # finally the string to a flaot
    runtime = float(runtime)
    return runtime


def python_benchmark(num_runs=3):
    image = cv2.imread(IMG_DIR + "rain.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    avg_runtime = (
        timeit.timeit(
            "python_color2gray(image)",
            setup="from instapy import python_color2gray",
            globals=locals(),
            number=num_runs,
        )
        / num_runs
    )

    with open(REPORT_DIR + "python_report_color2gray.txt", "w") as file:
        file.write("Size of image: %ix%i\n" % (image.shape[1], image.shape[0]))
        file.write("Timing: %s\n" % __file__)
        file.write(
            "Average runtime running %s after %i runs: %.6f s\n"
            % (__file__, num_runs, avg_runtime)
        )
        file.write("Timing performed using: timeit\n")
    # Save a copy of the image as a quick "unit test"
    cv2.imwrite(IMG_DIR + "rain_grayscale_python.jpeg", python_color2gray(image))
    return


def numpy_benchmark(num_runs=3):
    image = cv2.imread(IMG_DIR + "rain.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    avg_runtime = (
        timeit.timeit(
            "numpy_color2gray(image)",
            setup="from instapy import numpy_color2gray",
            globals=locals(),
            number=num_runs,
        )
        / num_runs
    )

    with open(REPORT_DIR + "numpy_report_color2gray.txt", "w") as file:
        file.write("Size of image: %ix%i\n" % (image.shape[1], image.shape[0]))
        file.write("Timing: %s\n" % __file__)
        file.write(
            "Average runtime running %s after %i runs: %.6f s\n"
            % (__file__, num_runs, avg_runtime)
        )

        # Fetch runtime of pure python implementation by parsing the report
        python_runtime = get_runtime_from_report(
            REPORT_DIR + "python_report_color2gray.txt"
        )

        file.write("Average runtime running of numpy_color2gray is ")
        if python_runtime > avg_runtime:
            file.write("%.3f times faster " % (python_runtime / avg_runtime))
        else:
            file.write("%.3f times slower" % (avg_runtime / python_runtime))

        file.write("than python_color2gray\n")
        file.write("Timing performed using: timeit\n")

    # Save a copy of the image as a quick "unit test"
    cv2.imwrite(IMG_DIR + "rain_grayscale_numpy.jpeg", numpy_color2gray(image))

    return


def numba_benchmark(num_runs=3):
    image = cv2.imread(IMG_DIR + "rain.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run it once to ensure that its compiled before benchmarking
    _ = numba_color2gray(image)

    avg_runtime = (
        timeit.timeit(
            "numba_color2gray(image)",
            setup="from instapy import numba_color2gray",
            globals=locals(),
            number=num_runs,
        )
        / num_runs
    )

    with open(REPORT_DIR + "numba_report_color2gray.txt", "w") as file:
        file.write("Size of image: %ix%i\n" % (image.shape[1], image.shape[0]))
        file.write("Timing: %s\n" % __file__)
        file.write(
            "Average runtime running %s after %i runs: %.6f s\n"
            % (__file__, num_runs, avg_runtime)
        )

        # Fetch runtime of pure python implementation by parsing the report
        python_runtime = get_runtime_from_report(
            REPORT_DIR + "python_report_color2gray.txt"
        )
        file.write("Average runtime running of numba_color2gray is ")
        if python_runtime > avg_runtime:
            file.write("%.3f times faster " % (python_runtime / avg_runtime))
        else:
            file.write("%.3f times slower" % (avg_runtime / python_runtime))
        file.write("than python_color2gray\n")

        # Fetch runtime of numpy implementation by parsing the report
        numpy_runtime = get_runtime_from_report(
            REPORT_DIR + "numpy_report_color2gray.txt"
        )
        file.write("Average runtime running of numba_color2gray is ")
        if numpy_runtime > avg_runtime:
            file.write("%.3f times faster " % (numpy_runtime / avg_runtime))
        else:
            file.write("%.3f times slower " % (avg_runtime / numpy_runtime))
        file.write("than numpy_color2gray\n")

        file.write("Timing performed using: timeit\n")
        # Add my comment here rather than writing it manually incase i overwrite the file later
        file.write("%s" % "-" * 80)
        file.write(
            """
Comment: In this case, the implementation using Numba and Numby quite similar performance with
Numba winning out by a factor 4. Furthermore, the numba code is literally a copy-paste of the
python implementation and the @njit decorator is responsible for the entirety of the performance
increase. 

In contrast, the numpy implementation required me to re-formulate the computation in a way which 
adheres to the numpy way of doing things. This re-formulation does however also turn out to be
much, much shorter and perhaps more elegant.

Also note that these benchmarks do not take into account the one-time overhead incurred by the Numba
implementation due to its just-in-time compilation which happens the first time the function 
is called.
"""
        )
    # Save a copy of the image as a quick "unit test"
    cv2.imwrite(IMG_DIR + "rain_grayscale_numba.jpeg", numba_color2gray(image))
    return


def cython_benchmark(num_runs=3):
    image = cv2.imread(IMG_DIR + "rain.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    avg_runtime = (
        timeit.timeit(
            "cython_color2gray(image)",
            setup="from instapy import cython_color2gray",
            globals=locals(),
            number=num_runs,
        )
        / num_runs
    )

    with open(REPORT_DIR + "cython_report_color2gray.txt", "w") as file:
        file.write("Size of image: %ix%i\n" % (image.shape[1], image.shape[0]))
        file.write("Timing: %s\n" % __file__)
        file.write(
            "Average runtime running %s after %i runs: %.6f s\n"
            % (__file__, num_runs, avg_runtime)
        )

        # Fetch runtime of pure python implementation by parsing the report
        python_runtime = get_runtime_from_report(
            REPORT_DIR + "python_report_color2gray.txt"
        )
        file.write("Average runtime running of cython_color2gray is ")
        if python_runtime > avg_runtime:
            file.write("%.3f times faster " % (python_runtime / avg_runtime))
        else:
            file.write("%.3f times slower" % (avg_runtime / python_runtime))
        file.write("than python_color2gray\n")

        # Fetch runtime of numpy implementation by parsing the report
        numpy_runtime = get_runtime_from_report(
            REPORT_DIR + "numpy_report_color2gray.txt"
        )
        file.write("Average runtime running of cython_color2gray is ")
        if numpy_runtime > avg_runtime:
            file.write("%.3f times faster " % (numpy_runtime / avg_runtime))
        else:
            file.write("%.3f times slower " % (avg_runtime / numpy_runtime))
        file.write("than numpy_color2gray\n")

        # Fetch runtime of numba implementation by parsing the report
        numba_runtime = get_runtime_from_report(
            REPORT_DIR + "numba_report_color2gray.txt"
        )
        file.write("Average runtime running of cython_color2gray is ")
        if numba_runtime > avg_runtime:
            file.write("%.3f times faster " % (numba_runtime / avg_runtime))
        else:
            file.write("%.3f times slower " % (avg_runtime / numba_runtime))
        file.write("than numba_color2gray\n")

        file.write("Timing performed using: timeit\n")
        # Add my comment here rather than writing it manually incase i overwrite the file later
        file.write("%s" % "-" * 80)
        file.write(
            """
Comment: The Cython code is faster than the pure python implementation, but considerably slower
than the Numpy and most notably, the Numba implementation. I suspect the two may use different compilers
and that the cython code has not been optimized as much.
        """
        )
    # Save a copy of the image as a quick "unit test"
    cv2.imwrite(IMG_DIR + "rain_grayscale_cython.jpeg", cython_color2gray(image))


if __name__ == "__main__":
    python_benchmark()
    numpy_benchmark()
    numba_benchmark()
    cython_benchmark()
