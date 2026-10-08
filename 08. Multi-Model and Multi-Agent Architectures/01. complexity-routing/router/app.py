# router/app.py
from flask import Flask, request, jsonify
import requests
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables from Docker Compose
SMALL_MODEL_URL = os.getenv('SMALL_MODEL_URL')
SMALL_MODEL = os.getenv('SMALL_MODEL')
MEDIUM_MODEL_URL = os.getenv('MEDIUM_MODEL_URL')
MEDIUM_MODEL = os.getenv('MEDIUM_MODEL')
LARGE_MODEL_URL = os.getenv('LARGE_MODEL_URL')
LARGE_MODEL = os.getenv('LARGE_MODEL')

def analyze_complexity(prompt):
    """Score how complex a prompt is (0-1)."""
    score = 0
    
    # Length adds to complexity
    score += min(len(prompt) / 500, 0.3)
    
    # Technical terms mean more complex
    technical_terms = ['distributed', 'architecture', 'optimization', 'algorithm']
    tech_count = sum(1 for term in technical_terms if term in prompt.lower())
    score += min(tech_count / 3, 0.4)
    
    # Reasoning words mean more complex
    reasoning_words = ['analyze', 'compare', 'design', 'evaluate']
    reasoning_count = sum(1 for word in reasoning_words if word in prompt.lower())
    score += min(reasoning_count / 2, 0.3)
    
    return score

def select_model(complexity_score):
    """Pick model based on complexity."""
    if complexity_score < 0.3:
        return SMALL_MODEL_URL, SMALL_MODEL, 'small'
    elif complexity_score < 0.7:
        return MEDIUM_MODEL_URL, MEDIUM_MODEL, 'medium'
    else:
        return LARGE_MODEL_URL, LARGE_MODEL, 'large'

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    # Analyze complexity
    complexity = analyze_complexity(prompt)
    url, model, size = select_model(complexity)
    
    logger.info(f"Complexity: {complexity:.2f}, using {size} model: {model}")
    
    try:
        response = requests.post(
            f"{url}completions",
            json={
                "model": model,
                "prompt": prompt,
                "max_tokens": 500
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            result['complexity_score'] = complexity
            result['model_size'] = size
            result['model_used'] = model
            return jsonify(result)
        else:
            return jsonify({"error": "Model error"}), 503
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
