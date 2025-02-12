from rest_framework import generics, status
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
# Create your views here.

class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    def create(self, request):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            error_messages = serializer.errors
            return Response({'error':error_messages}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            {'message':'User is succussfully Registered.',
             'data':serializer.data}
        )

class LoginView(generics.CreateAPIView):

    serializer_class = LoginSerializer

    def create(self, request):

        serializer = self.get_serializer(data=request.data)

        serializer = self.get_serializer(data = request.data)
        if not serializer.is_valid():
            error_messages = serializer.errors
            return Response({"error": error_messages}, status=status.HTTP_400_BAD_REQUEST)

        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response