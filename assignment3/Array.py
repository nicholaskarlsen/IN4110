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
        different_types = type(values[0])
        self.T = type(values[0])
        for val in values:
            if self.T != type(val):
                raise ValueError("Values are not all of the same type")

        self.shape = shape  # Shape of the data
        self.dim = len(shape)  # Dimensionality of the data
        # Static, contiguously in memory C-style array containing the data
        self._array = self.__initialize_array(values)

        # Optional: If not all values are of same type, all are converted to floats.
        return

    def __initialize_array(self, values):
        """
        Private method which initializes the internal storage used in the class.
        Stores the input values in a static, contiguous C type array.

        Args:
            values: tuple of input values provided in the constructor

        Returns:
            static C type array of the appropriate type containing the input values

        Raises:
            TypeError: If attempting to initialize an array containing elements of an unsupported type
        """
        if self.T is int:
            return (ctypes.c_int * self.size)(*values)

        elif self.T is float:
            return (ctypes.c_float * self.size)(*values)

        elif self.T == bool:
            return (ctypes.c_bool * self.size)(*values)

        else:
            raise TypeError(
                "Unsupported type in the input values. Supported types: int, float, bool"
            )

        return

    def __str__(self):
        """Returns a nicely printable string representation of the array, similar to Numpy.
        NOTE: Only implemented to work for 1 and 2D arrays.

        Returns:
            str_repr: A string representation of the array.

        Raises:
            NotImplementedError: If attempting to print array of dimensionality > 2
        """
        str_repr = ""
        if self.dim == 1:
            str_repr += self.__str_row(0, self.size)

        elif self.dim == 2:
            str_repr += "["
            for i in range(self.shape[0]):
                str_repr += self.__str_row(i * self.shape[1], (i + 1) * self.shape[1])
                str_repr += "\n "

            # Also remove the trailing newline & space inserted in line above
            str_repr = str_repr[:-2] + "]"

        elif self.dim > 2:
            raise NotImplementedError(
                "__str__ has not been implemended for arrays of dimensionality > 2"
            )

        return str_repr

    def __str_row(self, start, stop):
        """Returns a nicely formatted string representation of a sequence of entries in the array.
        Used to produce the rows in the __str__ method.

        Returns:
            str_repr: A string representation of a sequence of entries in the array
        """
        str_repr = "["
        for i in range(start, stop):
            str_repr += "{} ".format(self._array[i])

        # Also remove the trailing newline & space inserted in line above
        str_repr = str_repr[:-1] + "]"

        return str_repr

    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        NOTE: This method works for N-dim arrays

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        if isinstance(other, Array):
            if self.shape != other.shape:
                return NotImplemented

            if self.T != other.T:
                return NotImplemented

            # Create a new Array object with the contents and shape of this array
            sum_array = Array(self.shape, *self._array)

            # Recall: then underlying storage (i.e _array) is contiguous
            for i in range(self.size):
                sum_array._array[i] += other._array[i]

            return sum_array

        else:
            if self.T != type(other):
                return NotImplemented

            # Create a new Array object with the contents and shape of this array
            sum_array = Array(self.shape, *self._array)

            # Recall: then underlying storage (i.e _array) is contiguous
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

        NOTE: This method works for N-dim arrays

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
                # Recall: the underlying storage (i.e _array) is contiguous
                sub_array._array[i] -= other._array[i]

            return sub_array

        else:
            if self.T != type(other):
                return NotImplemented
            # Create a new Array object with the contents and shape of this array
            sub_array = Array(self.shape, *self._array)

            # Recall: the underlying storage (i.e _array) is contiguous
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
        # No obvious way to re-use __sub__ in a similar when subtracting a single number/bool, so write it out manually.
        else:
            if self.T != type(other):
                return NotImplemented

            # Create a new Array object with the contents and shape of this array
            sub_array = Array(self.shape, *self._array)

            # Recall: the underlying storage (i.e _array) is contiguous
            for i in range(self.size):
                sub_array._array[i] = -sub_array._array[i] + other

            return sub_array

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        NOTE: This method works for N-dim arrays

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

            # Recall: the underlying storage (i.e _array) is contiguous
            for i in range(self.size):
                prod_arr._array[i] *= other._array[i]

            return prod_arr

        else:
            if self.T != type(other):
                return NotImplemented

            # Create a new Array object with the contents and shape of this array
            prod_arr = Array(self.shape, *self._array)

            # Recall: the underlying storage (i.e _array) is contiguous
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

        NOTE: This method works for N-dim arrays

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        if not isinstance(other, Array):
            return False

        if self.shape != other.shape:
            return False

        if self.T != other.T:
            return False

        # Ensure that the contents of the arrays are identical
        for i in range(self.size):
            if self._array[i] != other._array[i]:
                return False

        # If none of the above tests return False, the arrays are equivalent.
        return True

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.

        NOTE: This method works for N-dim arrays

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        # Initialize the output Array filled with all True entries in a compact way.
        equal_array = Array(self.shape, *[bool(1) for x in range(self.size)])

        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError("Shape mismatch")

            if self.T != other.T:
                raise TypeError("Incompatible type")

            # Recall: the underlying storage (i.e _array) is contiguous.
            for i in range(self.size):
                equal_array._array[i] = self._array[i] == other._array[i]

        elif isinstance(other, self.T):
            # Recall: the underlying storage (i.e _array) is contiguous.
            for i in range(self.size):
                equal_array._array[i] = self._array[i] == other

        else:
            raise TypeError("Incompatible type")

        return equal_array

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        NOTE: This method works for N-dim arrays

        Returns:
            float: The value of the smallest element in the array.
        """
        if self.T is bool:
            return NotImplemented

        # Note: Since the underlying storage is contiguous, this works for any dimensionality
        minval = self._array[0]
        for i in range(1, self.size):
            minval = self._array[i] if self._array[i] < minval else minval

        return minval

    def __getitem__(self, idx):
        """Returns elements stored in the Array. If the Array is 1-D, it will array the element itself, but
        for 2-D, it will return a new Array containing the desired row.

        e.g for a 2D Array, fetching the i-th index yields A[i] -> Array((i), A[i][0], A[i][1], ...)
        The method has not been expanded to support the general N-dimensional.

        Args:
            idx: Index of the element you wish to fetch

        Returns:
            An element of type T or an Array of type T stored in the corresponding index

        Raises:
            IndexError: If attempting to access an element outside the range of the array
            NotImplementedError: If attempted to use for an array of dimensionality
        """
        # 1-Dimensional indexing
        if type(idx) == int:
            # if it is a 1-Dim array, simply return the entry corresponding to idx
            if len(self.shape) == 1:
                if not (0 <= idx < self.size):
                    raise IndexError(
                        "Attempting to access an element outside the range of the array"
                    )

                return self._array[idx]
            # If it is a 2-Dim array, return the row corresponding to idx by creating a new array containing that row.
            elif len(self.shape) == 2:
                if not (0 <= idx < self.shape[0]):
                    raise IndexError(
                        "Attempting to access an element outside the range of the array"
                    )
                return Array(
                    self.shape[1:],
                    *self._array[idx * self.shape[1] : (idx + 1) * self.shape[1]]
                )
            else:
                raise NotImplementedError("__getitem__ not implemented for dim>2")
        # Only accept integer indexing. i.e no slicing, because that would get rather involved for dim > 1
        else:
            return NotImplemented
