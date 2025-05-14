from typing import List, Dict, Any

def acronym(words: List[str]) -> str:
    return ''.join(map(lambda x: x[0].upper(), words))


def median(numbers: List[float]) -> float:
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    return ((sorted_numbers[ (n - 1) // 2] + sorted_numbers[n // 2]) / 2)


def square_root(x: float, epsilon: float = 1e-5) -> float:
    f = lambda y: y if abs(y*y - x) < epsilon else f((y + x/y)/2)
    return f(x / 2)


def make_alpha_dict(text: str) -> Dict[str, List[str]]:
    words = text.split()
    letters = sorted(set(filter(str.isalpha, text)))
    return {letter: list(filter(lambda word: letter in word, words)) for letter in letters}


def flatten(lst: List[Any]) -> List[Any]:
    return sum(map(lambda x: flatten(x) if isinstance(x, (list, tuple)) else [x], lst), [])


if __name__ == '__main__':
    print('--- Acronym ---')
    print(acronym(['hello', 'world'])) # HW
    print(acronym(['Zakład', 'Ubezpieczeń', 'Społecznych'])) # ZUS

    print('--- Median ---')
    print(median([1, 3, 2]))  # 2.0
    print(median([3, 4, 2, 1]))  # 2.5
    print(median([1, 2, 3, 4, 5]))  # 3.0

    print('--- Square Root ---')
    print(square_root(0))  # 0.0
    print(square_root(1))  # 1.0
    print(square_root(2))  # 1.414
    print(square_root(3))  # 1.414
    print(square_root(4))  # 2.0
    print(square_root(5))  # 1.414

    print('--- Make Alpha Dict ---')
    print(make_alpha_dict('Ala ma kota, a kot ma Alę'))
    print(make_alpha_dict('on i ona'))

    print('--- Flatten ---')
    print(flatten([1, 2, [3, 4], [5, [6, 7]], 8]))  # [1, 2, 3, 4, 5, 6, 7, 8]
    print(flatten([1, 2, [3, 4], [5, [6, 7]], 8, [9, [10]]]))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(flatten([1, 2, [3, 4], [5, [6, 7]], 8, [9, [10]], [11, [12]]]))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    print(flatten([(1, 2), [3, 4], [5, [6, 7]], (8), [9, [10]], [11, [12]]]))
    print(flatten([1, 2, 3]))
    print(flatten([(1, 2, 3)]))

