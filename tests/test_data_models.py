from pydantic import ValidationError
from base import RawBusinessData, ProcessedBusinessData
import pytest


def test_raw_data_validation():
    # Test valid data
    valid_data = {
        "daily_revenue": 10000.0,
        "daily_cost": 6000.0,
        "number_of_customers": 100,
        "prev_day_revenue": 8000.0,
        "prev_day_cost": 5000.0,
        "prev_day_customers": 50
    }
    assert RawBusinessData.model_validate(valid_data)

def test_raw_data_invalid_types():
    invalid_data = {
        "daily_revenue": "10000",  # String instead of float
        "daily_cost": 6000.0,
        "number_of_customers": 100,
        "prev_day_revenue": 8000.0,
        "prev_day_cost": 5000.0
    }
    with pytest.raises(ValidationError):
        RawBusinessData.model_validate(invalid_data)

def test_processed_data_calculations():
    data = {
        "daily_revenue": 10000.0,
        "daily_cost": 6000.0,
        "number_of_customers": 100,
        "prev_day_revenue": 8000.0,
        "prev_day_cost": 5000.0,
        "prev_day_customers": 80,
        "profit": 4000.0,
        "revenue_change_pct": 25.0,
        "cost_change_pct": 20.0,
        "current_cac": 60.0,
        "cac_change_pct": 20.0
    }
    processed = ProcessedBusinessData.model_validate(data)
    assert processed.profit == 4000.0
    assert processed.cac_change_pct == 20.0
