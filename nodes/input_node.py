from typing import Dict, Any
from base import RawBusinessData
from constants.messages import ErrorMessages
from utils.logger import setup_logger

logger = setup_logger(__name__)


class InputNode:
    def __init__(self, data_source: str = "API"):
        self.data_source = data_source
    
    def _fetch_from_api(self) -> Dict[str, Any]:
        """Example API data fetch"""
        return {
            "daily_revenue": 10000.0,
            "daily_cost": 6000.0,
            "number_of_customers": 100,
            "prev_day_revenue": 8000.0,
            "prev_day_cost": 5000.0,
            "prev_day_customers": 80
        }
    
    def __call__(self) -> RawBusinessData:
        """Fetch and validate input data using Pydantic model"""
        try:
            raw_data = self._fetch_from_api()
            validated_data = RawBusinessData.model_validate(raw_data)
            logger.info("Successfully validated input data")
            return validated_data
        except Exception as e:
            logger.error(f"Data validation failed: {str(e)}")
            raise ValueError(f"Input validation error: {str(e)}")
