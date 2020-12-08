from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ParseError

from app.models.post import Post
from app.services.post import (list_post, get_post, create_post, update_post,
                               delete_post, set_post_picture, count_post)


class PostListView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)

        class Meta:
            ref_name = 'PostListIn'
            fields = ['id']

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            ref_name = 'PostListOut'
            fields = ['id', 'content',
                      'published_date', 'post_picture']

    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(query_serializer=InputSerializer, responses={200: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = list_post(**serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_200_OK)


class PostGetView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)

        class Meta:
            ref_name = 'PostGetIn'
            fields = ['id']

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            ref_name = 'PostGetOut'
            fields = ['id', 'content',
                      'published_date', 'post_picture']

    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(query_serializer=InputSerializer, responses={200: OutputSerializer})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = get_post(**serializer.validated_data)
        return Response(self.OutputSerializer(result).data, status=status.HTTP_200_OK)


class PostCreateView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            ref_name = 'PostCreateIn'
            fields = ['content']

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            ref_name = 'PostCreateOut'
            fields = ['id', 'content',
                      'published_date', 'post_picture']

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=InputSerializer, responses={201: OutputSerializer()})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = create_post(account=request.user, **serializer.validated_data)
        return Response(self.OutputSerializer(result).data, status=status.HTTP_201_CREATED)


class PostUpdateView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        id = serializers.IntegerField(required=True)

        class Meta:
            model = Post
            ref_name = 'PostUpdateIn'
            fields = ['id', 'content']

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            ref_name = 'PostCreateOut'
            fields = ['id', 'content',
                      'published_date', 'post_picture']

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=InputSerializer, responses={200: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = update_post(account=request.user, **serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_200_OK)


class PostDeleteView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)

        class Meta:
            ref_name = 'PostDeleteIn'
            fields = ['id']

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            ref_name = 'PostCreateOut'
            fields = ['id', 'content',
                      'published_date', 'post_picture']

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=InputSerializer, responses={200: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = delete_post(account=request.user, **serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_200_OK)


class PostCountView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)

        class Meta:
            ref_name = 'PostCountIn'
            fields = ['id']

    class OutputSerializer(serializers.Serializer):
        count = serializers.IntegerField()

        class Meta:
            ref_name = 'PostCountOut'
            fields = ['count']

    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(query_serializer=InputSerializer, responses={200: OutputSerializer})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = count_post(**serializer.validated_data)
        return Response(self.OutputSerializer(result).data, status=status.HTTP_200_OK)


class PostPictureView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            set_post_picture(
                request.user, request.data['id'], request.data['file'])
        except KeyError:
            raise ParseError("'file' and/or 'id' field missing.")
        return Response("Uploaded.", status=status.HTTP_201_CREATED)
