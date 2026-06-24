import redis
import json
import time
import os

redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379, decode_responses=True)

def publish_file_metadata():
    """Publish file metadata to Redis channel"""
    patch_data = {
        "patch_id": "patch-001",
        "location": "/data/patch-001.diff",
        "agent": "bug-fixer",
        "content": "Sample patch content",
        "size": 100
    }
    
    print(f"📤 Publishing metadata: {patch_data}")
    redis_client.publish("patches", json.dumps(patch_data))
    print("✅ Metadata published to 'patches' channel")

if __name__ == "__main__":
    print("🚀 Writer agent starting...")
    time.sleep(2)  # Wait for Redis
    publish_file_metadata()
    print("💤 Keeping writer alive...")
    time.sleep(300)
