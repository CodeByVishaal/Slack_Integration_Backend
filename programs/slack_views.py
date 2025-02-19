from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import redirect
from django.conf import settings
import requests
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def slack_auth(request):
    user = request.user

    if user.slack_access_token:
        # User is authenticated with Slack
        return Response({
            'authenticated': True,
            'message': 'You are already authenticated with Slack.',
            'redirect_url': 'http://localhost:5173/slack-auth-test'
        }, status=200)

    slack_url = (
        f"https://slack.com/oauth/v2/authorize?client_id={settings.SLACK_CLIENT_ID}"
        f"&scope=channels:read,channels:manage,chat:write,users:write,users:read,commands,incoming-webhook"
        f"&user_scope=users:read,chat:write,channels:write.invites,groups:write.invites"
        f"&redirect_uri={settings.SLACK_REDIRECT_URI}"
        f"&bot_scope=channels:read"
    )
    return redirect(slack_url)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def slack_auth_callback(request):
    code = request.GET.get("code")
    print(code)
    if not code:
        return Response({"error": "No authorization code provided"}, status=400)

    response = requests.post("https://slack.com/api/oauth.v2.access", data={
        "client_id": settings.SLACK_CLIENT_ID,
        "client_secret": settings.SLACK_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.SLACK_REDIRECT_URI,

    }).json()

    if not response.get("ok"):
        return Response({"error": "Slack authentication failed"}, status=400)

    print(response)
    access_token = response["authed_user"]["access_token"]
    slack_user_id = response["authed_user"]["id"]
    slack_team_id = response["team"]["id"]

    user = request.user
    user.slack_access_token = access_token
    user.slack_user_id = slack_user_id
    user.slack_team_id = slack_team_id  # Store Slack team ID if needed
    user.save()

    return redirect("http://localhost:5173/select-slack-channel")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_slack_channels(request):
    user = request.user
    if not user.slack_access_token:
        return Response({"error": "Slack not connected"}, status=400)

    headers = {
        "Authorization": f"Bearer {user.slack_access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get("https://slack.com/api/conversations.list", headers=headers).json()

    if not response.get("ok"):
        return Response({"error": "Failed to fetch channels"}, status=400)

    channels = [{"id": ch["id"], "name": ch["name"]} for ch in response["channels"]]
    return Response({"channels": channels})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_slack_channel(request):
    channel_id = request.data.get("channel_id")
    if not channel_id:
        return Response({"error": "No channel selected"}, status=400)

    user = request.user
    user.slack_channel_id = channel_id
    user.save()

    return Response({"message": "Slack channel saved successfully"})


@api_view(['GET'])
def slack_api(request):
    slack_code = '8442511989926.8472239734629.1bacdd126ec19f12d51f10943faefa55dbf8d000a7c3ff1e10cfa50bcb04eaa1'

    print(slack_code)
    response = requests.post("https://slack.com/api/oauth.v2.access", data={
        "client_id": settings.SLACK_CLIENT_ID,
        "client_secret": settings.SLACK_CLIENT_SECRET,
        "code": slack_code,
        "redirect_uri": settings.SLACK_REDIRECT_URI,
    }).json()

    print(response)

    if not response.get("ok"):
        return Response({"error": "Slack authentication failed"}, status=400)

    access_token = response["access_token"]
    slack_user_id = response["authed_user"]["id"]
    slack_team_id = response["team"]["id"]
    slack_channel_id = response["incoming_webhook"]['channel_id']

    user = request.user
    user.slack_access_token = access_token
    user.slack_user_id = slack_user_id
    user.slack_team_id = slack_team_id  # Store Slack team ID if needed
    user.slack_channel_id = slack_channel_id
    user.save()

    return Response({"message": "Slack integration successful", "Slack_user": slack_user_id})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def slack_auth_test(request):
    user = request.user

    if user.slack_access_token:
        # User is authenticated with Slack
        return Response({
            'authenticated': True,
            'message': 'You are already authenticated with Slack.',
            'slack_user_id': user.slack_user_id,  # Assuming you store Slack user ID in your model
            'user_name': f'{user.first_name} {user.last_name}',
            'redirect_url': 'http://localhost:5173/slack-auth-test'
        }, status=200)

    return Response({
            'authenticated': False,
            'message': 'You are not authenticated with Slack. Please log in.',
            'redirect_url': 'http://localhost:5173/slack'  # Change this to your login URL
        }, status=401)