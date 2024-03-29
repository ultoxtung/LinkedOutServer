from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_yasg.utils import swagger_auto_schema

from app.models.account import Account
from app.services.account import (login, create_account, change_password,
                                  push_device_token)
from app.utils import inline_serializer


class LoginView(APIView):
    class OutputSerializer(serializers.Serializer):
        access_token = serializers.CharField()
        account = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'username': serializers.CharField(),
            'account_type': serializers.CharField(),
        })

        class Meta:
            ref_name = 'Login'
            fields = ['access_token', 'account']

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField(required=True)
        password = serializers.CharField(required=True)

        class Meta:
            ref_name = 'Login'
            fields = ['username', 'password']

    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(request_body=InputSerializer, responses={200: OutputSerializer})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = login(**serializer.validated_data)
        return Response(self.OutputSerializer(result).data)


class RegisterView(APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField(required=True)
        password = serializers.CharField(required=True)
        email = serializers.CharField(required=True)
        account_type = serializers.CharField(required=True)

        class Meta:
            ref_name = 'RegisterIns'
            fields = ['username', 'password', 'email', 'account_type']

    class OutputSerializer(serializers.Serializer):
        access_token = serializers.CharField()
        account = inline_serializer(fields={
            'id': serializers.IntegerField(),
            'username': serializers.CharField(),
            'account_type': serializers.CharField(),
        })

        class Meta:
            ref_name = 'RegisterOut'
            fields = ['access_token', 'account']

    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(request_body=InputSerializer, responses={201: OutputSerializer})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_existed, result = create_account(**serializer.validated_data)
        if user_existed:
            return Response({'detail': 'User already exist.'}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(self.OutputSerializer(result).data, status=status.HTTP_201_CREATED)


class ChangePasswordView(APIView):
    class InputSerializer(serializers.Serializer):
        current_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True)

        class Meta:
            ref_name = 'ChangePassword'
            fields = ['current_password', 'new_password']

    @swagger_auto_schema(request_body=InputSerializer, responses={200: "Password changed"})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        change_password(account=request.user, **serializer.validated_data)
        return Response("Password changed", status=status.HTTP_200_OK)


class PushDeviceTokenView(APIView):
    class InputSerializer(serializers.Serializer):
        device_token = serializers.CharField(required=True)

        class Meta:
            ref_name = 'PushDeviceTokenIn'
            fields = ['device_token']

    @swagger_auto_schema(request_body=InputSerializer, responses={200: "Device registered"})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        push_device_token(account=request.user, **serializer.validated_data)
        return Response("Device registered", status=status.HTTP_200_OK)
