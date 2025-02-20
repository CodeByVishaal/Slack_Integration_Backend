from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Submission
from .serializers import SubmissionSerializer
from programs.utils import send_slack_notification
# Create your views here.

class SubmissionListView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def perform_create(self, serializer):

        if self.request.user.role != 'researcher':
            raise PermissionDenied("You are not authorized to create Submission")

        submission = serializer.save()

        program_owner = submission.program.user
        message = f"📢 *New Submission Created!* \n🔹 *Title:* {submission.title}\n🔹 *Severity:* {submission.severity}\n🔹 *Status:* {submission.status}"
        send_slack_notification(program_owner, message)


class SubmissionUpdateView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdminUser]
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        program_owner = instance.program.user  # Get the program's owner

        old_data = {
            "title": instance.title,
            "description": instance.description,
            "severity": instance.severity,
            "status": instance.status,
        }

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            # Identify which fields changed
            updated_fields = {}
            for field, old_value in old_data.items():
                new_value = request.data.get(field, old_value)
                if str(new_value) != str(old_value):
                    updated_fields[field] = {"old": old_value, "new": new_value}

            if updated_fields:
                message = f"✏️ *Submission Updated!* \n🔹 *Title:* {instance.title}\n"
                for field, changes in updated_fields.items():
                    message += f"🔄 *{field.capitalize()}*: `{changes['old']}` ➡ `{changes['new']}`\n"

                # Send Slack notification to the program owner
                send_slack_notification(program_owner, message)

            return Response(serializer.data)