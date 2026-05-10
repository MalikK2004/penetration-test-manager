from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
from middleware.security import validate_and_sanitize
from prompts.templates import SYSTEM_PROMPT, DESCRIBE_PROMPT, RECOMMEND_PROMPT, REPORT_PROMPT
import json
import time

api_bp = Blueprint('api', __name__)
groq_client = GroqClient()
START_TIME = time.time()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    uptime = time.time() - START_TIME
    return jsonify({
        "status": "healthy",
        "model": groq_client.model,
        "uptime_seconds": round(uptime, 2),
        "average_response_time_seconds": groq_client.get_average_response_time()
    }), 200

@api_bp.route('/describe', methods=['GET', 'POST'])
def describe():
    """Generates a structured description for a vulnerability."""
    if request.method == 'GET':
        return jsonify({
            "message": "This is a POST endpoint.",
            "usage": "Send a POST request with a JSON payload.",
            "example_payload": {"vulnerability": "SQL injection in login"}
        }), 200

    data = request.get_json()
    if not data or 'vulnerability' not in data:
        return jsonify({"error": "Missing 'vulnerability' field in request"}), 400
        
    is_valid, sanitized_vuln, error_msg = validate_and_sanitize(data['vulnerability'])
    if not is_valid:
        return jsonify({"error": error_msg}), 400
        
    user_prompt = DESCRIBE_PROMPT.format(vulnerability=sanitized_vuln)
    result = groq_client.generate_description(SYSTEM_PROMPT, user_prompt)
    
    return jsonify(result), 200

@api_bp.route('/recommend', methods=['GET', 'POST'])
def recommend():
    """Generates remediation recommendations."""
    if request.method == 'GET':
        return jsonify({
            "message": "This is a POST endpoint.",
            "usage": "Send a POST request with a JSON payload.",
            "example_payload": {"vulnerability": "SQL Injection in login"}
        }), 200

    data = request.get_json()
    if not data or 'vulnerability' not in data:
        return jsonify({"error": "Missing 'vulnerability' field in request"}), 400
        
    is_valid_vuln, sanitized_vuln, error_msg_vuln = validate_and_sanitize(data['vulnerability'])
    if not is_valid_vuln:
        return jsonify({"error": f"vulnerability: {error_msg_vuln}"}), 400
        
    user_prompt = RECOMMEND_PROMPT.format(vulnerability=sanitized_vuln)
    result = groq_client.generate_recommendation(SYSTEM_PROMPT, user_prompt)
    
    return jsonify(result), 200

@api_bp.route('/generate-report', methods=['GET', 'POST'])
def generate_report():
    """Generates a comprehensive report from findings."""
    if request.method == 'GET':
        return jsonify({
            "message": "This is a POST endpoint.",
            "usage": "Send a POST request with a JSON payload.",
            "example_payload": {"input_data": "Found SQLi in the Banking App's login module"}
        }), 200

    data = request.get_json()
    if not data or 'input_data' not in data:
        return jsonify({"error": "Missing 'input_data' field in request"}), 400
        
    is_valid_d, sanitized_d, err_d = validate_and_sanitize(data['input_data'])
    
    if not is_valid_d:
        return jsonify({"error": f"input_data: {err_d}"}), 400
        
    user_prompt = REPORT_PROMPT.format(input_data=sanitized_d)
    result = groq_client.generate_report(SYSTEM_PROMPT, user_prompt)
    
    return jsonify(result), 200
