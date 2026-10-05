import redis
import json
import time
import os

def main():
    redis_client = redis.from_url(
        os.getenv('REDIS_URL', 'redis://redis:6379'),
        decode_responses=True
    )
    
    print("📤 Writer Agent Starting...")
    print("   Publishing patches to 'patches' channel\n")
    
    patch_id = 1
    
    while True:
        # Create patch metadata
        patch_data = {
            "patch_id": f"patch-{patch_id:03d}",
            "location": f"/data/patch-{patch_id:03d}.diff",
            "agent": "bug-fixer",
            "size": 100 + (patch_id * 10)
        }
        
        print(f"📤 Publishing: {patch_data['patch_id']}")
        print(f"   Size: {patch_data['size']} bytes")
        
        # Publish to Redis channel
        redis_client.publish("patches", json.dumps(patch_data))
        
        patch_id += 1
        time.sleep(5)  # Publish every 5 seconds

if __name__ == "__main__":
    main()
