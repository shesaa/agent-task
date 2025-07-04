from enum import Enum

class AlertMessages(Enum):
    NEGATIVE_PROFIT = "ALERT: Negative profit detected"
    REVENUE_DROP = "WARNING: Significant revenue drop detected"
    COST_INCREASE = "WARNING: Significant cost increase detected"
    CAC_INCREASE = "ALERT: Customer Acquisition Cost (CAC) increased significantly"

class RecommendationMessages(Enum):
    REDUCE_COSTS = "Recommendation: Reduce costs or increase revenue to improve profitability"
    INCREASE_BUDGET = "Recommendation: Consider increasing advertising budget as sales are growing"
    INVESTIGATE_REVENUE = "Recommendation: Investigate reasons for revenue decline"
    REVIEW_COSTS = "Recommendation: Review operational costs for potential savings"
    REVIEW_MARKETING = "Recommendation: Review marketing campaigns for efficiency"

class ErrorMessages(Enum):
    MISSING_FIELD = "Missing required field: {}"
    INVALID_TYPE = "Field '{}' should be type {}, got {}"
    NEGATIVE_VALUE = "{} cannot be negative"
