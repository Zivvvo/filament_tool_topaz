# Parallelizing using Pool.map()
import multiprocessing as mp

# Redefine, with only 1 mandatory argument.

import numpy as np
from time import time

# Prepare data
np.random.RandomState(100)
arr = np.random.randint(0, 10, size=[200000, 5])
data = arr.tolist()
data[:5]


def howmany_within_range_rowonly(row, minimum=4, maximum=8):
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return count

if __name__ == "__main__":

    print(mp.cpu_count())
    pool = mp.Pool(mp.cpu_count())

    results = pool.map(howmany_within_range_rowonly, [row for row in data])

    pool.close()

    print(results[:10])
    #> [3, 1, 4, 4, 4, 2, 1, 1, 3, 3]