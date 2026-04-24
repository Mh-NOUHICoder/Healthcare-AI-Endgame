from fastapi import APIRouter, HTTPException, Request
from interfaces.schemas import RouterRequest, RouterResponse, A2ARequest
from application.use_cases import run_router
from infrastructure.fhir_client import FHIRClient
from infrastructure.vector_store import VectorStore
from infrastructure.llm_wrapper import LLMWrapper
from infrastructure.a2a_utils import build_a2a_response, build_a2a_error_response, extract_a2a_text
from domain.entities import Specialty
import uuid

router = APIRouter()

# Dependencies will be lazily instantiated inside use_cases to prevent reload hangs
fhir_client = None
vector_store = None
llm = None

def get_dependencies():
    global fhir_client, vector_store, llm
    if fhir_client is None:
        from infrastructure.fhir_client import FHIRClient
        fhir_client = FHIRClient()
    if vector_store is None:
        from infrastructure.vector_store import VectorStore
        vector_store = VectorStore()
    if llm is None:
        from infrastructure.llm_wrapper import LLMWrapper
        llm = LLMWrapper()
    return fhir_client, vector_store, llm

@router.get("/a2a")
@router.get("/.well-known/card-agent.json")
async def get_agent_card(request: Request):
    """
    Discovery endpoint: Returns the AgentCard.
    Supports both /a2a (standard) and /.well-known/card-agent.json (platform specific).
    Uses the request object to provide absolute URLs for better external discovery.
    """
    base_url = str(request.base_url).rstrip("/")
    specialties = Specialty.list_all()
    description = f"Intelligent medical inquiry router specializing in: {', '.join([s.replace('_', ' ').title() for s in specialties])}."
    
    return {
        "id": "clinica-router-ai",
        "name": "Clinica-Router AI",
        "author": "Healthcare AI Endgame",
        "description": description,
        "version": "1.1.0",
        "protocol": "A2A",
        "protocolVersion": "0.3.0",
        "preferredTransport": "JSONRPC",
        "supportedInterfaces": [
            {
                "url": f"{base_url}/a2a",
                "protocolBinding": "JSONRPC",
                "protocolVersion": "0.3.0"
            }
        ],
        "skills": [
            {
                "id": "medical_routing",
                "name": "Medical Specialty Routing",
                "description": "Routes medical queries to the correct clinical guidelines and extracts structured clinical reports with citations.",
                "tags": ["clinical", "healthcare"] + specialties,
                "examples": [
                    "What are the hypertension guidelines for adults?",
                    "Common side effects of ibuprofen in infants?",
                    "Current protocols for early-stage breast cancer treatment?"
                ]
            }
        ]
    }

@router.post("/a2a")
async def a2a_handler(request: A2ARequest):
    """
    Standardized A2A Message endpoint using JSON-RPC 2.0.
    """
    try:
        # 1. Extract context
        params = request.params or {}
        
        # Helper to get values from either Pydantic model or dict
        def get_val(obj, key, default=None):
            if hasattr(obj, key): return getattr(obj, key)
            if isinstance(obj, dict): return obj.get(key, default)
            return default

        task_id = get_val(params, "id", str(uuid.uuid4()))
        session_id = get_val(params, "sessionId", None)
        
        # 2. Extract query text
        params_dict = params.dict() if hasattr(params, "dict") else params
        query_text = extract_a2a_text(params_dict)
        
        # 3. Handle default/empty queries
        if not query_text.strip():
            return build_a2a_response(
                request.id, task_id, "COMPLETED",
                "Hello! I am Clinica-Router AI. How can I help you with medical guidelines today?",
                {"agent": "ClinicaRouter", "intent": "greeting"},
                session_id
            )

        # 4. Run the Agent Executor (LangGraph)
        # For simplicity in this MVP, we use a generic patient ID if not provided in A2A
        patient_id = "a2a-patient"
        dep_fhir, dep_vs, dep_llm = get_dependencies()
        result = run_router(patient_id, query_text, dep_fhir, dep_vs, dep_llm)

        if "error" in result and result["error"]:
            return build_a2a_error_response(request.id, -32603, result["error"])

        # 5. Format metadata for A2A
        metadata = {
            "agent": "ClinicaRouter",
            "specialty": result["specialty"],
            "clinical_report": result.get("clinical_report"),
            "citations": result["citations"],
            "intent": "medical_inquiry"
        }

        return build_a2a_response(
            request.id,
            task_id,
            "COMPLETED",
            result["answer"],
            metadata,
            session_id
        )

    except Exception as e:
        return build_a2a_error_response(request.id, -32603, str(e))

@router.post("/router", response_model=RouterResponse)
async def route_query(request: RouterRequest):
    dep_fhir, dep_vs, dep_llm = get_dependencies()
    result = run_router(request.patient_id, request.query, dep_fhir, dep_vs, dep_llm)
    
    if "error" in result and result["error"]:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return RouterResponse(
        answer=result["answer"],
        clinical_report=result.get("clinical_report"),
        citations=result["citations"],
        specialty=result["specialty"]
    )
