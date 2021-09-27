import numpy
from distutils.core import setup
from Cython.Build import cythonize

setup(name="instapy",
      version="1.0",
      packages=["instapy"],
      scripts=["bin/instapy"],
      ext_modules=cythonize("instapy/*.pyx"),
      include_dirs=[numpy.get_include()],
      install_requires=["numpy"] 
      )