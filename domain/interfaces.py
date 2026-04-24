from abc import ABC, abstractmethod
from typing import List
from .entities import Patient, Specialty

class IFHIRClient(ABC):
    @abstractmethod
    def get_patient(self, patient_id: str) -> Patient:
        """Fetch patient details from FHIR server."""
        pass

class IVectorStore(ABC):
    @abstractmethod
    def similarity_search(self, query: str, collection_name: str, k: int = 3) -> List[dict]:
        """Search vector store for relevant documents."""
        pass

class ILLM(ABC):
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """Invoke LLM with a prompt."""
        pass
        
    @abstractmethod
    def invoke_with_system(self, system_message: str, human_message: str) -> str:
        """Invoke LLM with system and human messages."""
        pass
