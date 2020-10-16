from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models.user import User
from app.services.user import (create_user, get_user,
                                  set_profile_picture, update_user)


class UserProfilePictureView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            set_profile_picture(request.user, request.data['file'])
        except KeyError:
            raise ParseError("'file' field missing.")
        return Response("Uploaded.", status=status.HTTP_201_CREATED)


class UserGetView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)

        class Meta:
            ref_name = 'UserGetIn'
            fields = ['id']

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            ref_name = 'UserGetOut'
            fields = ['firstname', 'lastname', 'dateofbirth', 'gender',
                      'profile_picture', 'description']

    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(query_serializer=InputSerializer, responses={200: OutputSerializer})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = get_user(**serializer.validated_data)
        return Response(self.OutputSerializer(result).data, status=status.HTTP_200_OK)


class UserCreateView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            ref_name = 'UserCreateIn'
            fields = ['firstname', 'lastname',
                      'dateofbirth', 'gender', 'description']

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            ref_name = 'UserCreateOut'
            fields = ['firstname', 'lastname', 'dateofbirth', 'gender',
                      'profile_picture', 'description']

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=InputSerializer, responses={201: OutputSerializer})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = create_user(account=request.user, **
                                serializer.validated_data)
        return Response(self.OutputSerializer(result).data, status=status.HTTP_201_CREATED)


class UserUpdateView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            ref_name = 'UserUpdateIn'
            fields = ['firstname', 'lastname',
                      'dateofbirth', 'gender', 'description']

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            ref_name = 'UserUpdateOut'
            fields = ['firstname', 'lastname', 'dateofbirth', 'gender',
                      'profile_picture', 'description']

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=InputSerializer, responses={200: OutputSerializer})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = update_user(account=request.user, **
                                serializer.validated_data)
        return Response(self.OutputSerializer(result).data, status=status.HTTP_200_OK)
