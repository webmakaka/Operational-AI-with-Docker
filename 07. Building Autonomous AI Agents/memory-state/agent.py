import redis
import json
import time
import os
import requests
from datetime import datetime

class AgentMemory:
    """Manages agent memory using Redis for persistence"""
    
    def __init__(self, redis_url, agent_name):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.agent_name = agent_name
        
    def remember_action(self, task_id, action, result, success):
        """Store an action and its result in memory"""
        memory_key = f"agent:{self.agent_name}:actions:{task_id}"
        action_record = {
            "action": action,
            "result": result,
            "success": success,
            "timestamp": datetime.utcnow().isoformat()
        }
        # Append to list of actions for this task
        self.redis.rpush(memory_key, json.dumps(action_record))
        print(f"📝 Remembered: Task {task_id} - {action} - {'✅ Success' if success else '❌ Failed'}")
        
    def get_past_actions(self, task_id):
        """Retrieve all past actions for a task"""
        memory_key = f"agent:{self.agent_name}:actions:{task_id}"
        actions = self.redis.lrange(memory_key, 0, -1)
        return [json.loads(a) for a in actions]
    
    def has_completed_task(self, task_id):
        """Check if a task was already completed successfully"""
        actions = self.get_past_actions(task_id)
        return any(a['success'] for a in actions)
    
    def get_failed_attempts(self, task_id):
        """Get all failed attempts for a task"""
        actions = self.get_past_actions(task_id)
        return [a for a in actions if not a['success']]
    
    def update_context(self, key, value):
        """Store general context information"""
        context_key = f"agent:{self.agent_name}:context:{key}"
        self.redis.set(context_key, json.dumps(value))
    
    def get_context(self, key):
        """Retrieve context information"""
        context_key = f"agent:{self.agent_name}:context:{key}"
        value = self.redis.get(context_key)
        return json.loads(value) if value else None


