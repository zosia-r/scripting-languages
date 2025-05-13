import logging
import time

def configure_logger(level=logging.DEBUG):
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=level
    )

def log(level=logging.DEBUG):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time() 
            result = None
            
            try:
                logging.log(level, f"Calling function {func.__name__} with arguments {args} and kwargs {kwargs}")
                result = func(*args, **kwargs)
            except Exception as e:
                logging.log(level, f"Function {func.__name__} raised an exception: {e}")
                raise
            finally:
                end_time = time.time() 
                duration = end_time - start_time
                logging.log(level, f"Function {func.__name__} returned {result} and took {duration:.4f} seconds")
                
            return result
        return wrapper
    return decorator

def log_class_creation(level=logging.DEBUG):
    def decorator(cls):
        class Wrapped(cls):
            def __init__(self, *args, **kwargs):
                logging.log(level, f"Creating instance of class {cls.__name__} with arguments {args} and kwargs {kwargs}")
                super().__init__(*args, **kwargs)
        return Wrapped
    return decorator


@log(level=logging.INFO)
def add(a, b):
    return a + b

@log_class_creation(level=logging.INFO)
class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

if __name__ == "__main__":
    configure_logger(level=logging.DEBUG)
    add(2, 3)
    obj = MyClass(10, 20)
