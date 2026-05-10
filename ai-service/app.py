import os
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

from routes.api import api_bp
from utils.logger import get_logger

# Load environment variables
load_dotenv()

logger = get_logger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Configure strict slashes
    app.url_map.strict_slashes = False

    # Security headers
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response

    # Setup rate limiting
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["30 per minute"],
        storage_uri="memory://"
    )

    # Register blueprints
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        return jsonify({
            "service": "Penetration Test Manager AI Service",
            "status": "running",
            "endpoints": [
                "GET /health",
                "POST /describe",
                "POST /recommend",
                "POST /generate-report"
            ]
        }), 200

    # Global error handlers
    @app.errorhandler(429)
    def ratelimit_handler(e):
        logger.warning(f"Rate limit exceeded: {e.description}")
        return jsonify(error="ratelimit exceeded", description=str(e.description)), 429

    @app.errorhandler(400)
    def bad_request_handler(e):
        return jsonify(error="bad request", description=str(e.description)), 400

    @app.errorhandler(500)
    def internal_error_handler(e):
        logger.error(f"Internal server error: {e}")
        return jsonify(error="internal server error", description="An unexpected error occurred."), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
