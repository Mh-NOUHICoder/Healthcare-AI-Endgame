import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000/router"

test_cases = [
    # Category 1: Cardiology
    {"id": "1.1", "name": "Direct Chest Pain", "payload": {"patient_id": "patient-001", "query": "I am experiencing sharp chest pain and shortness of breath."}},
    {"id": "1.2", "name": "High Blood Pressure Inquiry", "payload": {"patient_id": "patient-001", "query": "What are the long-term risks of having a blood pressure of 140/90?"}},
    {"id": "1.3", "name": "Heart Palpitations", "payload": {"patient_id": "patient-001", "query": "My heart feels like it is skipping beats lately, especially at night."}},
    
    # Category 2: Pediatrics
    {"id": "2.1", "name": "Infant Fever", "payload": {"patient_id": "patient-001", "query": "My 6-month-old has a fever of 102F and is very fussy."}},
    {"id": "2.2", "name": "Childhood Vaccinations", "payload": {"patient_id": "patient-001", "query": "What is the recommended schedule for the MMR vaccine?"}},
    {"id": "2.3", "name": "Pediatric Rash", "payload": {"patient_id": "patient-001", "query": "My toddler has a red bumpy rash after eating strawberries."}},
    
    # Category 3: Drug Safety
    {"id": "3.1", "name": "Drug Interactions", "payload": {"patient_id": "patient-001", "query": "Is it safe to take Metformin with Ibuprofen?"}},
    {"id": "3.2", "name": "Side Effects", "payload": {"patient_id": "patient-001", "query": "I started taking Lisinopril and now I have a persistent dry cough. Is this normal?"}},
    {"id": "3.3", "name": "Dosage Safety", "payload": {"patient_id": "patient-001", "query": "What is the maximum safe daily dose of acetaminophen for an adult?"}},
    
    # Category 4: Context-Aware
    {"id": "4.1", "name": "Condition-Specific Query", "payload": {"patient_id": "patient-001", "query": "How does my hypertension affect my risk for other diseases?"}},
    {"id": "4.2", "name": "Medication Interaction with Condition", "payload": {"patient_id": "patient-001", "query": "Can I take decongestants with my current blood pressure medication?"}},
    
    # Category 5: Edge Cases
    {"id": "5.1", "name": "Minimal Greeting", "payload": {"patient_id": "patient-001", "query": "Hello"}},
    {"id": "5.2", "name": "Empty Query", "payload": {"patient_id": "patient-001", "query": ""}},
    {"id": "5.3", "name": "Out of Scope", "payload": {"patient_id": "patient-001", "query": "What is the capital of France?"}}
]

def run_all_tests():
    print("Starting full test suite execution...")
    results = []
    
    for tc in test_cases:
        print(f"Running Test {tc['id']}: {tc['name']}...")
        try:
            response = requests.post(BASE_URL, json=tc['payload'])
            results.append({
                "test_id": tc['id'],
                "name": tc['name'],
                "payload": tc['payload'],
                "status": response.status_code,
                "response": response.json()
            })
        except Exception as e:
            results.append({
                "test_id": tc['id'],
                "name": tc['name'],
                "payload": tc['payload'],
                "error": str(e)
            })

    output_file = "routing_test_results_final.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Clinica-Router AI: Final Test Suite Results\n")
        f.write("# Generated after full database population\n\n")
        
        for res in results:
            f.write("="*80 + "\n")
            f.write(f"TEST {res['test_id']}: {res['name']}\n")
            f.write(f"Payload: {json.dumps(res['payload'], indent=2)}\n")
            f.write("-" * 40 + "\n")
            if "error" in res:
                f.write(f"ERROR: {res['error']}\n")
            else:
                f.write(f"Status: {res['status']}\n")
                f.write(f"Response: {json.dumps(res['response'], indent=2)}\n")
            f.write("\n")
            
    print(f"Full results saved to {output_file}")

if __name__ == "__main__":
    run_all_tests()
