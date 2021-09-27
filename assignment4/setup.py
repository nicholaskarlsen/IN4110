import numpy
from distutils.core import setup, Extension
from Cython.Build import cythonize

cython_gray_module = Extension("cython_color2gray", ["instapy/cython_color2gray.pyx"])
cython_sepia_module = Extension("cython_color2sepia", ["instapy/cython_color2sepia.pyx"])

setup(name="instapy",
      version="1.0",
      packages=["instapy"],
      scripts=["bin/instapy"],
      ext_modules=cythonize([cython_gray_module, cython_sepia_module]),
      include_dirs=[numpy.get_include()],
      install_requires=["numpy", "opencv-python", "cython", "numba"] 
      )