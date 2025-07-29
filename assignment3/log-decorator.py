# Task 1: Writing and Testing a Decorator

import logging
from functools import wraps

# One-time setup
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        # Format log message
        log_message = (
            f"function: {func.__name__}\n"
            f"positional parameters: {args if args else 'none'}\n"
            f"keyword parameters: {kwargs if kwargs else 'none'}\n"
            f"return: {result}\n"
        )

        logger.log(logging.INFO, log_message)
        return result
    return wrapper

# Sample decorated functions 
@logger_decorator
def say_hello():
    print("Hello, World!")

@logger_decorator
def always_true(*args):
    return True

@logger_decorator
def return_decorator(**kwargs):
    return logger_decorator

# Main block 
if __name__ == "__main__":
    say_hello()
    always_true(1, 2, 3)
    return_decorator(name="Zwek", age=25)
