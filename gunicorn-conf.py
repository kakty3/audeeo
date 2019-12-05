import multiprocessing

bind = "0.0.0.0:8000"
# Generally we recommend (2 x $num_cores) + 1 as the number of workers to start off with.
# http://docs.gunicorn.org/en/stable/design.html#how-many-workers
workers = multiprocessing.cpu_count() * 2 + 1
