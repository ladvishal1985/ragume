import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def chat():
    print("--- Portfolio Chatbot (Console Mode) ---")
    print("Type 'exit' or 'quit' to stop.")
    print("Ensure the server is running: python -m uvicorn app.main:app --port 8000")
    print("----------------------------------------")

    # verify server is up
    try:
        requests.get(f"{BASE_URL}/")
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Could not connect to {BASE_URL}. Is the server running?")
        return

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            if not user_input.strip():
                continue

            payload = {"message": user_input}
            response = requests.post(f"{BASE_URL}/agent", json=payload)
            
            if response.status_code == 200:
                answer = response.json().get("response", "No response field")
                print(f"Agent: {answer}")
            else:
                print(f"[Error] {response.status_code}: {response.text}")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"[Error] {e}")

if __name__ == "__main__":
    chat()
