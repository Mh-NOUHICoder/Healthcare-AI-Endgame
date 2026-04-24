from langgraph.graph import StateGraph, END
from application.state import ClinicaState
from domain.interfaces import IFHIRClient, IVectorStore, ILLM
from domain.entities import Specialty

def build_graph(fhir_client: IFHIRClient, vector_store: IVectorStore, llm: ILLM):
    def fetch_patient_data(state: ClinicaState):
        try:
            patient = fhir_client.get_patient(state["patient_id"])
            return {
                "patient_age": patient.age,
                "symptoms": patient.observations,
                "conditions": patient.conditions,
                "error": None
            }
        except Exception as e:
            return {"error": str(e)}

    def router_node(state: ClinicaState):
        if state.get("error"):
            return state

        specialties = Specialty.list_all()
        prompt = f"""
        Given the following patient query, determine the medical specialty collection to query.
        Options: {", ".join(specialties)}
        
        Patient query: {state["query"]}
        Patient age: {state["patient_age"]}
        Patient conditions: {", ".join(state["conditions"])}
        
        Respond with ONLY the exact name of one of the options provided above.
        """
        response = llm.invoke(prompt).strip().lower()
        
        # dynamic match
        target = "general_practice" # Default fallback
        for s in specialties:
            if s in response:
                target = s
                break
            
        return {"target_collection": target}

    def retriever_node(state: ClinicaState):
        if state.get("error"):
            return state
            
        collection = state["target_collection"]
        docs = vector_store.similarity_search(state["query"], collection, k=3)
        return {"retrieved_docs": docs}

    def responder_node(state: ClinicaState):
        if state.get("error"):
            return state
            
        retrieved_docs = state.get("retrieved_docs", [])
        
        if not retrieved_docs:
            context = "NO CONTEXT AVAILABLE. Do not provide specific medical advice or citations."
        else:
            context = "\n".join([f"Source: {d['source']}, Page: {d['page']}\n{d['content']}" for d in retrieved_docs])
        
        system_prompt = """You are a helpful medical assistant. Generate a structured clinical report based on the context.
        Respond in a structured format:
        SUMMARY: <brief summary>
        ASSESSMENT: <clinical assessment based on query and context>
        PLAN: <proposed next steps>
        RECOMMENDATIONS: <list of specific recommendations>
        
        You MUST include citations in the format '(source: filename.pdf, page X)' at the end of relevant sentences.
        If NO CONTEXT AVAILABLE is stated, inform the patient but provide general safety guidance."""
        
        human_prompt = f"""
        Specialty: {state["target_collection"]}
        Patient Info: Age {state["patient_age"]}, Conditions: {", ".join(state["conditions"])}
        Context:
        {context}
        
        Patient Query: {state["query"]}
        """
        
        full_response = llm.invoke_with_system(system_prompt, human_prompt)
        
        # Parse the structured response
        import re
        report_data = {
            "summary": "",
            "assessment": "",
            "plan": "",
            "recommendations": [],
            "specialty_specific_data": {}
        }
        
        sections = re.split(r"(SUMMARY|ASSESSMENT|PLAN|RECOMMENDATIONS):", full_response)
        for i in range(1, len(sections), 2):
            key = sections[i].lower()
            content = sections[i+1].strip()
            if key == "recommendations":
                report_data[key] = [r.strip("- ").strip() for r in content.split("\n") if r.strip()]
            else:
                report_data[key] = content

        # Extract citations
        citation_pattern = r"\(source:\s*['\"]?(.*?)['\"]?,\s*page[:\s]*(\d+)\)"
        matches = re.findall(citation_pattern, full_response, re.IGNORECASE)
        
        citations = []
        seen = set()
        for source, page in matches:
            if source.lower() == "filename.pdf" and retrieved_docs:
                source = retrieved_docs[0]["source"]
            key = f"{source}-{page}"
            if key not in seen:
                citations.append({"source": source, "page": int(page)})
                seen.add(key)
        
        if not citations and retrieved_docs:
            for doc in retrieved_docs:
                key = f"{doc['source']}-{doc['page']}"
                if key not in seen:
                    citations.append({"source": doc["source"], "page": doc["page"]})
                    seen.add(key)
        
        return {
            "final_answer": full_response, 
            "clinical_report": report_data,
            "citations": citations
        }

    def route_after_fetch(state: ClinicaState):
        if state.get("error"):
            return END
        return "router"

    workflow = StateGraph(ClinicaState)
    
    workflow.add_node("fetch_patient", fetch_patient_data)
    workflow.add_node("router", router_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("responder", responder_node)
    
    workflow.set_entry_point("fetch_patient")
    workflow.add_conditional_edges("fetch_patient", route_after_fetch)
    workflow.add_edge("router", "retriever")
    workflow.add_edge("retriever", "responder")
    workflow.add_edge("responder", END)
    
    return workflow.compile()
