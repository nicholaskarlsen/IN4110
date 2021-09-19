from Array import Array
import numpy as np

"""
1-Dimensional tests
"""


def test_str_repr():
    """
    Check that your print function returns the nice string
    """
    vals = (1, 2, 3, 4, 5, 6)
    # Test various shapes, both 1D and 2D
    shape1 = (6,)
    shape2 = (2, 3)
    shape3 = (6, 1)
    # Use numpy as the ground truth
    np_arr = np.array(vals)

    for s in [shape1, shape2, shape3]:
        arr = Array(s, *vals)
        assert arr.__str__() == np_arr.reshape(s).__str__()


def test_1d_addition():
    """
    One or more tests verifying that adding to a 1d-array element-wise returns
    what it’s supposed to
    """
    shape = (6,)
    vals = (4, 8, 15, 16, 23, 42)

    arr_1 = Array(shape, *vals)
    # Test elementwise addition of a single number
    arr_2_l = arr_1 + 10  # left addition
    arr_2_r = 10 + arr_1  # right addition

    for i in range(6):
        assert arr_2_l[i] == vals[i] + 10
        assert arr_2_r[i] == vals[i] + 10

    # Test elementwise addition of an array object
    arr_3_l = arr_1 + arr_2_l  # left addition
    arr_3_r = arr_1 + arr_2_r  # right addition
    for i in range(6):
        assert arr_3_l[i] == (vals[i] + 10) + vals[i]
        assert arr_3_r[i] == (vals[i] + 10) + vals[i]

    return


def test_2d_addition():
    """ 
    One or more tests verifying that adding to a 2d-array element-wise returns
    what it’s supposed to 
    """
    shape = (2, 3)
    vals = (4, 8, 15, 16, 23, 42)
    arr_1 = Array(shape, *vals)

    # Test elementwise addition of a single number
    arr_l_int = arr_1 + 10  # left addition
    arr_r_int = 10 + arr_1  # right addition

    # Test elementwise addition of a single number, both left and right
    # use numpy as the ground truth
    ground_truth = np.array(vals).reshape(shape) + 10

    for i in range(2):
        for j in range(3):
            assert arr_l_int[i][j] == ground_truth[i][j]
            assert arr_r_int[i][j] == ground_truth[i][j]

    # Test elementwise addition of an array, both left and right
    vals2 = (-6, 9, 4, 2, 0, 42)
    arr_2 = Array(shape, *vals2)

    arr_l_arr = arr_1 + arr_2
    arr_r_arr = arr_2 + arr_1

    ground_truth = np.array(vals).reshape(shape) + np.array(vals2).reshape(shape)
    for i in range(2):
        for j in range(3):
            assert arr_l_arr[i][j] == ground_truth[i][j]
            assert arr_r_arr[i][j] == ground_truth[i][j]

    return


def test_1d_subtraction():
    """
    One or more tests verifying that substracting from a 1d-array element-
    wise returns what it’s supposed to
    """
    shape = (9,)
    vals = (-4, -3, -2, -1, 0, 1, 2, 3, 4)

    arr_1 = Array(shape, *vals)
    # Test elementwise subtraction of a single number
    arr_2_l = arr_1 - 10  # left subtraction
    arr_2_r = 10 - arr_1  # right subtraction

    for i in range(9):
        assert arr_2_l[i] == vals[i] - 10
        assert arr_2_r[i] == 10 - vals[i]

    # Test elementwise subtraction of an array object
    arr_3_l = arr_1 - arr_2_l
    arr_3_r = arr_2_r - arr_1
    for i in range(9):
        assert arr_3_l[i] == vals[i] - (vals[i] - 10)
        assert arr_3_r[i] == (10 - vals[i]) - vals[i]

    return

