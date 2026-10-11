
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

SERVICE_TOKEN = os.environ.get("SERVICE_TOKEN")

if not SERVICE_TOKEN:
    raise RuntimeError(
        "SERVICE_TOKEN environment variable is not configured"
    )


@app.route("/internal/inventory", methods=["GET"])
def get_inventory():
    auth_header = request.headers.get("Authorization", "")
    expected_header = f"Bearer {SERVICE_TOKEN}"

    if auth_header != expected_header:
        app.logger.warning(
            "Unauthorized service request rejected"
        )
        return jsonify({"error": "Unauthorized"}), 401

    app.logger.info("Authenticated service request accepted")

    return jsonify({
        "service": "inventory-service",
        "inventory": {
            "laptop": 12,
            "keyboard": 25
        }
    }), 200


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )
