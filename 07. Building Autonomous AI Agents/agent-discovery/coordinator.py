import requests
import time
import os

def main():
    worker_url = os.getenv('WORKER_URL', 'http://worker:8000')
    
    print("🎯 Coordinator Agent Starting...")
    print(f"   Worker URL: {worker_url}\n")
    
    # Wait for workers to be ready
    print("⏳ Waiting for workers...")
    time.sleep(3)
    
    task_id = 1
    
    while True:
        try:
            # Call worker using service name - DNS resolves automatically
            print(f"\n📤 Sending task #{task_id} to worker...")
            response = requests.get(f"{worker_url}/process", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Task completed by: {data['worker_id']}")
                print(f"   Hostname: {data['hostname']}")
                print(f"   Message: {data['message']}")
            else:
                print(f"❌ Worker returned: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error calling worker: {e}")
        
        task_id += 1
        time.sleep(3)

if __name__ == "__main__":
    main()
