from nodes import RecommendationNode
from base import ProcessedBusinessData
from constants.messages import AlertMessages, RecommendationMessages
import pytest


def test_recommendation_node_positive_profit(sample_processed_data, analysis_config):
    processed_data = ProcessedBusinessData.model_validate(sample_processed_data)
    node = RecommendationNode(analysis_config)
    result = node(processed_data)
    
    assert RecommendationMessages.INCREASE_BUDGET.value in result["recommendations"]
    assert AlertMessages.NEGATIVE_PROFIT.value not in result["alerts"]

def test_recommendation_node_negative_profit(analysis_config):
    data = {
        "daily_revenue": 5000.0,
        "daily_cost": 6000.0,
        "number_of_customers": 50,
        "prev_day_revenue": 8000.0,
        "prev_day_cost": 5000.0,
        "prev_day_customers": 80,
        "profit": -1000.0,
        "revenue_change_pct": -37.5,
        "cost_change_pct": 20.0,
        "current_cac": 120.0,
        "cac_change_pct": 50.0
    }
    processed_data = ProcessedBusinessData.model_validate(data)
    node = RecommendationNode(analysis_config)
    result = node(processed_data)
    
    assert AlertMessages.NEGATIVE_PROFIT.value in result["alerts"]
    assert AlertMessages.REVENUE_DROP.value in result["alerts"]
    assert RecommendationMessages.REDUCE_COSTS.value in result["recommendations"]

def test_recommendation_node_with_none_values(analysis_config):
    data = {
        "daily_revenue": 10000.0,
        "daily_cost": 6000.0,
        "number_of_customers": 20,
        "prev_day_revenue": 2000.0,
        "prev_day_cost": 5000.0,
        "prev_day_customers": 5,
        "profit": 4000.0,
        "revenue_change_pct": float('inf'),
        "cost_change_pct": 20.0,
        "current_cac": None,
        "cac_change_pct": None
    }
    processed_data = ProcessedBusinessData.model_validate(data)
    node = RecommendationNode(analysis_config)
    result = node(processed_data)
    
    assert AlertMessages.CAC_INCREASE.value not in result["alerts"]
    assert RecommendationMessages.REVIEW_MARKETING.value not in result["recommendations"]
