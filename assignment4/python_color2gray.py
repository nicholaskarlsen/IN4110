import numpy as np
import cv2


def color2grey(image, weights=[0.21, 0.72, 0.07]):
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
    N, M, _ = np.shape(image)
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
