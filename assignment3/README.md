# Array class

A python class which attempts to replicate some of the behaviour of numpy-type arrays, allowing one to perform elementwise arithmetic operations on numbers as well as other instances of the Array class. Furthermore, the underlying storage used in the Array class is contiguous in memory and much of the functionality trivially generalizes to N-dimensions, however, the class only fully supports up to 2D.

## Example usage
You may create an instance of the class like
```python
>>> A = Array((4,), 1, 2, 3, 4)
```
Arithmatic operations work elementwise like they do in numpy
```python
>>> print(A + 1)
[2 3 4 5]
>>> B = Array((4,), 5, 2, 7, 2)
>>> print(A + B)
[6 4 10 6]
```
Arrays are printed to the terminal in a nicely formatted way
```python
>>> C = Array((2,3), 1, 2, 3, 4, 5, 6)
>>> print(C)
[[1 2 3]
 [4 5 6]]
```
And much more!

## Unit tests
Unit tests for the Array class is contained in the file `test_Array.py` and is reccomended to run using pytest like
```bash
$ pytest test_Array.py
```
The tests covers all of the class methods in both the 1 and 2D cases, often using Numpy as the ground truth.

## Documentation

### Public Attributes 
|   |   | 
|---|---|
| `size`        | Total number of elements stored in the Array |   
| `T`           | The type of data stored in the array. Valid types are Int, Float and Bool | 
| `shape`       | A tuple containing the shape of the array | 
| `dim`         | The dimensionality of the array, equal to the length of the shape tuple|

### Public Methods
|   |   | 
|---|---|
| `+ (Operator)`                | Performs element-wise addition of a single number or another array with the same shape. Returns a new array with the same shape populated with the result of the operation |   
| `- (Operator)`                | Performs element-wise subtraction of a single number or another array with the same shape. Returns a new array with the same shape populated with the result of the operation |
| `* (Operator)`                | Performs element-wise multiplication of a single number or another array with the same shape. Returns a new array with the same shape populated with the result of the operation |
| `== (Operator)`               | Check if two arrays are identical. That is; if they have the same shape and the same entries. Returns a boolean. | 
| `is_equal(other)`             | Performs element-wise comparison of a single number or another array with the same shape. Returns a boolean array with entries corresponding to the outcome of the comparison. | 
| `min_element()`               | Finds and returns the smallest element in an array containing Float or Int. |