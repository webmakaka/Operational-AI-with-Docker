import os
import time
import redis
import json
from datetime import datetime

def main():
    agent_name = os.getenv('AGENT_NAME', 'agent')
    agent_type = os.getenv('AGENT_TYPE', 'worker')
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    print(f"🤖 Starting {agent_name} ({agent_type})")
    print(f"   Redis: {redis_url}")
    
    # Connect to shared memory
    redis_client = redis.from_url(redis_url, decode_responses=True)
    state_key = f"agent:{agent_name}:state"
    
    # RESUME FROM LAST STATE (production pattern)
    try:
        last_state = redis_client.get(state_key)
        if last_state:
            state_data = json.loads(last_state)
            iteration = state_data.get('iteration', 0) + 1
            print(f"📥 Resuming from iteration {iteration}")
        else:
            iteration = 1
            print(f"🆕 Starting fresh at iteration 1")
    except Exception as e:
        iteration = 1
        print(f"🆕 No previous state, starting at iteration 1")
    
    while True:
        # Write current state
        state = {
            "agent": agent_name,
            "type": agent_type,
            "iteration": iteration,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "active"
        }
        
        redis_client.set(state_key, json.dumps(state))
        print(f"✅ {agent_name} iteration {iteration} - state saved to {state_key}")
        
        # Read other agents' states (shared memory)
        all_keys = redis_client.keys("agent:*:state")
        print(f"   Visible agents: {len(all_keys)}")
        for key in all_keys:
            if key != state_key:
                other_state = json.loads(redis_client.get(key))
                print(f"   - {other_state['agent']}: iteration {other_state['iteration']}")
        
        iteration += 1
        time.sleep(10)

if __name__ == "__main__":
    main()
