import requests

from django.conf import settings

def send_slack_notification(message):
    webhook_url = settings.SLACK_WEBHOOK_URL  # Ensure this is in your settings.py
    payload = {"text": message}
    headers = {"Content-Type": "application/json"}

    response = requests.post(webhook_url, json=payload, headers=headers)

    return response.status_code == 200
