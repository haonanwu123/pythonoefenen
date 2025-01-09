import time


def measure_execution_time(func):
    """
    A decorator that measures the execution time of a function.

    This decorator wraps a function and calculates the time it takes to execute it.
    The execution time is printed when the function is called.

    Args:
        func (function): The function whose execution time is to be measured.

    Returns:
        wrapper (function): A function that wraps the original function and adds execution time measurement.
    """

    def wrapper(*args, **kwargs):
        """
        Wrapper function that calculates the execution time of the original function.

        Args:
            *args: Positional arguments passed to the original function.
            **kwargs: Keyword arguments passed to the original function.

        Returns:
            result_func: The result of the original function call.
        """
        start_time = time.time()  # Record the start time
        result_func = func(*args, **kwargs)  # Call the original function with arguments
        end_time = time.time()  # Record the end time
        excution_time = end_time - start_time  # Calculate the execution time
        print(
            f"Execution time of {func.__name__}: {excution_time:.6f} seconds"
        )  # Print the execution time
        return result_func  # Return the result of the original function call

    return wrapper  # Return the wrapper function


@measure_execution_time
def example_function():
    """
    Example function that calculates the sum of integers from 1 to 999999.

    This function simulates some time-consuming work by summing a large range of integers.

    Returns:
        total (int): The sum of integers from 1 to 999999.
    """
    total = 0
    for number in range(1, 1000000):  # Sum numbers from 1 to 999999
        total += number
    return total  # Return the total sum


if __name__ == "__main__":
    """
    Main entry point of the program. Calls the example_function
    and measures its execution time.
    """
    example_function()  # Call the decorated function
