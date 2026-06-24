# router/app.py
from flask import Flask, request, jsonify
import requests
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables set by Docker Compose models
CODE_MODEL_URL = os.getenv('CODE_MODEL_URL')
CODE_MODEL = os.getenv('CODE_MODEL')
VISION_MODEL_URL = os.getenv('VISION_MODEL_URL')
VISION_MODEL = os.getenv('VISION_MODEL')
TEXT_MODEL_URL = os.getenv('TEXT_MODEL_URL')
TEXT_MODEL = os.getenv('TEXT_MODEL')

# Log environment variables on startup
logger.info(f"CODE_MODEL_URL: {CODE_MODEL_URL}")
logger.info(f"VISION_MODEL_URL: {VISION_MODEL_URL}")
logger.info(f"TEXT_MODEL_URL: {TEXT_MODEL_URL}")

def classify_task(prompt):
    """Figure out task type from keywords."""
    prompt_lower = prompt.lower()
    
    code_keywords = ['code', 'function', 'bug', 'python', 'javascript']
    vision_keywords = ['image', 'picture', 'photo', 'analyze image']
    
    if any(kw in prompt_lower for kw in code_keywords):
        return 'code'
    if any(kw in prompt_lower for kw in vision_keywords):
        return 'vision'
    return 'text'

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "models": {
            "code": CODE_MODEL_URL,
            "vision": VISION_MODEL_URL,
            "text": TEXT_MODEL_URL
        }
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    task_type = classify_task(prompt)
    
    # Route to the right model
    if task_type == 'code':
        url = CODE_MODEL_URL
        model = CODE_MODEL
    elif task_type == 'vision':
        url = VISION_MODEL_URL
        model = VISION_MODEL
    else:
        url = TEXT_MODEL_URL
        model = TEXT_MODEL
    
    if not url or not model:
        return jsonify({
            "error": "Model not configured yet",
            "task_type": task_type,
            "message": "Models are still configuring. Please wait a few minutes."
        }), 503
    
    logger.info(f"Routing {task_type} request to model: {model} at {url}")
    
    try:
        # Model Runner uses a shared endpoint - the model is selected via the 'model' parameter
        response = requests.post(
            f"{url}completions",  # Note: URL already has /v1/ in it
            json={
                "model": model,
                "prompt": prompt,
                "max_tokens": 500,
                "temperature": 0.7
            },
            timeout=30
        )
        
        # Check if response is valid
        if response.status_code != 200:
            logger.error(f"Model returned status {response.status_code}: {response.text}")
            return jsonify({
                "error": "Model error",
                "status_code": response.status_code,
                "message": response.text
            }), response.status_code
        
        # Try to parse JSON
        try:
            result = response.json()
            result['routed_to'] = task_type
            result['model_used'] = model
            return jsonify(result)
        except ValueError:
            logger.error(f"Invalid JSON response: {response.text[:200]}")
            return jsonify({
                "error": "Invalid model response",
                "message": "Model returned non-JSON response. It may still be starting up.",
                "raw_response": response.text[:200]
            }), 503
            
    except requests.exceptions.ConnectionError:
        logger.error(f"Cannot connect to model at {url}")
        return jsonify({
            "error": "Model not available",
            "message": "Cannot connect to model. It may still be configuring."
        }), 503
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Model timeout",
            "message": "Model took too long to respond"
        }), 504
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "error": "Unexpected error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
