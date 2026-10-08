# coordinator/app.py
from flask import Flask, request, jsonify
import requests
import redis
import json
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Service URLs from environment
SEARCHER_URL = os.getenv('SEARCHER_URL')
ANALYZER_URL = os.getenv('ANALYZER_URL')
WRITER_URL = os.getenv('WRITER_URL')
REDIS_URL = os.getenv('REDIS_URL')
MODEL_URL = os.getenv('MODEL_URL')
MODEL_NAME = os.getenv('MODEL_NAME')

# Redis connection
r = redis.from_url(REDIS_URL, decode_responses=True)

def generate_plan(question):
    """Use the coordinator model to plan the research."""
    response = requests.post(
        f"{MODEL_URL}completions",
        json={
            "model": MODEL_NAME,
            "prompt": f"""Given this research question: "{question}"
            
Create a search plan with 3-5 specific search queries that will help answer it.
Return ONLY a JSON array of search queries, nothing else.
Example: ["query 1", "query 2", "query 3"]""",
            "max_tokens": 200,
            "temperature": 0.3
        },
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        text = result['choices'][0]['text'].strip()
        # Parse the JSON array from the response
        try:
            queries = json.loads(text)
            return queries
        except:
            # Fallback: extract queries from text
            return [question]
    return [question]

@app.route('/api/research', methods=['POST'])
def research():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    # Generate unique research ID
    research_id = f"research:{hash(question)}"
    
    logger.info(f"Starting research: {question}")
    
    # Step 1: Plan the research
    logger.info("Step 1: Planning search queries")
    search_queries = generate_plan(question)
    
    # Store in Redis
    r.hset(research_id, "question", question)
    r.hset(research_id, "queries", json.dumps(search_queries))
    
    # Step 2: Search for information
    logger.info(f"Step 2: Searching with {len(search_queries)} queries")
    search_results = requests.post(
        f"{SEARCHER_URL}/api/search",
        json={"queries": search_queries, "research_id": research_id},
        timeout=60
    ).json()
    
    # Step 3: Analyze the results
    logger.info("Step 3: Analyzing search results")
    analysis = requests.post(
        f"{ANALYZER_URL}/api/analyze",
        json={
            "question": question,
            "results": search_results,
            "research_id": research_id
        },
        timeout=60
    ).json()
    
    # Step 4: Write the final report
    logger.info("Step 4: Writing final report")
    report = requests.post(
        f"{WRITER_URL}/api/write",
        json={
            "question": question,
            "analysis": analysis,
            "research_id": research_id
        },
        timeout=60
    ).json()
    
    # Store final result
    r.hset(research_id, "report", json.dumps(report))
    r.expire(research_id, 3600)  # Keep for 1 hour
    
    return jsonify({
        "question": question,
        "queries": search_queries,
        "findings": analysis.get('insights', []),
        "report": report.get('content', ''),
        "research_id": research_id
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "coordinator"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
