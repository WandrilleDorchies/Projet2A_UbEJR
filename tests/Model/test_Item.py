import pytest
from pydantic_core import ValidationError

from src.Model.Item import Item


def test_item_constructor_ok():
    item_test = Item(
        item_id=1,
        orderable_id=1,
        item_name="Coca",
        item_price=1.5,
        item_type="boisson",
        item_description="canette 33cl",
        item_stock=10,
    )

    assert item_test.item_id == 1
    assert item_test.orderable_type == "item"
    assert item_test.orderable_id == 1
    assert item_test.item_name == "Coca"
    assert item_test.item_price == 1.5
    assert item_test.item_type == "boisson"
    assert item_test.item_description == "canette 33cl"
    assert item_test.item_stock == 10
    assert item_test.item_in_menu is True


def test_item_constructor_throws_on_incorrect_input():
    with pytest.raises(ValidationError) as exception_info:
        Item(
            item_id="one",
            orderable_id=1,
            item_name="Coca",
            item_price=1.5,
            item_type="boisson",
            item_description="canette 33cl",
            item_stock=10,
        )
    assert "item_id" in str(
        exception_info.value
    ) and "Input should be a valid integer, unable to parse string as an integer" in str(
        exception_info.value
    )


@pytest.mark.parametrize(
    "test",
    [
        1,
        "Item",
        Item(
            item_id=1,
            orderable_id=2,
            item_name="Coca",
            item_price=1.5,
            item_type="boisson",
            item_description="canette 33cl",
            item_stock=10,
        ),
    ],
)
def test_item_not_equal(test):
    item1 = Item(
        item_id=1,
        orderable_id=1,
        item_name="Coca",
        item_price=1.5,
        item_type="boisson",
        item_description="canette 33cl",
        item_stock=10,
    )

    assert not item1 == test


def test_items_equal():
    item1 = Item(
        item_id=1,
        orderable_id=1,
        item_name="Coca",
        item_price=1.5,
        item_type="boisson",
        item_description="canette 33cl",
        item_stock=10,
    )
    item2 = Item(
        item_id=1,
        orderable_id=1,
        item_name="Coca",
        item_price=1.5,
        item_type="boisson",
        item_description="canette 33cl",
        item_stock=10,
    )

    assert item1 == item2
