import sys
import os
sys.path.append(os.getcwd())

from infrastructure.fhir_client import FHIRClient
from infrastructure.vector_store import VectorStore
from infrastructure.llm_wrapper import LLMWrapper
from application.use_cases import run_router

fhir_client = FHIRClient()
vector_store = VectorStore()
llm = LLMWrapper()

try:
    print("Testing run_router...")
    res = run_router("test-p", "hello", fhir_client, vector_store, llm)
    print("Result:", res)
except Exception as e:
    import traceback
    traceback.print_exc()
