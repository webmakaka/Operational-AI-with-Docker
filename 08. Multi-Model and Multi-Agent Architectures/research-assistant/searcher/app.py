# searcher/app.py - UPDATED to call Firecrawl API directly
from flask import Flask, request, jsonify
import requests
import redis
import json
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')
REDIS_URL = os.getenv('REDIS_URL')
MODEL_URL = os.getenv('MODEL_URL')
MODEL_NAME = os.getenv('MODEL_NAME')

r = redis.from_url(REDIS_URL, decode_responses=True)

def search_web(query):
    """Search the web using Firecrawl API directly."""
    if not FIRECRAWL_API_KEY:
        logger.error("FIRECRAWL_API_KEY not set")
        return {"data": []}
    
    try:
        # Call Firecrawl search API directly
        # Documentation: https://docs.firecrawl.dev/api-reference/endpoint/search
        response = requests.post(
            "https://api.firecrawl.dev/v1/search",
            headers={
                "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "query": query,
                "limit": 5
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Search successful: {len(data.get('data', []))} results")
            return data
        else:
            logger.error(f"Search failed: {response.status_code} - {response.text}")
            return {"data": []}
            
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return {"data": []}

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    queries = data.get('queries', [])
    research_id = data.get('research_id')
    
    all_results = []
    
    for query in queries:
        logger.info(f"Searching: {query}")
        results = search_web(query)
        
        all_results.append({
            "query": query,
            "results": results.get('data', [])
        })
    
    # Store in Redis
    if research_id:
        r.hset(research_id, "search_results", json.dumps(all_results))
    
    return jsonify({
        "searches": all_results,
        "total_results": sum(len(r['results']) for r in all_results)
    })

@app.route('/health', methods=['GET'])
def health():
    has_key = bool(FIRECRAWL_API_KEY)
    return jsonify({
        "status": "healthy",
        "service": "searcher",
        "firecrawl_configured": has_key
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
