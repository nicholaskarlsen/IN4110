import numpy as np
import time
import timeit

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
        if ((array[i][0] >= 0.52)
            and (array[i][1] >= 0.88)
            and (array[i][0] <= 0.6)
            and (array[i][1] <= 0.96)):
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
        if (((array[i][0] >= 0.16)
            and (array[i][1] >= 0.16)
            and (array[i][0] <= 0.24)
            and (array[i][1] <= 0.24))
            #2nd square
            or 
            ((array[i][0] >= 0.28)
            and (array[i][1] >= 0.16)
            and (array[i][0] <= 0.36)
            and (array[i][1] <= 0.24))
            #3nd square
            or ((array[i][0] >= 0.4)
            and (array[i][1] >= 0.16)
            and (array[i][0] <= 0.48)
            and (array[i][1] <= 0.24))
            #4th square
            or ((array[i][0] >= 0.4)
            and (array[i][1] >= 0.28)
            and (array[i][0] <= 0.48)
            and (array[i][1] <= 0.36))
            #5th square
            or ((array[i][0] >= 0.52)
            and (array[i][1] >= 0.28)
            and (array[i][0] <= 0.6)
            and (array[i][1] <= 0.36))
            #5th square
            or ((array[i][0] >= 0.52)
            and (array[i][1] >= 0.4)
            and (array[i][0] <= 0.6)
            and (array[i][1] <= 0.48))
            #6th square
            or ((array[i][0] >= 0.52)
            and (array[i][1] >= 0.52)
            and (array[i][0] <= 0.6)
            and (array[i][1] <= 0.6))
            
            #6th square
            or ((array[i][0] >= 0.52)
            and (array[i][1] >= 0.64)
            and (array[i][0] <= 0.6)
            and (array[i][1] <= 0.72))):
            filtered_list.append(array[i])
    return np.array(filtered_list)


if __name__ == '__main__':
    # Benchmark the code by running each function num_runs times
    num_runs = 10
    benchmarks = {
        "array" : np.empty(num_runs, dtype=np.float64),
        "filtered_array" : np.empty(num_runs, dtype=np.float64),
        "filtered_array_snack" : np.empty(num_runs, dtype=np.float64)
    }

    # Perform the benchmarks manually by using pythons time module
    for i in range(num_runs):
        t0 = time.time()
        array = random_array(1e5)
        benchmarks["array"][i] = time.time() - t0

        t0 = time.time()
        filtered_array = snake_loop(array)
        benchmarks["filtered_array"][i] = time.time() - t0

        t0 = time.time()
        filtered_array_snack = loop(array)
        benchmarks["filtered_array_snack"][i] = time.time() - t0

    # Write the results to file
    outfile = open("reports/manual_report.txt", "w")
    outfile.write("Benchmark of functions in %s\n" % __file__)
    outfile.write("Number of runs: %i\n" % num_runs)
    # Compute the mean runtime for each function
    for key in benchmarks.keys():
        outfile.write("%20s %6.3f s\n" % (key, np.mean(benchmarks[key])))

    # Perform the same benchmark using timeit
    outfile.write("\nTiming of the slowest function using timeit:\n")
    outfile.write( "%20s %6.3f" % ("snake_loop", timeit.timeit("snake_loop(array)", globals=locals(), number = num_runs) /  num_runs))

    #if running in a jupyter notebook you might this inline
    # Measure code execution with inline magic (Jupyter Notebook)
    #print('Loop:\t', end='')
    #timeit loop(array)

    """
    # Plot the results
    import matplotlib.pyplot as plt

    #if running in a jupyter notebook you might this inline
    #matplotlib inline

    plt.figure(figsize=(10, 10))
    plt.title('Plot of Your Filters')
    plt.plot(array[:, 0], array[:, 1], 'k.')
    plt.plot(filtered_array[:, 0], filtered_array[:, 1], 'g.')
    plt.plot(filtered_array_snack[:, 0], filtered_array_snack[:, 1], 'r.')
    plt.show()
    """