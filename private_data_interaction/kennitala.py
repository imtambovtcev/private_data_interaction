import random


def generate_kennitala(birthday: str) -> str:
    """
    Generate a valid Icelandic Kennitala based on a given birthday.

    Args:
        birthday (str): The birthday in the format 'DDMMYY'.

    Returns:
        str: A valid 10-digit Kennitala.

    Raises:
        ValueError: If the birthday is not in the correct format (6 digits, DDMMYY).

    Notes:
        - The `century_indicator` is set to '8' for simplicity, assuming the 20th century.
        - The Kennitala is constructed as:
          [DDMMYY][century indicator][random identifier][check digit].
        - If the check digit is invalid (10), a new Kennitala is generated recursively.
    """
    if len(birthday) != 6 or not birthday.isdigit():
        raise ValueError("Birthday must be in the format 'DDMMYY'.")

    # Infer century indicator (adjust logic if more context is available)
    year = int(birthday[4:])
    century_indicator = '8'  # Default for 20th century
    if year >= 0 and year <= 99:  # Simplify if assuming DDMMYY always means 1900s
        century_indicator = '8'

    # Generate random identifier
    random_identifier = f"{random.randint(0, 999):03d}"
    partial_kennitala = birthday + century_indicator + random_identifier

    # Calculate check digit
    weights = [3, 2, 7, 6, 5, 4, 3, 2, 1]
    total = sum(int(partial_kennitala[i]) * weights[i] for i in range(9))
    remainder = total % 11
    check_digit = (11 - remainder) % 11  # Handle modulus 11 properly

    # If the check digit is invalid, retry with a new random identifier
    if check_digit == 10:
        return generate_kennitala(birthday)

    return partial_kennitala[:9] + str(check_digit)


def is_valid_kennitala(kennitala: str) -> bool:
    """
    Validate an Icelandic Kennitala.

    Args:
        kennitala (str): The 10-digit Kennitala to validate.

    Returns:
        bool: True if the Kennitala is valid, False otherwise.

    Notes:
        - The Kennitala must be 10 digits long.
        - The function verifies the check digit using the weighted sum formula.
        - If the calculated check digit is invalid (10), the Kennitala is invalid.
    """
    if len(kennitala) != 10 or not kennitala.isdigit():
        return False

    # Validation logic
    weights = [3, 2, 7, 6, 5, 4, 3, 2, 1]
    partial_kennitala = kennitala[:9]
    total = sum(int(partial_kennitala[i]) * weights[i] for i in range(9))
    remainder = total % 11
    expected_check_digit = (11 - remainder) % 11  # Handle modulus 11 properly

    # Invalid if the check digit is 10 (not allowed in Kennitala)
    if expected_check_digit == 10:
        return False

    # Check if last digit matches the expected check digit
    return int(kennitala[9]) == expected_check_digit


# Example usage
if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    birthday = "131290"  # 13th December 1990

    # Generate a Kennitala
    generated_kennitala = generate_kennitala(birthday)
    print("Generated Kennitala:", generated_kennitala)

    # Validate the generated Kennitala
    is_valid = is_valid_kennitala(generated_kennitala)
    print("Is valid Kennitala:", is_valid)
