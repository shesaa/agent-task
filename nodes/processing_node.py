from typing import Dict, Any
from base import RawBusinessData, ProcessedBusinessData
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ProcessingNode:
    def __init__(self, cac_threshold: float = 0.2):
        self.cac_threshold = cac_threshold
    
    def _calculate_percent_change(self, current: float, previous: float) -> float:
        """Calculate percentage change"""
        if previous == 0:
            return float('inf')
        return (current - previous) / previous * 100
    
    def __call__(self, data: RawBusinessData) -> ProcessedBusinessData:
        """Process business data and return validated processed data"""
        try:
            # Convert to dict for processing
            data_dict = data.model_dump()
            
            # Calculate metrics
            data_dict['profit'] = data.daily_revenue - data.daily_cost
            data_dict['revenue_change_pct'] = self._calculate_percent_change(
                data.daily_revenue, data.prev_day_revenue)
            data_dict['cost_change_pct'] = self._calculate_percent_change(
                data.daily_cost, data.prev_day_cost)
            
            # Calculate CAC metrics
            if data.number_of_customers > 0:
                data_dict['current_cac'] = data.daily_cost / data.number_of_customers
                if data.prev_day_customers and data.prev_day_customers > 0:
                    prev_cac = data.prev_day_cost / data.prev_day_customers
                    data_dict['cac_change_pct'] = self._calculate_percent_change(
                        data_dict['current_cac'], prev_cac)
            
            # Validate and return processed data
            processed_data = ProcessedBusinessData.model_validate(data_dict)
            logger.info("Successfully processed business data")
            return processed_data
            
        except Exception as e:
            logger.error(f"Data processing failed: {str(e)}")
            raise ValueError(f"Processing error: {str(e)}")
