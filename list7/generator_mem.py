from generator_with_closure import make_generator, fib
from functools import lru_cache
import time

def make_generator_mem(f):
    return make_generator(lru_cache(maxsize=None)(f))


if __name__ == '__main__':
    start = time.time()

    print("Fibonacci:")
    fib_gen = make_generator_mem(fib)
    for _ in range(1000):
        print(next(fib_gen))

    # print("\nCiąg arytmetyczny (3n+1):")
    # arith_gen = make_generator_mem(lambda n: 3 * n + 1)
    # for _ in range(5):
    #     print(next(arith_gen))

    # print("\nCiąg geometryczny (2^n):")
    # geom_gen = make_generator_mem(lambda n: 2 ** n)
    # for _ in range(5):
    #     print(next(geom_gen))

    # print("\nCiąg kwadratów (n^2):")
    # square_gen = make_generator_mem(lambda n: n * n)
    # for _ in range(5):
    #     print(next(square_gen))

    end = time.time()
    print(f"Execution time with memoization: {end - start:.6f} seconds")