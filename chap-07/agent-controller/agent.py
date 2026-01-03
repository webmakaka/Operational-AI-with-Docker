"""
Worker Agent - Autonomous agent that:
1. Registers with the controller
2. Pulls tasks from the queue
3. Processes tasks using LLM
4. Reports results back to controller
"""

import redis
import json
import time
import os
import requests
from datetime import datetime

class WorkerAgent:
    """Autonomous worker agent"""
    
    def __init__(self, redis_url, agent_name, agent_type, controller_url, model_url, model_name):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.controller_url = controller_url
        self.model_url = model_url
        self.model_name = model_name
        
    def register(self):
        """Register with the controller"""
        print(f"📝 Registering agent: {self.agent_name}")
        try:
            response = requests.post(
                f"{self.controller_url}/api/agents/register",
                json={"name": self.agent_name, "type": self.agent_type},
                timeout=5
            )
            if response.status_code == 200:
                print(f"✅ Successfully registered with controller")
                return True
        except Exception as e:
            print(f"⚠️  Could not register with controller: {e}")
        return False
    
    def send_heartbeat(self):
        """Send heartbeat to controller"""
        try:
            requests.post(
                f"{self.controller_url}/api/agents/{self.agent_name}/heartbeat",
                timeout=5
            )
        except:
            pass  # Silently fail heartbeats
    
    def get_task(self):
        """Get next task from controller"""
        try:
            response = requests.post(
                f"{self.controller_url}/api/tasks/dequeue",
                json={"agent_name": self.agent_name},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"⚠️  Could not get task: {e}")
        return None
    
    def complete_task(self, task_id, success, result):
        """Report task completion to controller"""
        try:
            requests.post(
                f"{self.controller_url}/api/tasks/{task_id}/complete",
                json={"success": success, "result": result},
                timeout=5
            )
        except Exception as e:
            print(f"⚠️  Could not complete task: {e}")
    
    def process_task(self, task):
        """Process a task using LLM"""
        print(f"\n{'='*60}")
        print(f"🎯 Processing Task: {task['id']}")
        print(f"📝 Description: {task['description']}")
        print(f"{'='*60}\n")
        
        # Use LLM to analyze and process the task
        try:
            response = requests.post(
                f"{self.model_url}/chat/completions",
                json={
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": f"You are a {self.agent_type} agent. Provide concise, actionable responses."},
                        {"role": "user", "content": f"Task: {task['description']}\n\nProvide a brief summary of what you would do to complete this task."}
                    ],
                    "max_tokens": 150,
                    "temperature": 0.7
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                result = data['choices'][0]['message']['content']
                print(f"✅ Task completed successfully")
                print(f"📊 Result: {result[:100]}...")
                return True, result
            else:
                print(f"❌ Task failed: HTTP {response.status_code}")
                return False, f"HTTP error: {response.status_code}"
                
        except Exception as e:
            print(f"❌ Task failed: {str(e)}")
            return False, str(e)
    
    def run(self):
        """Main agent loop"""
        print(f"\n🤖 Starting Worker Agent: {self.agent_name}")
        print(f"   Type: {self.agent_type}")
        print(f"   Controller: {self.controller_url}")
        print(f"   Model: {self.model_name}\n")
        
        # Register with controller
        self.register()
        
        # Agent loop
        heartbeat_counter = 0
        while True:
            try:
                # Send heartbeat every 10 iterations
                heartbeat_counter += 1
                if heartbeat_counter % 10 == 0:
                    self.send_heartbeat()
                
                # Try to get a task
                task = self.get_task()
                
                if task:
                    # Process the task
                    success, result = self.process_task(task)
                    
                    # Report completion
                    self.complete_task(task['id'], success, result)
                    
                    # Brief pause before next task
                    time.sleep(2)
                else:
                    # No tasks available, wait
                    print(f"💤 No tasks available, waiting...")
                    time.sleep(5)
                    
            except KeyboardInterrupt:
                print(f"\n👋 Agent {self.agent_name} shutting down...")
                break
            except Exception as e:
                print(f"⚠️  Error in agent loop: {e}")
                time.sleep(5)


def main():
    # Configuration
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    agent_name = os.getenv('AGENT_NAME', 'worker-1')
    agent_type = os.getenv('AGENT_TYPE', 'general')
    controller_url = os.getenv('CONTROLLER_URL', 'http://controller:8000')
    model_url = os.getenv('LLM_URL', 'http://localhost:8080/v1')
    model_name = os.getenv('LLM_MODEL', 'ai/smollm2:360m-instruct-q4_K_M')
    
    # Wait for controller to be ready
    print("⏳ Waiting for controller to be ready...")
    for i in range(30):
        try:
            requests.get(f"{controller_url}/api/stats", timeout=2)
            print("✅ Controller is ready!")
            break
        except:
            time.sleep(1)
    
    # Start agent
    agent = WorkerAgent(redis_url, agent_name, agent_type, controller_url, model_url, model_name)
    agent.run()


if __name__ == "__main__":
    main()
