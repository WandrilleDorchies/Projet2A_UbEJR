from datetime import date, time
from unittest.mock import Mock

import pytest
from pydantic_core import ValidationError

from src.Model.Item import Item
from src.Model.Order import Order


def test_order_constructor_ok():
    mock_item = Mock(spec=Item)

    order_test = Order(
        order_id=1,
        order_customer_id=1,
        order_date=date(2025, 5, 5),
        order_time=time(12, 30),
        order_items=[mock_item],
    )

    assert isinstance(order_test, Order)
    assert order_test.order_id == 1
    assert order_test.order_customer_id == 1
    assert order_test.order_state == 0
    assert order_test.order_date == date(2025, 5, 5)
    assert order_test.order_time == time(12, 30)
    assert order_test.order_items[0] == mock_item
    assert order_test.order_is_paid is False
    assert order_test.order_is_prepared is False


def test_order_constructor_throws_on_incorrect_input():
    with pytest.raises(ValidationError) as exception_info:
        mock_item = Mock(spec=Item)

        Order(
            order_id="one",
            order_customer_id=1,
            order_date=date(2025, 5, 5),
            order_time=time(12, 30),
            order_items=[mock_item],
        )
    assert "order_id" in str(
        exception_info.value
    ) and "Input should be a valid integer, unable to parse string as an integer" in str(
        exception_info.value
    )
