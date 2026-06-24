# writer/app.py
from flask import Flask, request, jsonify
import requests
import redis
import json
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_URL = os.getenv('REDIS_URL')
MODEL_URL = os.getenv('MODEL_URL')
MODEL_NAME = os.getenv('MODEL_NAME')

r = redis.from_url(REDIS_URL, decode_responses=True)

def write_report(question, insights):
    """Generate final research report."""
    insights_text = "\n".join([f"- {insight}" for insight in insights])
    
    prompt = f"""Question: {question}

Key findings:
{insights_text}

Write a clear, concise research report (2-3 paragraphs) that answers the question based on these findings."""
    
    response = requests.post(
        f"{MODEL_URL}completions",
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "max_tokens": 500,
            "temperature": 0.7
        },
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['text'].strip()
    
    return "Unable to generate report"

@app.route('/api/write', methods=['POST'])
def write():
    data = request.json
    question = data.get('question')
    analysis = data.get('analysis', {})
    research_id = data.get('research_id')
    
    insights = analysis.get('insights', [])
    
    logger.info(f"Writing report based on {len(insights)} insights")
    
    content = write_report(question, insights)
    
    report = {
        "content": content,
        "insights_used": len(insights)
    }
    
    # Store in Redis
    if research_id:
        r.hset(research_id, "final_report", json.dumps(report))
    
    return jsonify(report)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "writer"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)
