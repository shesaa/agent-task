from typing import Dict, Any
from base import ProcessedBusinessData
from constants.messages import AlertMessages, RecommendationMessages
from constants.configure import AnalysisConfig
from utils.logger import setup_logger

logger = setup_logger(__name__)


class RecommendationNode:
    def __init__(self, config: AnalysisConfig):
        self.config = config
    
    def __call__(self, data: ProcessedBusinessData) -> Dict[str, Any]:
        """Generate recommendations based on validated processed data"""
        try:
            output = {
                "alerts": [],
                "recommendations": [],
                "metrics": {
                    "profit": data.profit,
                    "revenue_change": data.revenue_change_pct,
                    "cost_change": data.cost_change_pct,
                    "current_cac": data.current_cac,
                    "cac_change": data.cac_change_pct
                }
            }
            
            # Profit analysis
            if data.profit is not None and data.profit < self.config.PROFIT_THRESHOLD:
                output["alerts"].append(AlertMessages.NEGATIVE_PROFIT.value)
                output["recommendations"].append(RecommendationMessages.REDUCE_COSTS.value)
            
            # Revenue change analysis
            if data.revenue_change_pct is not None:
                if data.revenue_change_pct > self.config.REVENUE_CHANGE_THRESHOLD:
                    output["recommendations"].append(RecommendationMessages.INCREASE_BUDGET.value)
                elif data.revenue_change_pct < -self.config.REVENUE_CHANGE_THRESHOLD:
                    output["alerts"].append(AlertMessages.REVENUE_DROP.value)
                    output["recommendations"].append(RecommendationMessages.INVESTIGATE_REVENUE.value)
            
            # Cost change analysis
            if data.cost_change_pct is not None and data.cost_change_pct > self.config.COST_CHANGE_THRESHOLD:
                output["alerts"].append(AlertMessages.COST_INCREASE.value)
                output["recommendations"].append(RecommendationMessages.REVIEW_COSTS.value)
            
            # CAC analysis
            if data.cac_change_pct is not None and data.cac_change_pct > self.config.CAC_CHANGE_THRESHOLD:
                output["alerts"].append(AlertMessages.CAC_INCREASE.value)
                output["recommendations"].append(RecommendationMessages.REVIEW_MARKETING.value)
            
            logger.info("Generated recommendations successfully")
            return output
            
        except Exception as e:
            logger.error(f"Recommendation generation failed: {str(e)}")
            raise ValueError(f"Recommendation error: {str(e)}")