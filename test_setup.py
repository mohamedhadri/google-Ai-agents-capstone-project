import time
import subprocess
import sys
import os
import requests

def test_mcp_server():
    print("🚀 Starting Local MCP Server for testing...")
    server_path = os.path.join(os.path.dirname(__file__), "tools/mcp_server.py")
    process = subprocess.Popen([sys.executable, server_path], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    
    try:
        # Wait for server to start
        for i in range(10):
            try:
                response = requests.get("http://127.0.0.1:8000/gems")
                if response.status_code == 200:
                    print("✅ MCP Server is UP and responding!")
                    print(f"Data: {response.json()}")
                    return
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                print(f"Waiting for server... ({i+1}/10)")
        
        print("❌ MCP Server failed to start.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("🛑 Stopping server...")
        process.terminate()

if __name__ == "__main__":
    test_mcp_server()
