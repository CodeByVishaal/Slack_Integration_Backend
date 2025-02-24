from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
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
        user = self.request.user
        if self.request.user.role != 'customer':
            raise PermissionDenied("You do not have permission to create a program.")

        updated_instance = serializer.save(user=user)  # Save the updated data
        user = self.request.user
        # Create a Slack notification message
        message = f"🔔 *{user.first_name} {user.last_name} Created a Program!*\n" \
                  f"📌 *Title:* {updated_instance.title}\n" \
                  f"📄 *Description:* {updated_instance.description}\n" \
                  f"⚠️ *Severity:* {updated_instance.severity}\n" \
                  f"📌 *Status:* {updated_instance.status}\n"

        # Send the Slack notification
        send_slack_notification(user, message)


class ProgramUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        old_data = {
            "title": instance.title,
            "description": instance.description,
            "severity": instance.severity,
            "status": instance.status,
        }
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            updated_fields = {}
            for field, old_value in old_data.items():
                new_value = request.data.get(field, old_value)
                if str(new_value) != str(old_value):
                    updated_fields[field] = {"old": old_value, "new": new_value}

            print(updated_fields)
            if updated_fields:
                message = f"🔔 *{instance.user.first_name} {instance.user.last_name} Updated: {instance.title}* 🔔\n"
                for field, changes in updated_fields.items():
                    message += f"📝 *{field.capitalize()}*: `{changes['old']}` ➡ `{changes['new']}`\n"

                print(message)
                send_slack_notification(instance.user, message)
            return Response(serializer.data)

        response = super().update(request, *args, **kwargs)


        return response

