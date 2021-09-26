import numpy
cimport numpy

from libc.math cimport sin

cpdef numpy.ndarray[numpy.uint8_t, ndim=1] color2grey(numpy.ndarray[numpy.uint8_t, ndim=1] a):
    cdef int i

    cdef numpy.ndarray[numpy.uint8_t, ndim=1] out
    out = numpy.ndarray(len(a), dtype=numpy.uint8_t)


    return out