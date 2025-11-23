import json
import uuid
import requests

# The Chief Wellness Officer is now the single entry point on port 8002
API_URL = "http://localhost:8002/tasks/send"
USER_ID = "user123"

def send_message(message: str) -> None:
    # Construct JSON-RPC 2.0 payload
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "tasks/send",
        "params": {
            "task": {
                "input": {
                    "text": message
                }
            }
        }
    }

    print(f"\n--> Sending to CWO ({API_URL}):\n", json.dumps(payload, indent=2))
    
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        print("Status:", response.status_code)
        
        if response.status_code == 200:
            data = response.json()
            # print("Raw Response:\n", json.dumps(data, indent=2))
            
            # Extract the text output if available
            if "result" in data and "output" in data["result"]:
                output_text = data["result"]["output"].get("text", "No text response")
                print(f"\n🤖 CWO Reply:\n{output_text}")
            elif "error" in data:
                print(f"\n❌ JSON-RPC Error: {data['error']}")
        else:
            print("Error Response:", response.text)
            
    except Exception as e:
        print(f"Request failed: {e}")


def interactive_chat():
    print("--- Wellness App (Single Entry Point) ---")
    print("Target: Chief Wellness Officer (Port 8002)")
    print("Note: Ensure ALL 3 agents are running (Ports 8000, 8001, 8002).")
    print("(Ctrl+C to exit)\n")

    while True:
        try:
            user_text = input("\nYou > ").strip()
        except KeyboardInterrupt:
            print("\nExiting chat tester.")
            break

        if not user_text:
            continue

        send_message(user_text)


if __name__ == "__main__":
    interactive_chat()
