from Array import Array

"""
1-Dimensional tests
"""

def test_str_repr():
    """
    Check that your print function returns the nice string
    """
    arr = Array((4,), 1, 2, 3, 4)
    # The expected output of the to-string method in the Array class
    arr_str = "[1, 2, 3, 4]"
    assert arr_str == arr.__str__()

def test_1d_addition():
    """
    One or more tests verifying that adding to a 1d-array element-wise returns
    what it’s supposed to
    """
    shape = (9,)
    vals = (-4, -3, -2, -1, 0, 1, 2, 3, 4)

    arr_1 = Array(shape, *vals)
    # Test elementwise addition of a single number
    arr_2_l = arr_1 + 10 # left addition
    arr_2_r = 10 + arr_1 # right addition

    for i in range(9):
        assert arr_2_l[i] == vals[i] + 10
        assert arr_2_r[i] == vals[i] + 10

    # Test elementwise addition of an array object
    arr_3_l = arr_1 + arr_2_l # left addition
    arr_3_r = arr_1 + arr_2_r # right addition
    for i in range(9):
        assert arr_3_l[i] == (vals[i] + 10) + vals[i]
        assert arr_3_r[i] == (vals[i] + 10) + vals[i]

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
    arr_2_l = arr_1 - 10 # left subtraction 
    arr_2_r = 10 - arr_1 # right subtraction

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

def test_1d_multiplication():
    """
    One or more tests verifying that multiplying a 1d-array element-wise by
    a factor or other 1-d array returns what it’s supposed to
    """
    shape = (9,)
    vals = (-4, -3, -2, -1, 0, 1, 2, 3, 4)

    arr_1 = Array(shape, *vals)
    # Test elementwise multiplication of a single number
    arr_2_l = arr_1 * 10 # left multiplication 
    arr_2_r = 10 * arr_1 # right multiplication 

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

def test_comparrison_operator():
    """
    One or more tests verifying that comparing arrays (by ==) returns what
    it is supposed to - which should be a boolean.
    """
    arr_1 = Array((4,), 1, 2, 3, 4)     # The main array
    arr_2 = Array((4,), 1, 2, 3, 4)     # Identical to the main array
    arr_3 = Array((4,), 1, 2, 1337, 4)  # Has one different element compared to the main array
    arr_4 = Array((5,), 1, 2, 3, 4, 5)  # Has different shape to the main array (but first elements are identical)

    assert arr_1 == arr_2
    assert arr_1 != arr_3
    assert arr_1 != arr_4
    return

def test_is_equal():
    """
    One or more tests verifying that comparing a 1d-array element-wise to
    another array through is equal returns what it’s supposed to - which
    should be a boolean array.
    """
    pass

def test_min_element():
    """
    One or more tests verifying that the the element returned by min element
    is the ”smallest” one in the array
    """
    arr_1 = Array((4,), 4, 2, 1, 3)         # Only positive values
    arr_2 = Array((5,), 1, 5, 0, 6, 100)    # Only positive values and zero
    arr_3 = Array((4,), 1, -2, 5, 2)        # Positive and negative values
    arr_4 = Array((4,), 1, -2, 0, 5)        # Positive and negative values and zero
    arr_5 = Array((4,), -2, -99, 0, -2)     # Negative values and zero
    arr_6 = Array((4,), -4, -1231, -2, -6)  # Only negative values

    assert arr_1.min_element() == 1
    assert arr_2.min_element() == 0
    assert arr_3.min_element() == -2
    assert arr_4.min_element() == -2
    assert arr_5.min_element() == -99
    assert arr_6.min_element() == -1231

    return

"""
2-Dimensional tests
"""


"""
N-Dimensional tests
"""
