from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ParseError
from drf_yasg.utils import swagger_auto_schema

from app.exceptions import InvalidInputFormat
from app.models.comment import Comment
from app.services.comment import list_comment, create_comment, update_comment, delete_comment


class CommentListView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)

        class Meta:
            ref_name = 'CommentListIn'
            fields = ['id']

    class OutputSerializer(serializers.ModelSerializer):
        user_id = serializers.SerializerMethodField()
        user_firstname = serializers.SerializerMethodField()
        user_lastname = serializers.SerializerMethodField()
        user_profile_picture = serializers.SerializerMethodField()

        def get_user_id(self, obj):
            return obj.user.account.id

        def get_user_firstname(self, obj):
            return obj.user.firstname

        def get_user_lastname(self, obj):
            return obj.user.lastname

        def get_user_profile_picture(self, obj):
            return obj.user.profile_picture.url

        class Meta:
            model = Comment
            ref_name = 'CommentListOut'
            fields = ['id', 'user_id', 'user_firstname', 'user_lastname',
                      'user_profile_picture', 'content', 'published_date']

    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(query_serializer=InputSerializer, responses={200: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = list_comment(**serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_200_OK)


class CommentCreateView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)
        content = serializers.CharField(required=True)

        class Meta:
            ref_name = 'CommentCreateIn'
            fields = ['id', 'content']

    class OutputSerializer(serializers.ModelSerializer):
        user_id = serializers.SerializerMethodField()
        user_firstname = serializers.SerializerMethodField()
        user_lastname = serializers.SerializerMethodField()
        user_profile_picture = serializers.SerializerMethodField()

        def get_user_id(self, obj):
            return obj.user.account.id

        def get_user_firstname(self, obj):
            return obj.user.firstname

        def get_user_lastname(self, obj):
            return obj.user.lastname

        def get_user_profile_picture(self, obj):
            return obj.user.profile_picture.url

        class Meta:
            model = Comment
            ref_name = 'CommentCreateOut'
            fields = ['id', 'user_id', 'user_firstname', 'user_lastname',
                      'user_profile_picture', 'content', 'published_date']

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=InputSerializer, responses={201: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = create_comment(account=request.user, **serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_201_CREATED)


class CommentUpdateView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)
        content = serializers.CharField(required=True)

        class Meta:
            ref_name = 'CommentUpdateIn'
            fields = ['id', 'content']

    class OutputSerializer(serializers.ModelSerializer):
        user_id = serializers.SerializerMethodField()
        user_firstname = serializers.SerializerMethodField()
        user_lastname = serializers.SerializerMethodField()
        user_profile_picture = serializers.SerializerMethodField()

        def get_user_id(self, obj):
            return obj.user.account.id

        def get_user_firstname(self, obj):
            return obj.user.firstname

        def get_user_lastname(self, obj):
            return obj.user.lastname

        def get_user_profile_picture(self, obj):
            return obj.user.profile_picture.url

        class Meta:
            model = Comment
            ref_name = 'CommentUpdateOut'
            fields = ['id', 'user_id', 'user_firstname', 'user_lastname',
                      'user_profile_picture', 'content', 'published_date']

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=InputSerializer, responses={201: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = update_comment(account=request.user, **serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_201_CREATED)


class CommentDeleteView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)

        class Meta:
            ref_name = 'CommentDeleteIn'
            fields = ['id']

    class OutputSerializer(serializers.ModelSerializer):
        user_id = serializers.SerializerMethodField()
        user_firstname = serializers.SerializerMethodField()
        user_lastname = serializers.SerializerMethodField()
        user_profile_picture = serializers.SerializerMethodField()

        def get_user_id(self, obj):
            return obj.user.account.id

        def get_user_firstname(self, obj):
            return obj.user.firstname

        def get_user_lastname(self, obj):
            return obj.user.lastname

        def get_user_profile_picture(self, obj):
            return obj.user.profile_picture.url

        class Meta:
            model = Comment
            ref_name = 'CommentDeleteOut'
            fields = ['id', 'user_id', 'user_firstname', 'user_lastname',
                      'user_profile_picture', 'content', 'published_date']

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=InputSerializer, responses={201: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = delete_comment(account=request.user, **serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_201_CREATED)
