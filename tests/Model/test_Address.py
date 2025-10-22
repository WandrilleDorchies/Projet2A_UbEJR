import pytest
from pydantic_core import ValidationError

from src.Model.Address import Address


def test_address_constructor_ok():
    ensai = Address(
        address_id=1,
        address_number=51,
        address_street="Rue Blaise Pascal",
        address_city="Bruz",
        address_postal_code=35170,
        address_country="France",
    )

    assert isinstance(ensai, Address)
    assert ensai.address_id == 1
    assert ensai.address_number == 51
    assert ensai.address_street == "Rue Blaise Pascal"
    assert ensai.address_city == "Bruz"
    assert ensai.address_postal_code == 35170
    assert ensai.address_country == "France"


def test_address_constructor_throws_on_incorrect_input():
    with pytest.raises(ValidationError) as exception_info:
        Address(
            address_number="fifty-one",
            address_street="Rue Blaise Pascal",
            address_city="Bruz",
            address_postal_code=35170,
            address_country="France",
        )
    assert "number" in str(
        exception_info.value
    ) and "Input should be a valid integer, unable to parse string as an integer" in str(
        exception_info.value
    )
