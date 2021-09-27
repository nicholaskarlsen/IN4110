main:
	# Task 4.0
	python manual_timing_.py
	python timeit_timing_.py
	python cProfile_timing_.py
	# Task 4.1
	python setup.py build_ext --inplace
	python grayscale_benchmarks.py
	# Task 4.2
	python sepia_benchmarks.py

clean:
	rm img/rain_grayscale_*
	rm img/rain_sepia_*
	rm reports/*
