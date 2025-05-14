import random
import string

class PasswordGenerator:
    def __init__(self, length, charset=None, count=1):
        self.length = length
        self.charset = charset if charset is not None else string.ascii_letters + string.digits
        self.count = count
        self.generated = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.generated >= self.count:
            raise StopIteration
        self.generated += 1
        return ''.join(random.choices(self.charset, k=self.length))
    

if __name__ == '__main__':

    print('----- next() -----')
    gen = PasswordGenerator(length=8, count=3)
    try:
        print(next(gen))
        print(next(gen))
        print(next(gen))
        print(next(gen))
    except StopIteration:
        print('StopIteration raised!!!!!!!!!!!!!!!')
 
    print('\n----- for-loop -----')
    for pswd in PasswordGenerator(length=10, count=5):
        print(pswd)

