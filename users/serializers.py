from .models import Profile
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    raise ValidationError("User is deactivate")
            else:
                raise ValidationError("Unable to login with given credentials")
        else:
            raise ValidationError("Must provide username or password")
        return data


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True, max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password1 = serializers.CharField(required=True, min_length=8, write_only=True)
    password2 = serializers.CharField(required=True, min_length=8, write_only=True)

    def create(self, validated_data):
        if validated_data['password1'] == validated_data['password2']:
            user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                            validated_data['password1'])

            return user
        else:
            raise ValidationError("Passwords do not match")

    class Meta:
        model = User
        fields = ('id', 'username', 'password1', 'password2', 'email')


class ProfileUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(required=False,
                                       max_length=30)
    last_name = serializers.CharField(required=False,
                                      max_length=150)

    class Meta:
        model = Profile
        fields = ('id', 'user_id', 'email', 'first_name', 'last_name', 'status', 'photo')
        read_only_fields = ('user_id',)