def test_2d_subtraction():
    """
    One or more tests verifying that substracting from a 2d-array element-
    wise returns what it’s supposed to
    """
    shape = (2, 3)
    vals = (4, 8, 15, 16, 23, 42)
    arr_1 = Array(shape, *vals)

    # Test elementwise addition of a single number
    arr_l_int = arr_1 - 10  # left addition
    arr_r_int = 10 - arr_1  # right addition

    # Test elementwise addition of a single number, both left and right
    # use numpy as the ground truth
    ground_truth_l = np.array(vals).reshape(shape) - 10
    ground_truth_r = 10 - np.array(vals).reshape(shape)

    for i in range(2):
        for j in range(3):
            assert arr_l_int[i][j] == ground_truth_l[i][j]
            assert arr_r_int[i][j] == ground_truth_r[i][j]

    # Test elementwise addition of an array, both left and right
    vals2 = (-6, 9, 4, 2, 0, 42)
    arr_2 = Array(shape, *vals2)

    arr_l_arr = arr_1 - arr_2
    arr_r_arr = arr_2 - arr_1

    ground_truth_l = np.array(vals).reshape(shape) - np.array(vals2).reshape(shape)
    ground_truth_r = np.array(vals2).reshape(shape) - np.array(vals).reshape(shape)
    for i in range(2):
        for j in range(3):
            assert arr_l_arr[i][j] == ground_truth_l[i][j]
            assert arr_r_arr[i][j] == ground_truth_r[i][j]

    return


def test_1d_multiplication():
    """
    One or more tests verifying that multiplying a 1d-array element-wise by
    a factor or other 1-d array returns what it’s supposed to
    """
    shape = (9,)
    vals = (-4, -3, -2, -1, 0, 1, 2, 3, 4)

    arr_1 = Array(shape, *vals)
    # Test elementwise multiplication of a single number
    arr_2_l = arr_1 * 10  # left multiplication
    arr_2_r = 10 * arr_1  # right multiplication

    for i in range(9):
        assert arr_2_l[i] == vals[i] * 10
        assert arr_2_r[i] == 10 * vals[i]

    # Test elementwise multiplication of an array object
    arr_3_l = arr_1 * arr_2_l
    arr_3_r = arr_2_r * arr_1
    for i in range(9):
        assert arr_3_l[i] == (vals[i] * 10) * vals[i]
        assert arr_3_r[i] == (vals[i] * 10) * vals[i]

    return

def test_2d_multiplication():
    """ 
    One or more tests verifying that multiplying  a 2d-array element-wise returns
    what it’s supposed to 
    """
    shape = (2, 3)
    vals = (4, 8, 15, 16, 23, 42)
    arr_1 = Array(shape, *vals)

    # Test elementwise addition of a single number
    arr_l_int = arr_1 * 10  # left addition
    arr_r_int = 10 * arr_1  # right addition

    # Test elementwise addition of a single number, both left and right
    # use numpy as the ground truth
    ground_truth = np.array(vals).reshape(shape) * 10

    for i in range(2):
        for j in range(3):
            assert arr_l_int[i][j] == ground_truth[i][j]
            assert arr_r_int[i][j] == ground_truth[i][j]

    # Test elementwise addition of an array, both left and right
    vals2 = (-6, 9, 4, 2, 0, 42)
    arr_2 = Array(shape, *vals2)

    arr_l_arr = arr_1 * arr_2
    arr_r_arr = arr_2 * arr_1

    ground_truth = np.array(vals).reshape(shape) * np.array(vals2).reshape(shape)
    for i in range(2):
        for j in range(3):
            assert arr_l_arr[i][j] == ground_truth[i][j]
            assert arr_r_arr[i][j] == ground_truth[i][j]

    return


def test_comparison_operator_1d():
    """
    One or more tests verifying that comparing arrays (by ==) returns what
    it is supposed to - which should be a boolean. Performs tests for 1D arrays
    """
    # The main array 
    arr_1 = Array((4,), 1, 2, 3, 4) 

    # Identical to the main array
    arr_2 = Array((4,), 1, 2, 3, 4)  

    # different compared to the main array
    arr_3 = Array((4,), 1, 2, 1337, 4)  
    arr_4 = Array((5,), 1, 2, 3, 4, 5)  

    assert arr_1 == arr_2
    assert arr_1 != arr_3
    assert arr_1 != arr_4
    return

def test_comparison_operator_2d():
    """
    One or more tests verifying that comparing arrays (by ==) returns what
    it is supposed to - which should be a boolean. Performs tests for 2D arrays
    """
    # The main array 
    arr_1 = Array((2,2), 1, 2, 3, 4) 

    # Identical to the main array
    arr_2 = Array((2,2), 1, 2, 3, 4)  

    # different compared to the main array
    arr_3 = Array((2,2), 1, 2, 1337, 4)  
    arr_4 = Array((5,1), 1, 2, 3, 4, 5)  

    assert arr_1 == arr_2
    assert arr_1 != arr_3
    assert arr_1 != arr_4
    return


