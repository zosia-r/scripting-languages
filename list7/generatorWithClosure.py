def make_generator(f):
    def generator():
        x = 1
        while True:
            yield f(x)
            x += 1
    return generator()

def fib(n):
    if n == 1 or n == 2:
        return 1
    a, b = 1, 1
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

if __name__ == "__main__":
    print("Fibonacci:")
    fib_gen = make_generator(fib)
    for _ in range(10):
        print(next(fib_gen))

    print("\nCiąg arytmetyczny (3n+1):")
    arith_gen = make_generator(lambda n: 3 * n + 1)
    for _ in range(5):
        print(next(arith_gen))

    print("\nCiąg geometryczny (2^n):")
    geom_gen = make_generator(lambda n: 2 ** n)
    for _ in range(5):
        print(next(geom_gen))

    print("\nCiąg kwadratów (n^2):")
    square_gen = make_generator(lambda n: n * n)
    for _ in range(5):
        print(next(square_gen))
