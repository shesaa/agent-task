from langgraph.graph import StateGraph
from nodes.input_node import InputNode
from nodes.processing_node import ProcessingNode
from nodes.recommendation_node import RecommendationNode
from constants.configure import AnalysisConfig
from typing import TypedDict, Optional, Dict, Any, List
import json


# Define the state structure
class AgentState(TypedDict):
    business_data: Dict[str, Any]
    processed_data: Dict[str, Any]
    recommendations: Dict[str, Any]
    errors: Optional[List[str]]


def create_workflow() -> StateGraph:
    # Initialize nodes
    input_node = InputNode(data_source="api")
    processing_node = ProcessingNode()
    recommendation_node = RecommendationNode(config=AnalysisConfig)
    
    # Create graph
    workflow = StateGraph(AgentState)
    
    # Add nodes with proper state handling
    def input_node_wrapper(state: AgentState) -> dict:
        return {"business_data": input_node()}
    
    def processing_node_wrapper(state: AgentState) -> dict:
        return {"processed_data": processing_node(state["business_data"])}
    
    def recommendation_node_wrapper(state: AgentState) -> dict:
        return {"recommendations": recommendation_node(state["processed_data"])}
    
    workflow.add_node("input", input_node_wrapper)
    workflow.add_node("process", processing_node_wrapper)
    workflow.add_node("recommend", recommendation_node_wrapper)
    
    # Define edges
    workflow.add_edge("input", "process")
    workflow.add_edge("process", "recommend")
    
    # Set entry and end points
    workflow.set_entry_point("input")
    workflow.set_finish_point("recommend")
    
    return workflow.compile()

def export_workflow():
    workflow = create_workflow()
    graph = workflow.get_graph()

    # Export PNG correctly
    with open("Studio.png", "wb") as f:
        f.write(graph.draw_mermaid_png())

    # Save Mermaid .mmd file
    with open("Studio.mmd", "w") as f:
        f.write(graph.draw_mermaid())


if __name__ == "__main__":
    export_workflow()

    app = create_workflow()
    
    # Run with empty initial state
    initial_state = AgentState(
        business_data=None,
        processed_data=None,
        recommendations=None
    )
    result = app.invoke(initial_state)
    print("Analysis Results:")
    print(json.dumps(result["recommendations"], indent=2))
