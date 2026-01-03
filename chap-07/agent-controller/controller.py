"""
Agent Controller - Manages and coordinates autonomous agents
Provides REST API for agent management and monitoring
"""

import redis
import json
import time
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, render_template_string
import os
import threading

app = Flask(__name__)

class AgentController:
    """Controls and monitors autonomous agents"""
    
    def __init__(self, redis_url, controller_name):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.controller_name = controller_name
        
    def register_agent(self, agent_name, agent_type):
        """Register a new agent with the controller"""
        agent_info = {
            "name": agent_name,
            "type": agent_type,
            "status": "active",
            "registered_at": datetime.utcnow().isoformat(),
            "last_heartbeat": datetime.utcnow().isoformat(),
            "tasks_completed": 0,
            "tasks_failed": 0
        }
        key = f"controller:{self.controller_name}:agents:{agent_name}"
        self.redis.set(key, json.dumps(agent_info))
        print(f"✅ Registered agent: {agent_name} ({agent_type})")
        return agent_info
    
    def heartbeat(self, agent_name):
        """Record agent heartbeat"""
        key = f"controller:{self.controller_name}:agents:{agent_name}"
        agent_data = self.redis.get(key)
        if agent_data:
            agent_info = json.loads(agent_data)
            agent_info["last_heartbeat"] = datetime.utcnow().isoformat()
            agent_info["status"] = "active"
            self.redis.set(key, json.dumps(agent_info))
    
    def update_agent_stats(self, agent_name, success):
        """Update agent task statistics"""
        key = f"controller:{self.controller_name}:agents:{agent_name}"
        agent_data = self.redis.get(key)
        if agent_data:
            agent_info = json.loads(agent_data)
            if success:
                agent_info["tasks_completed"] = agent_info.get("tasks_completed", 0) + 1
            else:
                agent_info["tasks_failed"] = agent_info.get("tasks_failed", 0) + 1
            self.redis.set(key, json.dumps(agent_info))
    
    def get_all_agents(self):
        """Get status of all registered agents"""
        pattern = f"controller:{self.controller_name}:agents:*"
        keys = self.redis.keys(pattern)
        agents = []
        
        for key in keys:
            agent_data = self.redis.get(key)
            if agent_data:
                agent_info = json.loads(agent_data)
                
                # Check if agent is stale (no heartbeat in 30 seconds)
                last_heartbeat = datetime.fromisoformat(agent_info["last_heartbeat"])
                if datetime.utcnow() - last_heartbeat > timedelta(seconds=30):
                    agent_info["status"] = "inactive"
                    self.redis.set(key, json.dumps(agent_info))
                
                agents.append(agent_info)
        
        return agents
    
    def assign_task(self, task_id, task_description, agent_type=None):
        """Assign a task to the task queue"""
        task = {
            "id": task_id,
            "description": task_description,
            "assigned_type": agent_type,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Add to task queue
        queue_key = f"controller:{self.controller_name}:task_queue"
        self.redis.rpush(queue_key, json.dumps(task))
        print(f"📝 Task assigned: {task_id} - {task_description}")
        return task
    
    def get_task_queue(self):
        """Get all pending tasks"""
        queue_key = f"controller:{self.controller_name}:task_queue"
        tasks = self.redis.lrange(queue_key, 0, -1)
        return [json.loads(t) for t in tasks]
    
    def dequeue_task(self, agent_name):
        """Get next task for an agent"""
        queue_key = f"controller:{self.controller_name}:task_queue"
        task_data = self.redis.lpop(queue_key)
        
        if task_data:
            task = json.loads(task_data)
            task["assigned_to"] = agent_name
            task["status"] = "processing"
            task["started_at"] = datetime.utcnow().isoformat()
            
            # Store in active tasks
            active_key = f"controller:{self.controller_name}:active_tasks:{task['id']}"
            self.redis.set(active_key, json.dumps(task))
            
            return task
        return None
    
    def complete_task(self, task_id, success, result):
        """Mark a task as completed"""
        active_key = f"controller:{self.controller_name}:active_tasks:{task_id}"
        task_data = self.redis.get(active_key)
        
        if task_data:
            task = json.loads(task_data)
            task["status"] = "completed" if success else "failed"
            task["result"] = result
            task["completed_at"] = datetime.utcnow().isoformat()
            
            # Move to completed tasks
            completed_key = f"controller:{self.controller_name}:completed_tasks"
            self.redis.rpush(completed_key, json.dumps(task))
            
            # Remove from active
            self.redis.delete(active_key)
            
            # Update agent stats
            if "assigned_to" in task:
                self.update_agent_stats(task["assigned_to"], success)
    
    def get_system_stats(self):
        """Get overall system statistics"""
        agents = self.get_all_agents()
        queue = self.get_task_queue()
        
        active_agents = sum(1 for a in agents if a["status"] == "active")
        total_completed = sum(a.get("tasks_completed", 0) for a in agents)
        total_failed = sum(a.get("tasks_failed", 0) for a in agents)
        
        return {
            "total_agents": len(agents),
            "active_agents": active_agents,
            "inactive_agents": len(agents) - active_agents,
            "pending_tasks": len(queue),
            "total_completed": total_completed,
            "total_failed": total_failed,
            "success_rate": round(total_completed / (total_completed + total_failed) * 100, 1) if (total_completed + total_failed) > 0 else 0
        }


# Initialize controller
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
controller_name = os.getenv('CONTROLLER_NAME', 'main-controller')
controller = AgentController(redis_url, controller_name)

# Dashboard HTML
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Agent Controller Dashboard</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
            margin: 0;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #2c3e50; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stat-value {
            font-size: 32px;
            font-weight: bold;
            color: #3498db;
        }
        .stat-label {
            color: #7f8c8d;
            font-size: 14px;
            margin-top: 5px;
        }
        .section {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .agent-card {
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 10px 0;
            background: #f8f9fa;
            border-radius: 5px;
        }
        .agent-card.inactive { border-left-color: #e74c3c; }
        .status { 
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }
        .status.active { background: #d4edda; color: #155724; }
        .status.inactive { background: #f8d7da; color: #721c24; }
        .task-item {
            padding: 10px;
            margin: 5px 0;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 3px solid #3498db;
        }
        button {
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover { background: #2980b9; }
    </style>
    <script>
        function refresh() { location.reload(); }
        setInterval(refresh, 5000); // Auto-refresh every 5 seconds
    </script>
</head>
<body>
    <div class="container">
        <h1>🤖 Agent Controller Dashboard</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{{ stats.total_agents }}</div>
                <div class="stat-label">Total Agents</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ stats.active_agents }}</div>
                <div class="stat-label">Active Agents</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ stats.pending_tasks }}</div>
                <div class="stat-label">Pending Tasks</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ stats.success_rate }}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Registered Agents</h2>
            {% for agent in agents %}
            <div class="agent-card {{ agent.status }}">
                <strong>{{ agent.name }}</strong> 
                <span class="status {{ agent.status }}">{{ agent.status }}</span>
                <br>
                Type: {{ agent.type }} | 
                Completed: {{ agent.tasks_completed }} | 
                Failed: {{ agent.tasks_failed }} |
                Last seen: {{ agent.last_heartbeat }}
            </div>
            {% endfor %}
        </div>
        
        <div class="section">
            <h2>📋 Task Queue ({{ stats.pending_tasks }} pending)</h2>
            {% for task in tasks %}
            <div class="task-item">
                <strong>{{ task.id }}</strong>: {{ task.description }}
                {% if task.assigned_type %}(Type: {{ task.assigned_type }}){% endif %}
            </div>
            {% endfor %}
            {% if stats.pending_tasks == 0 %}
            <p style="color: #7f8c8d;">No pending tasks</p>
            {% endif %}
        </div>
        
        <button onclick="refresh()">🔄 Refresh Now</button>
    </div>
