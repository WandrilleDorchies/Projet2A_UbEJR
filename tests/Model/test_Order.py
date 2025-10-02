from unittest.mock import Mock

import pytest
from pydantic_core import ValidationError
from src.Model.Item import Item

from src.Model.Order import Order


def test_order_constructor_ok():
    mock_item = Mock(spec=Item)

    mock_date = Mock(name="mock_date")
    mock_time = Mock(name="mock_time")

    order_test = Order(
        id_order=1,
        client_id=1,
        items=[mock_item],
        date=mock_date,
        time=mock_time,
    )

    assert order_test.id_order == 1
    assert order_test.client_id == 1
    assert order_test.items[0] == mock_item
    assert order_test.date == mock_date
    assert order_test.time == mock_time
    assert order_test.state == 0
    assert order_test.is_paid is False
    assert order_test.is_prepared is False


def test_order_constructor_throws_on_incorrect_input():
    with pytest.raises(ValidationError) as exception_info:
        mock_item = Mock(spec=Item)

        mock_date = Mock(name="mock_date")
        mock_time = Mock(name="mock_time")

        Order(
            id_order="one",
            client_id=1,
            items=[mock_item],
            date=mock_date,
            time=mock_time,
        )
    assert "id" in str(
        exception_info.value
    ) and "Input should be a valid integer, unable to parse string as an integer" in str(exception_info.value)
