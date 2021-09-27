import numpy as np
import time
import timeit

REPORT_DIR = "../reports/"

def random_array(size, dim=3):
    """
    Generate a random array of size size and dimension dim
    """
    return np.random.rand(int(size), dim)


def loop(array):
    """
    Takes a numpy array and isolates all points that are within [0.52,0.6]
    for the first column and between [0.88,0.96] for the second column by
    looping through every point.
    """
    filtered_list = []
    for i in range(len(array)):
        # Check if the point is within the rectangle
        if (
            (array[i][0] >= 0.52)
            and (array[i][1] >= 0.88)
            and (array[i][0] <= 0.6)
            and (array[i][1] <= 0.96)
        ):
            filtered_list.append(array[i])
    return np.array(filtered_list)


def snake_loop(array):
    """
    Takes a numpy array and isolates all points in a given
    range via array indexing by
    looping through every point.
    """
    filtered_list = []
    for i in range(len(array)):
        # Check if the point is within the rectangle
        if (
            (
                (array[i][0] >= 0.16)
                and (array[i][1] >= 0.16)
                and (array[i][0] <= 0.24)
                and (array[i][1] <= 0.24)
            )
            # 2nd square
            or (
                (array[i][0] >= 0.28)
                and (array[i][1] >= 0.16)
                and (array[i][0] <= 0.36)
                and (array[i][1] <= 0.24)
            )
            # 3nd square
            or (
                (array[i][0] >= 0.4)
                and (array[i][1] >= 0.16)
                and (array[i][0] <= 0.48)
                and (array[i][1] <= 0.24)
            )
            # 4th square
            or (
                (array[i][0] >= 0.4)
                and (array[i][1] >= 0.28)
                and (array[i][0] <= 0.48)
                and (array[i][1] <= 0.36)
            )
            # 5th square
            or (
                (array[i][0] >= 0.52)
                and (array[i][1] >= 0.28)
                and (array[i][0] <= 0.6)
                and (array[i][1] <= 0.36)
            )
            # 5th square
            or (
                (array[i][0] >= 0.52)
                and (array[i][1] >= 0.4)
                and (array[i][0] <= 0.6)
                and (array[i][1] <= 0.48)
            )
            # 6th square
            or (
                (array[i][0] >= 0.52)
                and (array[i][1] >= 0.52)
                and (array[i][0] <= 0.6)
                and (array[i][1] <= 0.6)
            )
            # 6th square
            or (
                (array[i][0] >= 0.52)
                and (array[i][1] >= 0.64)
                and (array[i][0] <= 0.6)
                and (array[i][1] <= 0.72)
            )
        ):
            filtered_list.append(array[i])
    return np.array(filtered_list)


if __name__ == "__main__":
    # Benchmark the code by running each function num_runs times
    num_runs = 5
    # Write the results to file
    with open(REPORT_DIR + "timeit_report.txt", "w") as outfile:
        outfile.write("timeit becnhmarks of functions in %s\n" % __file__)
        outfile.write("Number of runs: %i\n\n" % num_runs)

        array = random_array(2e6)

        outfile.write(
            "%30s %10.4f s\n"
            % (
                "array = random_array(2e6)",
                timeit.timeit("random_array(2e6)", globals=locals(), number=num_runs)
                / num_runs,
            )
        )
        outfile.write(
            "%30s %10.4f s\n"
            % (
                "snake_loop(array)",
                timeit.timeit("snake_loop(array)", globals=locals(), number=num_runs)
                / num_runs,
            )
        )
        outfile.write(
            "%30s %10.4f s\n"
            % (
                "loop(array)",
                timeit.timeit("loop(array)", globals=locals(), number=num_runs)
                / num_runs,
            )
        )

        # Add my comment here rather than writing it manually incase i overwrite the file later
        outfile.write("%s" % "-" * 80)
        outfile.write("\nComment: ")
        outfile.write(
            "The timings from timeit and my manual implementation look to be equivalent\n"
        )
        outfile.write(
            "where the slight difference can more than likely be attributed to the variance\n"
        )
        outfile.write(
            "of the measurements rather than a poor implementation on my part."
        )
