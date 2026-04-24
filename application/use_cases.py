from domain.interfaces import IFHIRClient, IVectorStore, ILLM
from application.graph import build_graph

_graph_instance = None

def run_router(patient_id: str, query: str, fhir_client: IFHIRClient, vector_store: IVectorStore, llm: ILLM) -> dict:
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = build_graph(fhir_client, vector_store, llm)
    
    graph = _graph_instance
    
    initial_state = {
        "patient_id": patient_id,
        "query": query,
        "patient_age": None,
        "symptoms": [],
        "conditions": [],
        "target_collection": None,
        "retrieved_docs": [],
        "final_answer": None,
        "citations": [],
        "error": None
    }
    
    # We could use a checkpointer here if configured
    result = graph.invoke(initial_state)
    
    if result is None:
        return {"error": "The AI workflow failed to produce a response. Please check if your LLM API keys are valid."}
        
    if result.get("error"):
        return {"error": result["error"]}
        
    return {
        "answer": result.get("final_answer", "I couldn't generate a specific answer for this query."),
        "clinical_report": result.get("clinical_report"),
        "citations": result.get("citations", []),
        "specialty": result.get("target_collection", "general_practice")
    }
