import logging
import json
import time
import os
import sys

# Configure structured JSON logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "agent_id": os.getenv("HOSTNAME", "unknown")
        }
        
        # Add extra fields if present
        if hasattr(record, 'task_id'):
            log_data['task_id'] = record.task_id
        if hasattr(record, 'duration'):
            log_data['duration'] = record.duration
            
        return json.dumps(log_data)

# Setup logger
logger = logging.getLogger("agent")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

def simulate_task(task_id):
    """Simulate processing a task"""
    start = time.time()
    
    logger.info(f"Starting task", extra={"task_id": task_id})
    
    # Simulate work
    time.sleep(1)
    
    duration = time.time() - start
    logger.info(f"Task completed", extra={"task_id": task_id, "duration": round(duration, 2)})

def main():
    logger.info("🔒 Secure Agent Starting...")
    logger.info(f"   Running as: {os.getuid()}:{os.getgid()}")
    logger.info(f"   Hostname: {os.getenv('HOSTNAME')}")
    
    # Test filesystem permissions
    try:
        with open('/test-write.txt', 'w') as f:
            f.write("test")
        logger.info("✅ Filesystem is writable")
    except Exception as e:
        logger.warning(f"⚠️  Filesystem is read-only: {str(e)}")
    
    # Test tmpfs write
    try:
        with open('/tmp/test.txt', 'w') as f:
            f.write("test")
        logger.info("✅ /tmp is writable (tmpfs)")
    except Exception as e:
        logger.error(f"❌ /tmp write failed: {str(e)}")
    
    # Process tasks
    task_id = 1
    while True:
        try:
            simulate_task(f"task-{task_id:03d}")
            task_id += 1
            time.sleep(3)
        except Exception as e:
            logger.error(f"Task failed", extra={"error": str(e), "error_type": type(e).__name__})

if __name__ == "__main__":
    main()
