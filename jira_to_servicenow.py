from flask import Flask, request, jsonify
import requests
import base64
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Load config from .env
SNOW_INSTANCE = os.getenv("SNOW_INSTANCE")
SNOW_USER = os.getenv("SNOW_USER")
SNOW_PASSWORD = os.getenv("SNOW_PASSWORD")
SNOW_TABLE = os.getenv("SNOW_TABLE", "incident")

JIRA_INSTANCE = os.getenv("JIRA_INSTANCE")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# --- Utility to encode auth ---
def encode_auth(user, password):
    return base64.b64encode(f"{user}:{password}".encode()).decode()

# --- Webhook Endpoint ---
@app.route('/webhook', methods=['POST'])
def jira_webhook():
    data = request.json
    print("Webhook received:", json.dumps(data, indent=2))

    # Extract Jira issue info
    issue_key = data['issue']['key']
    summary = data['issue']['fields']['summary']
    description = data['issue']['fields'].get('description', '')

    # --- Create Incident in ServiceNow ---
    snow_url = f"{SNOW_INSTANCE}/api/now/table/{SNOW_TABLE}"
    snow_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    snow_auth = (SNOW_USER, SNOW_PASSWORD)
    snow_payload = {
        "short_description": f"[Jira {issue_key}] {summary}",
        "description": description,
        "caller_id": "<Default Caller>",  # Optional: adjust to your needs
        "category": "Inquiry / Help",
        "subcategory": "Software"
    }

    snow_response = requests.post(snow_url, auth=snow_auth,
                                  headers=snow_headers, json=snow_payload)

    if snow_response.status_code != 201:
        print("Failed to create ServiceNow Incident:", snow_response.text)
        return jsonify({"status": "error", "details": snow_response.text}), 500

    snow_result = snow_response.json()['result']
    incident_number = snow_result['number']

    print(f"Created ServiceNow Incident: {incident_number}")

    # --- (Optional) Add comment back to Jira ---
    jira_url = f"{JIRA_INSTANCE}/rest/api/3/issue/{issue_key}/comment"
    jira_headers = {
        "Authorization": f"Basic {encode_auth(JIRA_USER, JIRA_API_TOKEN)}",
        "Content-Type": "application/json"
    }
    jira_payload = {
    "body": {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"A related ServiceNow incident {incident_number} has been created."
                    }
                ]
            }
        ]
    }
}

    jira_response = requests.post(jira_url, headers=jira_headers, json=jira_payload)

    if jira_response.status_code not in [200, 201]:
        print("Failed to add comment to Jira:", jira_response.text)

    return jsonify({"status": "success", "incident_number": incident_number}), 200


if __name__ == '__main__':
    # Run Flask on your server
    app.run(host='0.0.0.0', port=5000)