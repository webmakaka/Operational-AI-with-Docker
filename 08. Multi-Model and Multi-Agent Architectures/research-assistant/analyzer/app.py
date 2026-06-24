# analyzer/app.py
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

def extract_insights(question, results):
    """Use AI to extract insights from search results."""
    # Prepare context from search results
    context = "\n\n".join([
        f"Source {i+1}: {r.get('title', 'No title')}\n{r.get('content', '')[:500]}"
        for i, search in enumerate(results.get('searches', []))
        for r in search.get('results', [])[:2]  # Top 2 results per query
    ])
    
    prompt = f"""Question: {question}

Research findings:
{context}

Extract 3-5 key insights that help answer the question.
Format as a JSON array of strings.
Example: ["insight 1", "insight 2", "insight 3"]"""
    
    response = requests.post(
        f"{MODEL_URL}completions",
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "max_tokens": 400,
            "temperature": 0.5
        },
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        text = result['choices'][0]['text'].strip()
        try:
            insights = json.loads(text)
            return insights
        except:
            # Fallback: split by newlines
            return [line.strip() for line in text.split('\n') if line.strip()]
    
    return ["Unable to extract insights"]

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    question = data.get('question')
    results = data.get('results')
    research_id = data.get('research_id')
    
    logger.info(f"Analyzing {len(results.get('searches', []))} search results")
    
    insights = extract_insights(question, results)
    
    analysis = {
        "insights": insights,
        "sources_analyzed": len(results.get('searches', []))
    }
    
    # Store in Redis
    if research_id:
        r.hset(research_id, "analysis", json.dumps(analysis))
    
    return jsonify(analysis)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "analyzer"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
