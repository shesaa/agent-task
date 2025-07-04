from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Any
from datetime import date
from constants.messages import ErrorMessages


class BaseBusinessData(BaseModel):
    """Base model for business data with common validation"""
    daily_revenue: float = Field(..., gt=0, description="Today's total revenue")
    daily_cost: float = Field(..., gt=0, description="Today's total costs")
    number_of_customers: int = Field(..., gt=0, description="Number of customers acquired")
    prev_day_revenue: float = Field(..., gt=0, description="Previous day's revenue")
    prev_day_cost: float = Field(..., gt=0, description="Previous day's costs")
    prev_day_customers: Optional[int] = Field(None, gt=0, description="Previous day's customers")


    @model_validator(mode='before')
    @classmethod
    def check_required_fields(cls, data: Any) -> Any:
        """Validate all required fields are present"""
        if isinstance(data, dict):
            missing_fields = [
                field for field in cls.model_fields
                if cls.model_fields[field].is_required and field not in data
            ]
            if missing_fields:
                raise ValueError(
                    ErrorMessages.MISSING_FIELD.value.format(', '.join(missing_fields))
                )
        return data

class RawBusinessData(BaseBusinessData):
    """Model for raw input data with additional validation"""
    
    @field_validator('daily_revenue', 'daily_cost', 'prev_day_revenue', 'prev_day_cost')
    @classmethod
    def validate_currency(cls, v: float) -> float:
        """Round currency values to 2 decimal places"""
        return round(v, 2)

class ProcessedBusinessData(RawBusinessData):
    """Model for processed data with calculated fields"""
    profit: Optional[float] = Field(None, description="Calculated profit (revenue - cost)")
    revenue_change_pct: Optional[float] = Field(None, description="Percentage change in revenue")
    cost_change_pct: Optional[float] = Field(None, description="Percentage change in costs")
    current_cac: Optional[float] = Field(None, description="Current Customer Acquisition Cost")
    cac_change_pct: Optional[float] = Field(None, description="Percentage change in CAC")

    @field_validator('revenue_change_pct', 'cost_change_pct', 'cac_change_pct', mode='before')
    @classmethod
    def handle_infinite_changes(cls, v: float) -> Optional[float]:
        """Convert infinite changes to None"""
        return None if v == float('inf') else v
