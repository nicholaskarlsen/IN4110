import numpy as np


def color2grey(image, weights=np.array([0.21, 0.72, 0.07])):
    """Performs a contraction of an RGB image to greyscale. The contraction is performed using a set of
    weights which may be optionally changed by the user.

    In this implementation, the computations are performed as a tensor contraction o Numpy arrays.
    The contraction being performed written out more clearly in maths notation:
    grayscale_image_{i,j} = image_{i,j,k} weights_k
    where repeated indices are summed over (einstein notation)

    Arguments:
        image: Representation of an RGB image with shape (N,M,3) and integer entries in the interval [0,255]
        weights: Weights to used in summation when contracting the RGB layer to greyscale

    Returns:
        Representation of a greyscale image with shape (N,M) and integer entries in the interval [0,255]
    """
    return np.tensordot(image, weights, axes=(2, 0)).astype("uint8")
    # Alternative, equivalent and longer implementation using slicing incase its "required" that
    # we use slicing as mentioned the assignment text.
    # G = np.zeros(image.shape[:2])
    # G += image[:, :, 0] * weights[0]
    # G += image[:, :, 1] * weights[1]
    # G += image[:, :, 2] * weights[2]
    # return G.astype("uint8")


if __name__ == "__main__":
    import timeit
    import cv2
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

        file.write("Average runtime running of numpy_color2gray is ")
        if python_runtime > avg_runtime:
            file.write("%.3f times faster " % (python_runtime / avg_runtime))
        else:
            file.write("%.3f times slower" % (avg_runtime / python_runtime))

        file.write("than python_color2gray\n")
        file.write("Timing performed using: timeit\n")

    # Save a copy of the image as a quick "unit test"
    cv2.imwrite("img/rain_grayscale_numpy.jpeg", color2grey(image))
