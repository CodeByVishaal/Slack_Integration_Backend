import requests

def send_slack_notification(user, message):
    if not user.slack_access_token:
        print("Slack access token missing.")
        return

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {user.slack_access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "channel": user.slack_channel_id,
        "text": message,
    }

    print(f"Sending message to channel: {user.slack_channel_id}")

    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()

    if not response_data.get("ok"):
        print("Slack API Error:", response_data)

        # If the bot is not in the channel, try to join it
        if response_data.get("error") == "not_in_channel":
            join_url = "https://slack.com/api/conversations.join"
            join_data = {"channel": user.slack_channel_id}
            join_response = requests.post(join_url, json=join_data, headers=headers)

            join_response_data = join_response.json()
            print("Join Channel Response:", join_response_data)

            # Retry sending the message after joining
            if join_response_data.get("ok"):
                response = requests.post(url, json=data, headers=headers)
                response_data = response.json()

    return response_data
