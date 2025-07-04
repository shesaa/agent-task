from datetime import date
from base import RawBusinessData, ProcessedBusinessData
from constants.configure import AnalysisConfig
import pytest


@pytest.fixture
def sample_raw_data():
    return {
        "daily_revenue": 10000.0,
        "daily_cost": 6000.0,
        "number_of_customers": 100,
        "prev_day_revenue": 8000.0,
        "prev_day_cost": 5000.0,
        "prev_day_customers": 80
    }

@pytest.fixture
def sample_processed_data():
    return {
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

@pytest.fixture
def analysis_config():
    return AnalysisConfig()
