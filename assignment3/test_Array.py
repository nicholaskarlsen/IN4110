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
    shape = (4,)
    vals = (1, 2, 3, 4)
    arr_1 = Array(shape, *vals)
    # Test elementwise addition of a single number
    arr_2 = arr_1 + 10

    for i in range(4):
        assert arr_2[i] == vals[i] + 10

    # Test elementwise addition of an array object
    arr_3 = arr_1 + arr_2
    for i in range(4):
        assert arr_3[i] == (vals[i] + 10) + vals[i]

    # Test that addition is commutative (i.e that _radd_ is working as it should.)
    arr_2 = 10 + arr_1
    for i in range(4):
        assert arr_2[i] == vals[i] + 10

    arr_3 = arr_2 + arr_1
    for i in range(4):
        assert arr_3[i] == (vals[i] + 10) + vals[i]

    return

def test_1d_subtraction():
    """
    One or more tests verifying that substracting from a 1d-array element-
    wise returns what it’s supposed to
    """
    pass

def test_1d_multiplication():
    """
    One or more tests verifying that multiplying a 1d-array element-wise by
    a factor or other 1-d array returns what it’s supposed to
    """
    pass

def test_comparrison_operator():
    """
    One or more tests verifying that comparing arrays (by ==) returns what
    it is supposed to - which should be a boolean.
    """
    pass

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
    pass


"""
2-Dimensional tests
"""


"""
N-Dimensional tests
"""
