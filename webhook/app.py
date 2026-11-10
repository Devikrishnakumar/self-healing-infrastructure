
from flask import Flask, request, jsonify
import subprocess
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/alert", methods=["POST"])
def receive_alert():
    data = request.get_json(silent=True) or {}
    results = []

    for alert in data.get("alerts", []):
        name = alert.get("labels", {}).get("alertname")
        status = alert.get("status", data.get("status", ""))

        if name != "NginxDown" or status != "firing":
            results.append({"alert": name, "action": "ignored"})
            continue

        logging.warning("NginxDown alert received. Starting recovery playbook.")

        try:
            result = subprocess.run(
                [
                    "ansible-playbook",
                    "/ansible/recover-nginx.yml"
                ],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                logging.info("Recovery playbook completed successfully.")
                results.append({
                    "alert": name,
                    "action": "recovery_completed"
                })
            else:
                logging.error("Recovery failed: %s", result.stderr)
                return jsonify({
                    "error": "Recovery playbook failed",
                    "details": result.stderr[-2000:]
                }), 500

        except subprocess.TimeoutExpired:
            logging.error("Recovery playbook timed out.")
            return jsonify({"error": "Recovery timed out"}), 504

    return jsonify({"results": results}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
