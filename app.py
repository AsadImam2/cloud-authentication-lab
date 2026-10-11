

from flask import Flask, request, jsonify
import logging
import time
import secrets
import requests
import os

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Local learning lab only
TOKEN_LIFETIME = 30
issued_tokens = {}


@app.route("/")
def home():
    return jsonify({
        "message": "Cloud Authentication Lab API is running"
    })


@app.route("/api/token", methods=["POST"])
def issue_token():
    # Demo only: a real token endpoint needs proper client authentication
    token = secrets.token_urlsafe(16)
    expires_at = time.time() + TOKEN_LIFETIME

    issued_tokens[token] = expires_at

    logger.info("Demo token issued; expires in %s seconds", TOKEN_LIFETIME)

    return jsonify({
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": TOKEN_LIFETIME
    })


@app.route("/api/profile")
def profile():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        logger.warning("Authentication failed: missing bearer token")
        return jsonify({"error": "Missing bearer token"}), 401

    token = auth_header.removeprefix("Bearer ")
    expires_at = issued_tokens.get(token)

    if expires_at is None:
        logger.warning("Authentication failed: invalid token")
        return jsonify({"error": "Invalid token"}), 401

    if time.time() >= expires_at:
        issued_tokens.pop(token, None)
        logger.warning("Authentication failed: expired token")
        return jsonify({"error": "Token expired"}), 401

    logger.info("Authentication successful: profile accessed")

    return jsonify({
        "message": "Access granted",
        "profile": {
            "username": "lab-user",
            "role": "user"
        }
    })



@app.route("/api/inventory")
def inventory():
    # 1. Validate the user's bearer token
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        logger.warning("Inventory access denied: missing bearer token")
        return jsonify({"error": "Missing bearer token"}), 401

    user_token = auth_header.removeprefix("Bearer ")

    expires_at = issued_tokens.get(user_token)

    if expires_at is None:
        logger.warning("Inventory access denied: invalid user token")
        return jsonify({"error": "Invalid or expired token"}), 401

    if time.time() >= expires_at:
        issued_tokens.pop(user_token, None)
        logger.warning("Inventory access denied: expired user token")
        return jsonify({"error": "Invalid or expired token"}), 401

    # 2. Read the service token from the environment
    service_token = os.environ.get("SERVICE_TOKEN")

    if not service_token:
        logger.error("SERVICE_TOKEN is not configured")
        return jsonify({
            "error": "Inventory service authentication is not configured"
        }), 503

    # 3. Call Service B using the service token
    headers = {
        "Authorization": f"Bearer {service_token}"
    }

    try:
        response = requests.get(
            "http://127.0.0.1:5001/internal/inventory",
            headers=headers,
            timeout=5
        )

        logger.info(
            "Inventory service responded with status %s",
            response.status_code
        )

        return jsonify(response.json()), response.status_code

    except requests.RequestException:
        logger.warning("Inventory service request failed")
        return jsonify({
            "error": "Inventory service unavailable"
        }), 503



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

