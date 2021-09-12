import ctypes

class Array:
    def __init__(self, shape, *values):
        """
        Initialize an array of 1-dimensionality. Elements can only be of type:
        - int
        - float
        - bool

        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either numeric or boolean.

        Raises:
            ValueError: If the values are not all of the same type.
        """
        # product of entries in shape should correspond to the number of elements in values
        self.size = 1
        for s in shape:
            self.size *= s
        if self.size != len(values):
            raise ValueError("The number of values does not fit with the shape")

        # Type of the 0-th entry should be equal to type of all other entries
        self.T = type(values[0])
        for val in values:
            if self.T != type(val):
                raise ValueError("Values are not all of the same type")

        self.shape = shape                              # Shape of the data
        self.dim = len(shape)                           # Dimensionality of the data
        self.num_elements = len(values)                 # The total number of entries in the array
        self._array = self.__initialize_array(values)   # Static, contigously stored C-style array containing the data
        # Optional: If not all values are of same type, all are converted to floats.
        return


    def __initialize_array(self, values):
        """
        Stores the input values in a static, contigous C type array.

        Args:
            values: tuple of input values provided in the constructor

        Returns:
            static C type array of the appropriate type containing the input values
        """
        if self.T is int:
            return (ctypes.c_int * self.size)(*values)

        elif self.T is float:
            return (ctypes.c_float * self.size)(*values)

        elif self.T == bool:
            return (ctypes.c_bool * self.size)(*values)

        else:
            raise TypeError("Unsupported type in the input values. Supported types: int, float, bool")

        return

    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str_repr: A string representation of the array.

        """
        str_repr = "" # String representation of the array
        str_repr += "["
        for i in range(self.shape[0] - 1):
            str_repr += "{}, ".format(self._array[i])
        str_repr += "{}]".format(self._array[self.shape[0] - 1])
        str_repr += "\n"
        # If the array is N>1 dimensional
        if self.dim > 1:
            str_repr = "[" + str_repr
            for d in range(1, self.dim):
                str_repr += " ["
                for i in range(self.shape[d]-1):
                    # data is stored contigously in memory, so access them C style with offsets.
                    # NOTE: will have to sum over all the previous offsets for dim>2 !!!
                    str_repr += "{}, ".format(self._array[self.shape[d - 1] + i])
                str_repr += "{}]".format(self._array[self.shape[d - 1] + self.shape[d]-1])
                str_repr += "]\n"

        return str_repr[:-1] # Don't include the last newline

    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise NotImplemented
            if self.T != other.T:
                return NotImplemented
            # Create a new Array object with the contents and shape of this array
            sum_array = Array(self.shape, *self._array)
            for i in range(self.size):
                sum_array._array[i] += other[i]

            return sum_array

        else:
            if self.T != type(other):
                return NotImplemented
            # Create a new Array object with the contents and shape of this array
            sum_array = Array(self.shape, *self._array)
            for i in range(self.size):
                sum_array._array[i] += other

            return sum_array



    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        return self.__add__(other)

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise NotImplemented
            if self.T != other.T:
                return NotImplemented
            # Create a new Array object with the contents and shape of this array
            sub_array = Array(self.shape, *self._array)
            for i in range(self.size):
                sub_array._array[i] -= other[i]

            return sub_array

        else:
            if self.T != type(other):
                return NotImplemented
            # Create a new Array object with the contents and shape of this array
            sub_array = Array(self.shape, *self._array)
            for i in range(self.size):
                sub_array._array[i] -= other

            return sub_array

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """
        if isinstance(other, Array):
            return other.__sub__(self)
        # No obvious way to re-use __sub__ in a similar when subtracting a single number/bool, so have to write it out manually.
        else:
            if self.T != type(other):
                return NotImplemented
            # Create a new Array object with the contents and shape of this array
            sub_array = Array(self.shape, *self._array)
            for i in range(self.size):
                sub_array._array[i] = - sub_array._array[i] + other

            return sub_array


    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise NotImplemented
            if self.T != other.T:
                return NotImplemented
            # Create a new Array object with the contents and shape of this array
            prod_arr = Array(self.shape, *self._array)
            for i in range(self.size):
                prod_arr._array[i] *= other[i]

            return prod_arr

        else:
            if self.T != type(other):
                return NotImplemented
            # Create a new Array object with the contents and shape of this array
            prod_arr = Array(self.shape, *self._array)
            for i in range(self.size):
                prod_arr._array[i] *= other

            return prod_arr

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        # Hint: this solution/logic applies for all r-methods
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        if not isinstance(other, Array):
            return False

        if self.shape != other.shape:
            return False

        # Ensure that the contents of the arrays are identical
        for i in range(self.size):
            if self._array[i] != other[i]:
                return False

        # If none of the above tests return False, the arrays are (probably) equivalent.
        return True

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        if isinstance(other, Array):
            pass

        if isinstance(other, self.T):
            pass

        return TypeError

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """
        if self.T is bool:
            return NotImplemented

        minval = self._array[0]
        for i in range(1, self.size):
            minval = self._array[i] if self._array[i] < minval else minval

        return minval

    def __getitem__(self, idx):
        # 1-Dimensional indexing 
        if type(idx) == int and len(self.shape) == 1:
            # NOTE: Boundary check is already present in ctype, so a check if idx < size would be redundant.
            return self._array[idx]
        # N-dimensional case



if __name__=="__main__":
    shape = (3,2)
    my_array = Array(shape, 1, 2, 3, 4, 5, 6)
    print(my_array)

    shape = (2,2,2)
    my_array = Array(shape, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    print(my_array)

    """
    assert my_array[2] == 1
    print(my_array)
    print(my_array.min_element())
    print(type(my_array))
    print(my_array+my_array)
    """
