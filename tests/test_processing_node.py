from nodes import ProcessingNode
from base import RawBusinessData, ProcessedBusinessData
import pytest


def test_processing_node_calculations(sample_raw_data):
    raw_data = RawBusinessData.model_validate(sample_raw_data)
    node = ProcessingNode()
    result = node(raw_data)
    
    assert isinstance(result, ProcessedBusinessData)
    assert result.profit == 4000.0  # 10000 - 6000
    assert result.revenue_change_pct == 25.0  # ((10000-8000)/8000)*100
    assert result.current_cac == 60.0  # 6000/100
    assert result.cac_change_pct == pytest.approx(-4)  # ((60-62.5)/62.5)*100

