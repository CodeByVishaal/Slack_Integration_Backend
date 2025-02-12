from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics
from .serializers import ProgramSerializer
from .models import Program
# Create your views here.

class ProgramListView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ProgramSerializer

    def get_queryset(self):
        return Program.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role != 'customer':
            raise PermissionDenied("You do not have permission to create a program.")
        serializer.save()

class ProgramUpdateView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdminUser]
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()

