from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from .models import Submission
from .serializers import SubmissionSerializer
# Create your views here.

class SubmissionListView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def perform_create(self, serializer):

        if self.request.user.role != 'researcher':
            raise PermissionDenied("You are not authorized to create Submission")
        serializer.save()


class SubmissionUpdateView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdminUser]
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()