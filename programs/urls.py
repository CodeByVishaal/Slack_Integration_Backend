from django.urls import path
from .slack_views import slack_auth, slack_auth_callback, slack_api, get_slack_channels, save_slack_channel, slack_auth_test
from .views import ProgramListView, ProgramUpdateView

urlpatterns = [
    path('', ProgramListView.as_view()),
    path("slack/auth/", slack_auth),
    path('slack/auth/callback/', slack_auth_callback),
    path('update/<uuid:pk>/', ProgramUpdateView.as_view()),
    path('slack/channels/', get_slack_channels),
    path('slack/save_channel/', save_slack_channel),
    path('slack-code', slack_api),
    path('slack-auth-test', slack_auth_test),
]
