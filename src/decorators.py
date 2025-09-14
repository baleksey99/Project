from time import time


def log(filename=None):
    """декоратор, который будет автоматически логировать начало и
конец выполнения функции, а также ее результаты или возникшие ошибки."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                if filename:
                    with open(filename, 'a') as f:
                        f.write(f'Function {func.__name__} started\n')
                else:
                    print(f'Function {func.__name__} started')

                result = func(*args, **kwargs)

                if filename:
                    with open(filename, 'a') as f:
                        f.write(f'example called with args {args} and kwargs {kwargs}: result {result}\n')
                else:
                    print(f'example called with args {args} and kwargs {kwargs}: result {result}')

                return result
            except Exception as e:
                error_message = f"{func.__name__} error: {str(e)}. Inputs: {args}, {kwargs}"
                if filename:
                    with open(filename, 'a') as f:
                        f.write(error_message + '\n')
                else:
                    print(error_message)
                raise
        return wrapper
    return decorator


def timer(func):
    def wrapper(*args, **kwargs):
        time_1 = time()
        result = func(*args, **kwargs)
        time_2 = time()
        print(f'Time for work: {time_2 - time_1}')
        return result
    return wrapper


@log(filename="mylog.txt")
@timer
def example():
    for i in range(100000000):
        continue


example()
