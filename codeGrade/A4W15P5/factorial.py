def factorial(n: int) -> int:
    factorial_result = 1

    if n <= 0:
        raise ValueError("the number must be positive.")
    else:
        for decrementing_number in range(1, n + 1):
            factorial_result *= decrementing_number
        return factorial_result


def rec_factorial(n: int) -> int:
    if n <= 0:
        raise ValueError("the number must be positive.")
    elif n == 1:
        return 1
    else:
        return n * rec_factorial(n - 1)
