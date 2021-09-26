import numpy as np


def color2grey(image, weights=np.array([0.21, 0.72, 0.07])):
    """Performs a contraction of an RGB image to greyscale. The contraction is performed using a set of
    weights which may be optionally changed by the user.

    In this implementation, the computations are performed as vector operations on Numpy arrays.

    Arguments:
        image: Representation of an RGB image with shape (N,M,3) and integer entries in the interval [0,255]
        weights: Weights to used in summation when contracting the RGB layer to greyscale

    Returns:
        G: Representation of a greyscale image with shape (N,M) and integer entries in the interval [0,255]
    """
    G = np.zeros(image.shape[:2])
    G += image[:, :, 0] * weights[0]
    G += image[:, :, 1] * weights[1]
    G += image[:, :, 2] * weights[2]
    return G.astype("uint8")


if __name__ == "__main__":
    import timeit
    import cv2

    image = cv2.imread("img/rain.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    num_runs = 3
    avg_runtime = (
        timeit.timeit("color2grey(image)", globals=locals(), number=num_runs) / num_runs
    )

    with open("reports/%s_report_color2gray.txt" % __file__.split("_")[0], "w") as file:
        file.write("Timing: %s\n" % __file__)
        file.write(
            "Average runtime running %s after %i runs: %.3e s\n"
            % (__file__, num_runs, avg_runtime)
        )
        file.write("Timing performed using: timeit\n")
