class ClinicaDomainError(Exception):
    """Base class for domain errors."""
    pass

class PatientNotFoundError(ClinicaDomainError):
    """Raised when a patient cannot be found in the FHIR server."""
    pass

class RoutingError(ClinicaDomainError):
    """Raised when the router fails to determine a specialty."""
    pass
