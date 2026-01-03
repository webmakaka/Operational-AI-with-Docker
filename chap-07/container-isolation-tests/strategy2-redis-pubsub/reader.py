import redis
import json
import time
import os

redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379, decode_responses=True)

def listen_for_patches():
    """Subscribe to patches channel and process messages"""
    pubsub = redis_client.pubsub()
    pubsub.subscribe("patches")
    
    print("👂 Reader agent listening for patches...")
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"📨 Received message: {message}")
            data = json.loads(message['data'])
            print(f"✅ Parsed metadata: {data}")
            print(f"   Patch ID: {data['patch_id']}")
            print(f"   Agent: {data['agent']}")
            print(f"   Location: {data['location']}")
            print(f"   Content: {data['content']}")
            break  # Exit after first message

if __name__ == "__main__":
    print("🚀 Reader agent starting...")
    time.sleep(3)  # Wait for writer to publish
    listen_for_patches()
    print("✅ Test complete!")
