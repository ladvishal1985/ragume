import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoints():
    print("--- Testing RAG Endpoints ---")
    
    # 0. Test Root
    print("\n0. Testing Root...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Root Error: {e}")

    # 1. Test Ingestion
    print("\n1. Testing Ingestion...")
    ingest_payload = {
        "file_path": "d:/Users/vishal lad/workspace/first_python_project/data/sample_data.pdf"
    }
    try:
        response = requests.post(f"{BASE_URL}/ingest", json=ingest_payload)
        if response.status_code == 200:
            print(f"[SUCCESS] Ingestion Check: {response.json()}")
        else:
            print(f"[ERROR] Ingestion Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Connection Error during Ingestion: {e}")
        return

    # 2. Test Retrieval/Generation
    print("\n2. Testing Agent Query...")
    agent_payload = {
        "message": "What is this document about?"
    }
    try:
        response = requests.post(f"{BASE_URL}/agent", json=agent_payload)
        if response.status_code == 200:
            print(f"[SUCCESS] Agent Response: {response.json()}")
        else:
            print(f"[ERROR] Agent Query Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Connection Error during Query: {e}")

if __name__ == "__main__":
    test_endpoints()
