import requests
import json

BASE_URL = "http://127.0.0.1:8000/router"

test_cases = [
    {
        "name": "TEST CASE 3.1: Drug Interactions",
        "payload": { "patient_id": "patient-001", "query": "Is it safe to take Metformin with Ibuprofen?" }
    },
    {
        "name": "TEST CASE 3.2: Side Effects",
        "payload": { "patient_id": "patient-001", "query": "I started taking Lisinopril and now I have a persistent dry cough. Is this normal?" }
    },
    {
        "name": "TEST CASE 3.3: Dosage Safety",
        "payload": { "patient_id": "patient-001", "query": "What is the maximum safe daily dose of acetaminophen for an adult?" }
    }
]

def run_tests():
    with open("routing_test_suite.txt", "a", encoding="utf-8") as f:
        f.write("\n\n--- RUNNING MISSING DRUG SAFETY TESTS ---\n")
        for tc in test_cases:
            print(f"Running {tc['name']}...")
            try:
                response = requests.post(BASE_URL, json=tc['payload'])
                f.write(f"\n{tc['name']}\n")
                f.write(f"Payload: {json.dumps(tc['payload'])}\n")
                f.write(f"Response: {json.dumps(response.json(), indent=2)}\n")
                f.write(f"Status Code: {response.status_code}\n")
            except Exception as e:
                f.write(f"\n{tc['name']} FAILED: {str(e)}\n")

if __name__ == "__main__":
    run_tests()
