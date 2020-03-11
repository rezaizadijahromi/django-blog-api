from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = {
            'username','email',
            'first_name','last_name'
        }


class UserCreateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(label='Email Address')
    email2 = serializers.EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = (
            'username',
            'email','email2',
            'password'
        )

        extra_kwargs = {
            'password':{
                'write_only':'True'
            }
        }

    def validate(self, attrs):
        return super().validate(attrs)

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get('email2')
        email2 = value
        if email1 != email2:
            raise serializers.ValidationError('emauls must match')

        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise serializers.ValidationError('This user has already registered')

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise serializers.ValidationError('Emails must match')
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class UserLoginSerializer(serializers.ModelSerializer):

    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField()
    email = serializers.CharField(label='Email Address')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'token'
        )

        extra_kwargs = {
            'password':{
                'write_only':True
            }
        }

    def validate(self, attrs):
        return super().validate(attrs)