class TaskAgent:
    """
    Autonomous agent that follows the agent loop:
    Perceive → Reason → Plan → Act → Observe → Iterate
    """
    
    def __init__(self, memory, model_url, model_name):
        self.memory = memory
        self.model_url = model_url
        self.model_name = model_name
        
    def _call_llm(self, system_prompt, user_prompt, max_tokens=200):
        """Make a direct HTTP call to the model API"""
        try:
            response = requests.post(
                f"{self.model_url}/chat/completions",
                json={
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "max_tokens": max_tokens,
                    "temperature": 0.7
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except Exception as e:
            print(f"   ⚠️  LLM call failed: {e}")
            return f"Simple action based on task description"
        
    def perceive(self, tasks):
        """1. PERCEIVE: Monitor environment for new tasks"""
        print("\n🔍 PERCEIVE: Checking for tasks...")
        pending_tasks = []
        for task in tasks:
            if not self.memory.has_completed_task(task['id']):
                pending_tasks.append(task)
                print(f"   Found new task: {task['id']} - {task['description']}")
            else:
                print(f"   ⏭️  Skipping already completed task: {task['id']}")
        return pending_tasks
    
    def reason(self, task):
        """2. REASON: Analyze the task using LLM and past context"""
        print(f"\n🧠 REASON: Analyzing task {task['id']}...")
        
        # Check for past failures
        failed_attempts = self.memory.get_failed_attempts(task['id'])
        
        context = f"Task: {task['description']}\n"
        if failed_attempts:
            context += f"\nPrevious failed attempts:\n"
            for attempt in failed_attempts:
                context += f"- {attempt['action']}: {attempt['result']}\n"
            context += "\nLearn from these failures and suggest a different approach."
        
        # Use LLM to reason about the task
        analysis = self._call_llm(
            system_prompt="You are a helpful task planning assistant. Provide concise, actionable analysis.",
            user_prompt=f"{context}\n\nAnalyze this task and explain the approach needed.",
            max_tokens=200
        )
        
        print(f"   Analysis: {analysis}")
        return analysis
    
    def plan(self, task, analysis):
        """3. PLAN: Create action plan based on analysis"""
        print(f"\n📋 PLAN: Creating action plan for task {task['id']}...")
        
        # Use LLM to create a specific action plan
        action = self._call_llm(
            system_prompt="You are a task execution planner. Provide a clear, single action to take.",
            user_prompt=f"Based on this analysis: {analysis}\n\nWhat specific action should be taken for task: {task['description']}?\nRespond with just the action in one sentence.",
            max_tokens=100
        )
        
        action = action.strip()
        print(f"   Planned action: {action}")
        return action
    
    def act(self, task, action):
        """4. ACT: Execute the planned action"""
        print(f"\n⚡ ACT: Executing action for task {task['id']}...")
        print(f"   Action: {action}")
        
        # Simulate action execution
        # In a real agent, this would interact with external systems
        time.sleep(1)
        
        # Simulate success/failure based on task type
        if "error" in task['description'].lower():
            result = "Error: Failed to process"
            success = False
        else:
            result = f"Successfully completed: {action}"
            success = True
            
        return result, success
    
    def observe(self, task, action, result, success):
        """5. OBSERVE: Check results and update memory"""
        print(f"\n👁️  OBSERVE: Checking results for task {task['id']}...")
        print(f"   Result: {result}")
        print(f"   Status: {'✅ Success' if success else '❌ Failed'}")
        
        # Store action and result in memory
        self.memory.remember_action(task['id'], action, result, success)
        
        return success
    
    def iterate(self, task, success):
        """6. ITERATE: Decide next steps"""
        print(f"\n🔄 ITERATE: Determining next steps for task {task['id']}...")
        
        if success:
            print(f"   ✅ Task completed successfully. Moving to next task.")
            return "complete"
        else:
            failed_attempts = len(self.memory.get_failed_attempts(task['id']))
            if failed_attempts >= 3:
                print(f"   ⚠️  Too many failures ({failed_attempts}). Marking as failed.")
                return "failed"
            else:
                print(f"   🔁 Attempt {failed_attempts}/3 failed. Will retry with different approach.")
                return "retry"
    
    def run_loop(self, task):
        """Execute the complete agent loop for a task"""
        print(f"\n{'='*60}")
        print(f"🤖 AGENT LOOP STARTED for Task: {task['id']}")
        print(f"{'='*60}")
        
        max_retries = 3
        attempt = 0
        
        while attempt < max_retries:
            # 1. Perceive (already done in main loop)
            
            # 2. Reason
            analysis = self.reason(task)
            
            # 3. Plan
            action = self.plan(task, analysis)
            
            # 4. Act
            result, success = self.act(task, action)
            
            # 5. Observe
            self.observe(task, action, result, success)
            
            # 6. Iterate
            decision = self.iterate(task, success)
            
            if decision == "complete":
                break
            elif decision == "failed":
                break
            elif decision == "retry":
                attempt += 1
                print(f"\n   Retrying... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(2)


def main():
    print("🚀 Starting Task Agent with Memory\n")
    
    # Initialize components
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    agent_name = os.getenv('AGENT_NAME', 'task-processor')
    model_url = os.getenv('AI_MODEL_URL', 'http://localhost:8080/v1')
    model_name = os.getenv('AI_MODEL_NAME', 'ai/smollm2:360m-instruct-q4_K_M')
    
    print(f"📊 Configuration:")
    print(f"   Redis: {redis_url}")
    print(f"   Agent: {agent_name}")
    print(f"   Model: {model_name}")
    print()
    
    # Initialize memory and agent
    memory = AgentMemory(redis_url, agent_name)
    agent = TaskAgent(memory, model_url, model_name)
    
    # Example tasks
    tasks = [
        {"id": "task-001", "description": "Process customer feedback data"},
        {"id": "task-002", "description": "Generate monthly report"},
        {"id": "task-003", "description": "Handle error in payment system"},  # Will fail
        {"id": "task-004", "description": "Update user documentation"},
    ]
    
    # Agent loop: Perceive → Process tasks
    print("🔄 Starting agent loop...\n")
    
    # 1. Perceive: Filter tasks based on memory
    pending_tasks = agent.perceive(tasks)
    
    # Process each pending task
    for task in pending_tasks:
        agent.run_loop(task)
    
    print(f"\n{'='*60}")
    print("✅ Agent loop completed")
    print(f"{'='*60}\n")
    
    # Show memory state
    print("📚 Memory State:")
    for task in tasks:
        actions = memory.get_past_actions(task['id'])
        if actions:
            print(f"\n   Task {task['id']}:")
            for action in actions:
                status = "✅" if action['success'] else "❌"
                print(f"      {status} {action['action'][:50]}...")
    
    # Keep agent running (in real scenario, would continuously perceive new tasks)
    print("\n💤 Agent entering idle state (press Ctrl+C to stop)...")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n\n👋 Agent shutting down...")


if __name__ == "__main__":
    main()
