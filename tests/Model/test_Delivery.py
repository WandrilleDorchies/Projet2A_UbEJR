import pytest
from pydantic_core import ValidationError

from src.Model.Delivery import Delivery


def test_delivery_constructor_ok():
    # WHEN
    delivery_test = Delivery(id_order=1, id_driver=1, state=0)

    # THEN
    assert isinstance(delivery_test, Delivery)
    assert delivery_test.id_order == 1
    assert delivery_test.id_driver == 1
    assert delivery_test.state == 0


def test_delivery_constructor_throws_on_incorrect_input():
    with pytest.raises(ValidationError) as exception_info:
        Delivery(id_order="one", id_driver=1, state=0)
    assert "id_order" in str(
        exception_info.value
    ) and "Input should be a valid integer, unable to parse string as an integer" in str(exception_info.value)
