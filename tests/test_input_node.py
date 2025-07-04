from unittest.mock import patch
from nodes import InputNode
from base import RawBusinessData
from pydantic import ValidationError
import pytest


def test_input_node_returns_valid_model(sample_raw_data):
    with patch.object(InputNode, '_fetch_from_api', return_value=sample_raw_data):
        node = InputNode()
        result = node()
        assert isinstance(result, RawBusinessData)
        assert result.daily_revenue == 10000.0

def test_input_node_handles_invalid_data():
    invalid_data = {
        "daily_revenue": -10000.0,  # Negative value
        "daily_cost": 6000.0,
        "number_of_customers": 100,
        "prev_day_revenue": 8000.0,
        "prev_day_cost": 5000.0
    }
    with patch.object(InputNode, '_fetch_from_api', return_value=invalid_data):
        node = InputNode()
        with pytest.raises(ValueError):
            node()

def test_input_node_handles_missing_fields():
    incomplete_data = {
        "daily_revenue": 10000.0,
        "daily_cost": 6000.0,
        "number_of_customers": 100,
        "prev_day_cost": 5000.0
        # Missing prev_day_revenue
    }
    with patch.object(InputNode, '_fetch_from_api', return_value=incomplete_data):
        node = InputNode()
        with pytest.raises(ValueError):
            node()
