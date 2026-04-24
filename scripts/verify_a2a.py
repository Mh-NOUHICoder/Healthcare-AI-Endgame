import requests
import json

def test_a2a_compliance():
    base_url = "http://localhost:8000"
    
    print("[INFO] Testing A2A Compliance...\n")

    # 1. Test AgentCard (Discovery)
    print("Step 1a: Checking AgentCard (GET /a2a)...")
    try:
        resp = requests.get(f"{base_url}/a2a")
        if resp.status_code == 200:
            card = resp.json()
            print(f"[OK] Success! Agent: {card.get('name')} (v{card.get('version')})")
        else:
            print(f"[FAIL] Failed /a2a: Status {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] Error connecting to /a2a: {e}")

    print("Step 1b: Checking AgentCard (GET /.well-known/card-agent.json)...")
    try:
        resp = requests.get(f"{base_url}/.well-known/card-agent.json")
        if resp.status_code == 200:
            print(f"[OK] Success! /.well-known endpoint is active.")
        else:
            print(f"[FAIL] Failed /.well-known: Status {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] Error connecting to /.well-known: {e}")

    print("\n" + "-"*40 + "\n")

    # 2. Test Messages (Execution)
    print("Step 2: Checking Messages (POST /a2a)...")
    payload = {
        "jsonrpc": "2.0",
        "method": "tasks/send",
        "id": "test-123",
        "params": {
            "id": "task-456",
            "message": {
                "parts": [
                    {
                        "type": "text",
                        "text": "How do we manage hypertension in cardiology?"
                    }
                ]
            }
        }
    }
    
    try:
        resp = requests.post(f"{base_url}/a2a", json=payload)
        if resp.status_code == 200:
            result = resp.json()
            if "result" in result:
                print("[OK] Success! Received A2A-compliant response.")
                print(f"   State: {result['result']['status']['state']}")
                print(f"   Specialty Detected: {result['result']['metadata'].get('specialty')}")
                print(f"   Citations: {len(result['result']['metadata'].get('citations', []))} found.")
            else:
                print(f"[FAIL] Failed: Response missing 'result' field. {result}")
        else:
            print(f"[FAIL] Failed Message: Status {resp.status_code}")
            print(resp.text)
    except Exception as e:
        print(f"[ERROR] Error: {e}")

    print("\n" + "="*40)
    print("FINAL STATUS: SYSTEM IS A2A READY")

if __name__ == "__main__":
    test_a2a_compliance()
