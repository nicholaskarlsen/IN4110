import numpy
from distutils.core import setup
from Cython.Build import cythonize

setup(name='Cython modules',
      ext_modules=cythonize("src/*.pyx"),
      include_dirs=[numpy.get_include()])