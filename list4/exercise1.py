from os import environ
import sys

def show_env_var():

    arguments = sys.argv[1:]
    
    for var, value in sorted(environ.items()): 
        if not arguments or any(arg.lower() in var.lower() for arg in arguments):
            print(var, "=", value)


if __name__ == "__main__":
    show_env_var()