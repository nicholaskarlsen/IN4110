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
    benchmarks = {
        "array = random_array(2e6)": np.empty(num_runs, dtype=np.float64),
        "snake_loop(array)": np.empty(num_runs, dtype=np.float64),
        "loop(array)": np.empty(num_runs, dtype=np.float64),
    }

    # Perform the benchmarks manually by using pythons time module
    for i in range(num_runs):
        t0 = time.time()
        array = random_array(2e6)
        benchmarks["array = random_array(2e6)"][i] = time.time() - t0

        t0 = time.time()
        filtered_array = snake_loop(array)
        benchmarks["snake_loop(array)"][i] = time.time() - t0

        t0 = time.time()
        filtered_array_snack = loop(array)
        benchmarks["loop(array)"][i] = time.time() - t0

    # Write the results to file
    with open(REPORT_DIR + "manual_report.txt", "w") as outfile:
        outfile.write("Manual becnhmark of functions in %s\n" % __file__)
        outfile.write("Number of runs: %i\n\n" % num_runs)
        # Compute the mean runtime for each function
        for key in benchmarks.keys():
            outfile.write("%30s %10.4f s\n" % (key, np.mean(benchmarks[key])))

        # Add my comment here rather than writing it manually incase i overwrite the file later
        outfile.write("%s" % "-" * 80)
        outfile.write("\nComment: ")
        outfile.write("We observe that snake_loop is the slowest function")
