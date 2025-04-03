from os import environ
import sys

def show_env_var():
    environment_variables = {}
    arguments = sys.argv[1:]

    for var in environ: 
        environment_variables[var] = environ[var]
        
    for var in dict(sorted(environment_variables.items())):
        if len(arguments) > 0:
            for arg in arguments:
                if arg.lower() in var.lower():
                    print(var, "=", environment_variables[var])
                    break
        else:
            print(var, "=", environment_variables[var])

if __name__ == "__main__":
    print(type(environ))
    show_env_var()
