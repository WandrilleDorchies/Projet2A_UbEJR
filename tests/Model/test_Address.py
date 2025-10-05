import pytest
from pydantic_core import ValidationError

from src.Model.Address import Address


def test_address_constructor_ok():
    # WHEN
    ensai = Address(
        number=51, street="Rue Blaise Pascal", city="Bruz", postal_code=35170, country="France"
    )

    # THEN
    assert isinstance(ensai, Address)
    assert ensai.number == 51
    assert ensai.street == "Rue Blaise Pascal"
    assert ensai.city == "Bruz"
    assert ensai.postal_code == 35170
    assert ensai.country == "France"


def test_address_constructor_throws_on_incorrect_input():
    with pytest.raises(ValidationError) as exception_info:
        Address(
            number="fifty-one",
            street="Rue Blaise Pascal",
            city="Bruz",
            postal_code=35170,
            country="France",
        )
    assert "number" in str(
        exception_info.value
    ) and "Input should be a valid integer, unable to parse string as an integer" in str(
        exception_info.value
    )
