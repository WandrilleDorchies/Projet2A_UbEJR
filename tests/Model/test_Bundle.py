from datetime import datetime
from unittest.mock import Mock

import pytest
from pydantic_core import ValidationError

from src.Model.Bundle import Bundle
from src.Model.Item import Item


def test_order_constructor_ok():
    mock_item = Mock(spec=Item)

    bundle_test = Bundle(
        bundle_id=1,
        orderable_id=1,
        bundle_name="Menu",
        bundle_reduction=25,
        bundle_description="Menu classique",
        bundle_availability_start_date=datetime(2025, 10, 9, 12, 30, 0),
        bundle_availability_end_date=datetime(2025, 10, 9, 13, 0, 0),
        bundle_items={mock_item: 1},
    )

    assert isinstance(bundle_test, Bundle)
    assert bundle_test.bundle_id == 1
    assert bundle_test.orderable_id == 1
    assert bundle_test.orderable_type == "bundle"
    assert bundle_test.bundle_name == "Menu"
    assert bundle_test.bundle_reduction == 25
    assert bundle_test.bundle_description == "Menu classique"
    assert bundle_test.bundle_availability_start_date == datetime(2025, 10, 9, 12, 30, 0)
    assert bundle_test.bundle_availability_end_date == datetime(2025, 10, 9, 13, 0, 0)
    assert list(bundle_test.bundle_items)[0] == mock_item
    assert list(bundle_test.bundle_items.values())[0] == 1


def test_order_constructor_throws_on_incorrect_input():
    with pytest.raises(ValidationError) as exception_info:
        mock_item = Mock(spec=Item)

        Bundle(
            bundle_id="one",
            orderable_id=1,
            bundle_name="Menu",
            bundle_reduction=25,
            bundle_description="Menu classique",
            bundle_availability_start_date=datetime(2025, 10, 9, 12, 30, 0),
            bundle_availability_end_date=datetime(2025, 10, 9, 13, 0, 0),
            bundle_items={mock_item: 1},
        )
    assert "bundle_id" in str(
        exception_info.value
    ) and "Input should be a valid integer, unable to parse string as an integer" in str(
        exception_info.value
    )


def test_bundle_price(sample_item):
    bundle = Bundle(
        bundle_id=1,
        orderable_id=1,
        bundle_name="Menu",
        bundle_reduction=25,
        bundle_description="Menu classique",
        bundle_availability_start_date=datetime(2025, 10, 9, 12, 30, 0),
        bundle_availability_end_date=datetime(2025, 10, 9, 13, 0, 0),
        bundle_items={sample_item: 1},
    )

    assert bundle.bundle_price == sample_item.item_price * (1 - bundle.bundle_reduction / 100)


@pytest.mark.parametrize(
    "params, response",
    [
        ((datetime(2025, 10, 9, 12, 30, 0), datetime(2026, 10, 9, 12, 30, 0)), True),
        ((datetime(2025, 10, 9, 12, 30, 0), datetime(2025, 10, 9, 13, 0, 0)), False),
    ],
)
def test_bundle_check_availability_true(params, response, sample_item):
    bundle = Bundle(
        bundle_id=1,
        orderable_id=1,
        bundle_name="Menu",
        bundle_reduction=25,
        bundle_description="Menu classique",
        bundle_availability_start_date=params[0],
        bundle_availability_end_date=params[1],
        bundle_items={sample_item: 1},
    )

    assert bundle.check_availability() is response
