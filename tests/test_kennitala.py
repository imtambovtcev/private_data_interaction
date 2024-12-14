import pytest
from private_data_interaction.kennitala import generate_kennitala, is_valid_kennitala


def test_generate_kennitala_valid_birthday():
    birthday = "131290"  # Valid birthday in DDMMYY format
    kennitala = generate_kennitala(birthday)
    assert len(kennitala) == 10, "Kennitala must be 10 digits long"
    assert kennitala[:6] == birthday, "Kennitala must start with the birthday"
    assert kennitala[6].isdigit(
    ), "Kennitala must have a valid century indicator"
    assert kennitala[7:9].isdigit(
    ), "Kennitala must have a valid personal identifier"
    assert kennitala[9].isdigit(), "Kennitala must have a valid check digit"
    assert is_valid_kennitala(kennitala), "Generated kennitala must be valid"


def test_is_valid_kennitala_valid():
    valid_kennitala = "1312908657"  # Example valid kennitala
    assert is_valid_kennitala(
        valid_kennitala), "Valid kennitala must pass validation"


def test_is_valid_kennitala_invalid_length():
    invalid_kennitala = "131290812"  # Only 9 digits
    assert not is_valid_kennitala(
        invalid_kennitala), "Kennitala with invalid length must fail validation"


def test_is_valid_kennitala_invalid_characters():
    invalid_kennitala = "131290812X"  # Contains non-digit character
    assert not is_valid_kennitala(
        invalid_kennitala), "Kennitala with non-digit character must fail validation"


def test_is_valid_kennitala_invalid_check_digit():
    invalid_kennitala = "1312908125"  # Example invalid check digit
    assert not is_valid_kennitala(
        invalid_kennitala), "Kennitala with invalid check digit must fail validation"


@pytest.mark.parametrize("birthday", [
    "010101",  # 1st January 2001
    "310599",  # 31st May 1999
    "150345",  # 15th March 1945
])
def test_generate_kennitala_various_birthdays(birthday):
    kennitala = generate_kennitala(birthday)
    assert len(kennitala) == 10, "Kennitala must be 10 digits long"
    assert kennitala[:6] == birthday, "Kennitala must start with the birthday"
    assert is_valid_kennitala(
        kennitala), "Generated kennitala must be valid for various birthdays"
