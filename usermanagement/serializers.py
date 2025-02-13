from rest_framework import serializers
from .models import User
from django.utils import timezone
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(min_length = 3, max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=100, required=True)
    role = serializers.CharField(required=True, max_length=20)
    password = serializers.CharField(min_length=5, max_length=20, write_only=True, style={'input_type':'password'})
    confirm_password = serializers.CharField(min_length=5, max_length=20, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'role', 'password', 'confirm_password']

    def validate(self, data):
        username = data.get('username')
        first_name = data.get('first_name')
        role = data.get('role').lower()
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        roles = ['customer', 'researcher', 'admin']

        if first_name and first_name.isupper():
            raise  serializers.ValidationError({'first_name':"First Name should not contain uppercase letter"})

        if role and role not in roles:
            raise serializers.ValidationError({'role': "Provide a valid Role for the User"})

        if password != confirm_password:
            raise  serializers.ValidationError({'password':"Password does not match", 'confirm_password':"Password does not match"})

        username_exists = User.objects.filter(username = username).exists()
        email_exists = User.objects.filter(email=email).exists()

        if username_exists:
            raise serializers.ValidationError({'username':'Username already exists, try using different username.'})

        if email_exists:
            raise serializers.ValidationError({'username':'Email already exists, try using different email.'})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        validated_data['role'] = validated_data.get('role').lower()

        if validated_data.get('role') == 'admin':
            return User.objects.create_superuser(**validated_data)

        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=5, style={'input_type':'password'}, write_only=True)
    username = serializers.CharField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    role = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user_data = User.objects.filter(email=email).first()

        if not user_data:
            raise serializers.ValidationError(
                {'message':'Invalid user, Please check provided credentials'}
            )

        if not user_data.is_active:
            raise serializers.ValidationError(
                {'AuthorizationError':'User is Inactive, Please verify your email and your account will be activated by our internal team.'}
                )
        if user_data:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )
            if not user:
                raise serializers.ValidationError({'AuthorizationError':'Invalid Credentials provided\nPlease check the provided credentials'})

            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            user_token = user.token()

            return {
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'role': user.role,
            'access_token': str(user_token.get('access_token')),
            'refresh_token':str(user_token.get('refresh_token')),
            }

        else:
            raise serializers.ValidationError({'AuthorizationError':'Invalid User'})