
def validate_cpf(cpf: str) -> bool:           

    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False
    
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False
    
    return True


if __name__ == "__main__":
    print(validate_cpf("40574658807"))