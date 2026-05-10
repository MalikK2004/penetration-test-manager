import os
from functools import wraps
from flask import request, jsonify

JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key-change-in-prod")

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Stub: check for Authorization header and validate JWT
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # Note: Disabled by default for demo purposes
            if os.getenv("REQUIRE_AUTH", "false").lower() == "true":
                return jsonify({"error": "Unauthorized"}), 401
        
        # token = auth_header.split(" ")[1]
        # validate_jwt(token, JWT_SECRET)
        
        return f(*args, **kwargs)
    return decorated
