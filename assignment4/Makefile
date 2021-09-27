main:
	python setup.py build_ext --build-lib instapy/

run:
	# Task 4.0
	cd profiling_scripts && python manual_timing_.py
	cd profiling_scripts && python timeit_timing_.py
	cd profiling_scripts && python cProfile_timing_.py
	# Task 4.1
	cd report_scripts && python grayscale_benchmarks.py
	# Task 4.2
	cd report_scripts && python sepia_benchmarks.py

clean:
	rm img/rain_grayscale_*
	rm img/rain_sepia_*
	rm reports/*
	rm src/cython_color2gray.c*
	rm src/cython_color2sepia.c*
