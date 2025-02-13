from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics
from .serializers import ProgramSerializer
from .models import Program
from .utils import send_slack_notification
# Create your views here.

class ProgramListView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role != 'customer':
            raise PermissionDenied("You do not have permission to create a program.")

        updated_instance = serializer.save()  # Save the updated data
        # Create a Slack notification message
        message = f"🔔 *Program Updated!*\n" \
                  f"📌 *Title:* {updated_instance.title}\n" \
                  f"📄 *Description:* {updated_instance.description}\n" \
                  f"⚠️ *Severity:* {updated_instance.severity}\n" \
                  f"📌 *Status:* {updated_instance.status}\n"

        # Send the Slack notification
        send_slack_notification(message)


class ProgramUpdateView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdminUser]
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()

