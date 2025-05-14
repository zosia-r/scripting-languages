
def forall(pred, iterable):
    return all(pred(x) for x in iterable)

def exists(pred, iterable):
    return any(pred(x) for x in iterable)

def atleast(n, pred, iterable):
    return sum(1 for x in iterable if pred(x)) >= n

def atmost(n, pred, iterable):
    return sum(1 for x in iterable if pred(x)) <= n


def is_even(x):
    return x % 2 == 0


if __name__ == "__main__":
    nums = [2, 4, 6, 8]

    print("forall:", forall(is_even, nums))       
    print("exists:", exists(is_even, nums))       
    print("atleast 3:", atleast(3, is_even, nums))
    print("atmost 5:", atmost(5, is_even, nums))  
