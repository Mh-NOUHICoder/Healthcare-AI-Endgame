import requests
import json

BASE_URL = "http://127.0.0.1:8000/router"

test_cases = [
    {
        "name": "TEST CASE 4.1: Condition-Specific Query",
        "payload": { "patient_id": "patient-001", "query": "How does my hypertension affect my risk for other diseases?" }
    },
    {
        "name": "TEST CASE 4.2: Medication Interaction with Condition",
        "payload": { "patient_id": "patient-001", "query": "Can I take decongestants with my current blood pressure medication?" }
    },
    {
        "name": "TEST CASE 5.1: Minimal Greeting",
        "payload": { "patient_id": "patient-001", "query": "Hello" }
    },
    {
        "name": "TEST CASE 5.2: Empty Query",
        "payload": { "patient_id": "patient-001", "query": "" }
    },
    {
        "name": "TEST CASE 5.3: Out of Scope",
        "payload": { "patient_id": "patient-001", "query": "What is the capital of France?" }
    }
]

def run_tests():
    with open("routing_test_suite.txt", "a", encoding="utf-8") as f:
        f.write("\n\n--- RUNNING REMAINING TESTS (CATEGORIES 4 & 5) ---\n")
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