</body>
</html>
'''

# REST API Endpoints
@app.route('/')
def dashboard():
    """Agent controller dashboard"""
    agents = controller.get_all_agents()
    tasks = controller.get_task_queue()
    stats = controller.get_system_stats()
    
    return render_template_string(DASHBOARD_HTML, 
                                 agents=agents, 
                                 tasks=tasks, 
                                 stats=stats)

@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Get all registered agents"""
    return jsonify(controller.get_all_agents())

@app.route('/api/agents/register', methods=['POST'])
def register_agent():
    """Register a new agent"""
    data = request.json
    agent_info = controller.register_agent(data['name'], data['type'])
    return jsonify(agent_info)

@app.route('/api/agents/<agent_name>/heartbeat', methods=['POST'])
def agent_heartbeat(agent_name):
    """Agent heartbeat"""
    controller.heartbeat(agent_name)
    return jsonify({"status": "ok"})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get task queue"""
    return jsonify(controller.get_task_queue())

@app.route('/api/tasks/assign', methods=['POST'])
def assign_task():
    """Assign a new task"""
    data = request.json
    task = controller.assign_task(
        data['id'],
        data['description'],
        data.get('type')
    )
    return jsonify(task)

@app.route('/api/tasks/dequeue', methods=['POST'])
def dequeue_task():
    """Get next task for an agent"""
    data = request.json
    task = controller.dequeue_task(data['agent_name'])
    if task:
        return jsonify(task)
    return jsonify({"status": "no_tasks"}), 404

@app.route('/api/tasks/<task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """Mark task as completed"""
    data = request.json
    controller.complete_task(task_id, data['success'], data.get('result', ''))
    return jsonify({"status": "ok"})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    return jsonify(controller.get_system_stats())

if __name__ == '__main__':
    print("🚀 Starting Agent Controller...")
    print(f"📊 Dashboard: http://localhost:8000")
    print(f"📡 API: http://localhost:8000/api/*")
    
    # Auto-register some demo tasks
    time.sleep(2)
    controller.assign_task("demo-001", "Process customer data", "data-processor")
    controller.assign_task("demo-002", "Analyze sales trends", "analyst")
    controller.assign_task("demo-003", "Generate report", "analyst")
    
    app.run(host='0.0.0.0', port=8000, debug=True)
