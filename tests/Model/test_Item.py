import pytest
from pydantic_core import ValidationError

from src.Model.Item import Item


def test_item_constructor_ok():
    item_test = Item(
        item_id=1,
        item_name="Coca",
        item_price=1.5,
        item_type="boisson",
        item_description="canette 33cl",
        item_stock=10,
    )

    assert item_test.item_id == 1
    assert item_test.item_name == "Coca"
    assert item_test.item_price == 1.5
    assert item_test.item_type == "boisson"
    assert item_test.item_description == "canette 33cl"
    assert item_test.item_stock == 10


def test_item_constructor_throws_on_incorrect_input():
    with pytest.raises(ValidationError) as exception_info:
        Item(
            item_id="one",
            item_name="Coca",
            item_price=1.5,
            item_type="boisson",
            item_description="canette 33cl",
            item_stock=10,
        )
    assert "id_item" in str(
        exception_info.value
    ) and "Input should be a valid integer, unable to parse string as an integer" in str(
        exception_info.value
    )
