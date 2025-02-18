import requests

def send_slack_notification(user, message):
    if not user.slack_access_token:
        return

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {user.slack_access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "channel": user.slack_channel_id or user.slack_user_id,  # Send to user if no channel selected
        "text": message,
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
