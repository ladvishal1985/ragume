import requests
import argparse
import os

BASE_URL = "http://127.0.0.1:8000"

def ingest_file(file_path):
    print(f"--- Ingesting {file_path} ---")
    
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return

    # Helper: Convert relative path to absolute for the API
    abs_path = os.path.abspath(file_path)
    
    payload = {
        "file_path": abs_path
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ingest", json=payload)
        if response.status_code == 200:
            print(f"[SUCCESS] {response.json()}")
        else:
            print(f"[ERROR] Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Connection Error: {e}")
        print("Ensure the server is running on port 8000.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest a PDF file into the Portfolio Agent.")
    parser.add_argument("file", help="Path to the PDF file to ingest")
    args = parser.parse_args()
    
    ingest_file(args.file)
