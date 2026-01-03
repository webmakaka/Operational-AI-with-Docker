import redis
import json
import os

def main():
    redis_client = redis.from_url(
        os.getenv('REDIS_URL', 'redis://redis:6379'),
        decode_responses=True
    )
    
    print("👂 Reader Agent Starting...")
    print("   Listening for patches on 'patches' channel\n")
    
    # Subscribe to the patches channel
    pubsub = redis_client.pubsub()
    pubsub.subscribe("patches")
    
    print("✅ Subscribed successfully!\n")
    
    # Listen for messages
    for message in pubsub.listen():
        if message['type'] == 'message':
            # Parse the JSON data
            data = json.loads(message['data'])
            
            print(f"📨 Received: {data['patch_id']}")
            print(f"   Location: {data['location']}")
            print(f"   Size: {data['size']} bytes")
            print(f"   Processing patch...\n")

if __name__ == "__main__":
    main()