def test_is_equal_1d():
    """
    One or more tests verifying that comparing a 1d-array element-wise to
    another array through is equal returns what it’s supposed to - which
    should be a boolean array. Treats the output of an equivalent Numpy function
    as the ground truth.
    """
    vals1 = (4, 8, 15, 16, 23, 42)
    arr1 = Array((6,), *vals1)

    # Test is_equal for a single number
    equal_arr_num = arr1.is_equal(15)
    ground_truth = np.equal(np.array(vals1), 15)
    for i in range(6):
        assert equal_arr_num[i] == ground_truth[i]

    # Test is_equal for two arrays
    vals2 = (0, 8, 2, 16, 23, 0)
    arr2 = Array((6,), *vals2)
    equal_arr_arr = arr1.is_equal(arr2)
    ground_truth = np.equal(np.array(vals1), np.array(vals2))

    for i in range(6):
        assert equal_arr_arr[i] == ground_truth[i]

    return

def test_is_equal_2d():
    """
    One or more tests verifying that comparing a 2d-array element-wise to
    another array through is equal returns what it’s supposed to - which
    should be a boolean array. Treats the output of an equivalent Numpy function
    as the ground truth.
    """
    shape = (2,3)
    vals1 = (4, 8, 15, 16, 23, 42)
    arr1 = Array(shape, *vals1)

    # Test is_equal for a single number
    equal_arr_num = arr1.is_equal(15)
    ground_truth = np.equal(np.array(vals1).reshape(shape), 15)
    for i in range(2):
        for j in range(3):
            assert equal_arr_num[i][j] == ground_truth[i][j]

    # Test is_equal for two arrays
    vals2 = (0, 8, 2, 16, 23, 0)
    arr2 = Array(shape, *vals2)
    equal_arr_arr = arr1.is_equal(arr2)
    ground_truth = np.equal(np.array(vals1).reshape(shape), np.array(vals2).reshape(shape))

    for i in range(2):
        for j in range(3):
            assert equal_arr_arr[i][j] == ground_truth[i][j]

    return


def test_min_element_1d():
    """
    One or more tests verifying that the the element returned by min element
    is the ”smallest” one in the array for a selection of 1D arrays
    """
    arr_1 = Array((4,), 4, 2, 1, 3)  # Only positive values
    arr_2 = Array((5,), 1, 5, 0, 6, 100)  # Only positive values and zero
    arr_3 = Array((4,), 1, -2, 5, 2)  # Positive and negative values
    arr_4 = Array((4,), 1, -2, 0, 5)  # Positive and negative values and zero
    arr_5 = Array((4,), -2, -99, 0, -2)  # Negative values and zero
    arr_6 = Array((4,), -4, -1231, -2, -6)  # Only negative values

    assert arr_1.min_element() == 1
    assert arr_2.min_element() == 0
    assert arr_3.min_element() == -2
    assert arr_4.min_element() == -2
    assert arr_5.min_element() == -99
    assert arr_6.min_element() == -1231

    return

def test_min_element_2d():
    """
    One or more tests verifying that the the element returned by min element
    is the ”smallest” one in the array for a selection of 2D arrays
    """
    arr_1 = Array((2,2), 4, 2, 1, 3)  # Only positive values
    arr_2 = Array((5,1), 1, 5, 0, 6, 100)  # Only positive values and zero
    arr_3 = Array((2,2), 1, -2, 5, 2)  # Positive and negative values
    arr_4 = Array((2,2), 1, -2, 0, 5)  # Positive and negative values and zero
    arr_5 = Array((2,2), -2, -99, 0, -2)  # Negative values and zero
    arr_6 = Array((2,2), -4, -1231, -2, -6)  # Only negative values

    assert arr_1.min_element() == 1
    assert arr_2.min_element() == 0
    assert arr_3.min_element() == -2
    assert arr_4.min_element() == -2
    assert arr_5.min_element() == -99
    assert arr_6.min_element() == -1231
