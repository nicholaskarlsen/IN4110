import numpy as np
import cProfile
from contextlib import redirect_stdout


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
    num_runs = 10
    # Write the results to file
    with open("reports/cProfile_report.txt", "w") as outfile:
        # Re-direct stdout to a file to capture the output of print_stats()
        with redirect_stdout(outfile):
            outfile.write("cProfile profiling of functions in %s\n" % __file__)
            outfile.write("%s" % "-" * 80)
            outfile.write("\nProfiling line: array = random_array(2e6)\n\n")

            pr = cProfile.Profile()
            res = pr.run("array = random_array(2e6)")
            res.print_stats(sort="time")

            outfile.write("%s" % "-" * 80)
            outfile.write("\nProfiling line: snake_loop(array)\n\n")
            pr = cProfile.Profile()
            res = pr.run("snake_loop(array)")
            res.print_stats(sort="time")

            outfile.write("%s" % "-" * 80)
            outfile.write("\nProfiling line: loop(array)\n\n")
            pr = cProfile.Profile()
            res = pr.run("loop(array)")
            res.print_stats(sort="time")

            # Add my comment here rather than writing it manually incase i overwrite the file later
            outfile.write("%s" % "-" * 80)
            outfile.write("\nComment: ")
            outfile.write(
                "Timing corresponds to both timeit and my manual implementation.\n"
            )
