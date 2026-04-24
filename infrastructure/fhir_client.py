import logging
from typing import List
from fhirpy import SyncFHIRClient
from domain.interfaces import IFHIRClient
from domain.entities import Patient
from domain.errors import PatientNotFoundError
from infrastructure.config import FHIR_SERVER_URL, FHIR_ACCESS_TOKEN

logger = logging.getLogger(__name__)

class FHIRClient(IFHIRClient):
    def __init__(self):
        headers = {}
        if FHIR_ACCESS_TOKEN:
            headers["Authorization"] = f"Bearer {FHIR_ACCESS_TOKEN}"
        self.client = SyncFHIRClient(FHIR_SERVER_URL, extra_headers=headers)

    def get_patient(self, patient_id: str) -> Patient:
        try:
            # Mock implementation for hackathon purposes if actual FHIR is not responding
            # fhir_patient = self.client.resources('Patient').search(_id=patient_id).first()
            # if not fhir_patient:
            #     raise PatientNotFoundError(f"Patient with ID {patient_id} not found.")
            
            # Simple mock patient
            return Patient(
                id=patient_id,
                age=45,
                gender="male",
                conditions=["Hypertension", "Type 2 Diabetes"],
                observations=["Blood Pressure: 140/90", "Heart Rate: 80"]
            )
        except Exception as e:
            logger.error(f"Error fetching patient {patient_id}: {e}")
            raise PatientNotFoundError(f"Failed to fetch patient {patient_id}: {e}")
