import pytest
from pydantic_core import ValidationError

from src.Model.Item import Item


def test_item_constructor_ok():
    item_test = Item(
        id_item=1, name="Coca", price=1.5, item_type="boisson", description="canette 33cl", stock=10
    )

    assert item_test.id_item == 1
    assert item_test.name == "Coca"
    assert item_test.price == 1.5
    assert item_test.item_type == "boisson"
    assert item_test.description == "canette 33cl"
    assert item_test.stock == 10


def test_item_constructor_throws_on_incorrect_input():
    with pytest.raises(ValidationError) as exception_info:
        Item(
            id_item="one",
            name="Coca",
            price=1.5,
            item_type="boisson",
            description="canette 33cl",
            stock=10,
        )
    assert "id_item" in str(
        exception_info.value
    ) and "Input should be a valid integer, unable to parse string as an integer" in str(
        exception_info.value
    )
