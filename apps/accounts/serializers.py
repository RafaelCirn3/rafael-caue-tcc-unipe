from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'school_name',
            'city',
            'state',
            'xp',
            'avatar',
            'financial_goal',
            'preferences',
            'financial_profile',
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            'school_name',
            'city',
            'state',
            'avatar',
            'financial_goal',
            'preferences',
            'financial_profile',
        )

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Este e-mail ja esta em uso.')
        return value.lower()

    def create(self, validated_data):
        username = validated_data.get('username') or validated_data['email'].split('@')[0]
        user = User.objects.create_user(
            username=username,
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            school_name=validated_data.get('school_name', ''),
            city=validated_data.get('city', ''),
            state=validated_data.get('state', ''),
            avatar=validated_data.get('avatar', ''),
            financial_goal=validated_data.get('financial_goal', 0),
            preferences=validated_data.get('preferences', {}),
            financial_profile=validated_data.get('financial_profile', {}),
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'school_name',
            'city',
            'state',
            'avatar',
            'financial_goal',
            'preferences',
            'financial_profile',
        )


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

    def validate(self, attrs):
        email = attrs.get('email', '').lower()
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            try:
                user_obj = User.objects.get(email__iexact=email)
                user = authenticate(
                    request=self.context.get('request'),
                    username=user_obj.username,
                    password=password,
                )
            except User.DoesNotExist:
                user = None

        if not user:
            raise serializers.ValidationError('Credenciais invalidas.')

        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data,
        }


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self):
        email = self.validated_data['email'].lower()
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        self.context['reset_uid'] = uid
        self.context['reset_token'] = token
        self.context['reset_email'] = user.email


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs['uid']))
            user = User.objects.get(pk=uid)
        except (ValueError, TypeError, User.DoesNotExist):
            raise serializers.ValidationError('Token de redefinicao invalido.')

        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError('Token de redefinicao invalido.')

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])