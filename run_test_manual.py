from fastapi.testclient import TestClient
import sys

# Import app inside try/except to catch import errors gracefully
try:
    from src.api.main import app
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

print("Starting manual tests...")

try:
    with TestClient(app) as client:
        # Test Health
        print("Testing /health...")
        resp = client.get("/health")
        if resp.status_code != 200:
            print(f"Health check failed: {resp.status_code}")
            sys.exit(1)
        
        health_data = resp.json()
        if not health_data.get("kb_loaded"):
            print("WARNING: KB not loaded in health check")
        
        print("Health check OK")

        # Test Ask Known
        print("Testing /ask (known question)...")
        resp = client.post("/ask", json={"question": "o que é o nied?"})
        if resp.status_code != 200:
            print(f"Ask known failed: {resp.status_code}")
            print(resp.text)
            sys.exit(1)
        
        data = resp.json()
        if data["confidence"] <= 0.5:
            print(f"Confidence too low: {data['confidence']}")
            print(f"Response: {data}")
            sys.exit(1)
        
        if not data["sources"]["matched_triggers"]:
            print("No matched triggers found")
            sys.exit(1)
            
        print("Ask known OK")

        # Test Ask Unknown
        print("Testing /ask (unknown question)...")
        resp = client.post("/ask", json={"question": "qual a capital de marte?"})
        if resp.status_code != 200:
             print(f"Ask unknown failed: {resp.status_code}")
             sys.exit(1)
        
        data = resp.json()
        if data["confidence"] != 0.0:
            print(f"Confidence should be 0.0, got: {data['confidence']}")
        
        print("Ask unknown OK")

        print("ALL TESTS PASSED MANUALLY")

except Exception as e:
    print(f"Exception during test: {e}")
    sys.exit(1)
