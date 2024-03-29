from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ParseError

from app.models.job import Job
from app.models.skill import Skill
from app.models.city import City
from app.services.job import (get_job, list_job, create_job, update_job,
                              delete_job, set_job_picture, count_job)


class SkillRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return Skill.objects.get(name=data)
        except:
            raise ParseError('Skill doesn\'t exist')


class CityRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return City.objects.get(name=data)
        except:
            raise ParseError('City doesn\'t exist')


class JobListView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)

        class Meta:
            ref_name = 'JobListIn'
            fields = ['id']

    class OutputSerializer(serializers.ModelSerializer):
        cities = CityRelatedField(queryset=City.objects.all(), many=True)
        skills = SkillRelatedField(queryset=Skill.objects.all(), many=True)

        class Meta:
            model = Job
            ref_name = 'JobListOut'
            fields = ['id', 'title', 'description', 'seniority_level', 'employment_type',
                      'recruitment_url', 'published_date', 'job_picture', 'cities', 'skills']

    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(query_serializer=InputSerializer, responses={200: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = list_job(**serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_200_OK)


class JobGetView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)

        class Meta:
            ref_name = 'JobGetIn'
            fields = ['id']

    class OutputSerializer(serializers.ModelSerializer):
        account_id = serializers.SerializerMethodField()
        company_name = serializers.SerializerMethodField()
        company_profile_picture = serializers.SerializerMethodField()
        cities = CityRelatedField(queryset=City.objects.all(), many=True)
        skills = SkillRelatedField(queryset=Skill.objects.all(), many=True)

        def get_account_id(self, obj):
            return obj.company.account.id

        def get_company_name(self, obj):
            return obj.company.name

        def get_company_profile_picture(self, obj):
            return obj.company.profile_picture.url

        class Meta:
            model = Job
            ref_name = 'JobGetOut'
            fields = ['id', 'account_id', 'company_name',
                      'company_profile_picture', 'title', 'description',
                      'seniority_level', 'employment_type', 'recruitment_url',
                      'published_date', 'job_picture', 'cities', 'skills']

    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(query_serializer=InputSerializer, responses={200: OutputSerializer})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = get_job(**serializer.validated_data)
        return Response(self.OutputSerializer(result).data, status=status.HTTP_200_OK)


class JobCreateView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        cities = CityRelatedField(queryset=City.objects.all(), many=True)
        skills = SkillRelatedField(queryset=Skill.objects.all(), many=True)

        class Meta:
            model = Job
            ref_name = 'JobCreateIn'
            fields = ['title', 'description', 'seniority_level', 'employment_type',
                      'recruitment_url', 'cities', 'skills']

    class OutputSerializer(serializers.ModelSerializer):
        cities = CityRelatedField(queryset=City.objects.all(), many=True)
        skills = SkillRelatedField(queryset=Skill.objects.all(), many=True)

        class Meta:
            model = Job
            ref_name = 'JobCreateOut'
            fields = ['id', 'title', 'description', 'seniority_level', 'employment_type',
                      'recruitment_url', 'published_date', 'job_picture', 'cities', 'skills']

    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # authentication_classes = []

    @swagger_auto_schema(request_body=InputSerializer, responses={201: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = create_job(account=request.user, **serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_201_CREATED)


class JobUpdateView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        id = serializers.IntegerField(required=True)
        cities = CityRelatedField(queryset=City.objects.all(), many=True, required=True)
        skills = SkillRelatedField(queryset=Skill.objects.all(), many=True, required=True)

        class Meta:
            model = Job
            ref_name = 'JobUpdateIn'
            fields = ['id', 'title', 'description', 'seniority_level', 'employment_type',
                      'recruitment_url', 'cities', 'skills']

    class OutputSerializer(serializers.ModelSerializer):
        cities = CityRelatedField(queryset=City.objects.all(), many=True)
        skills = SkillRelatedField(queryset=Skill.objects.all(), many=True)

        class Meta:
            model = Job
            ref_name = 'JobUpdateOut'
            fields = ['id', 'title', 'description', 'seniority_level', 'employment_type',
                      'recruitment_url', 'published_date', 'job_picture', 'cities', 'skills']

    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # authentication_classes = []

    @swagger_auto_schema(request_body=InputSerializer, responses={200: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = update_job(account=request.user, **serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_200_OK)


class JobDeleteView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)

        class Meta:
            ref_name = 'JobDeleteIn'
            fields = ['id']

    class OutputSerializer(serializers.ModelSerializer):
        cities = CityRelatedField(queryset=City.objects.all(), many=True)
        skills = SkillRelatedField(queryset=Skill.objects.all(), many=True)

        class Meta:
            model = Job
            ref_name = 'JobDeleteOut'
            fields = ['id', 'title', 'description', 'seniority_level', 'employment_type',
                      'recruitment_url', 'published_date', 'job_picture', 'cities', 'skills']

    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # authentication_classes = []

    @swagger_auto_schema(request_body=InputSerializer, responses={200: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = delete_job(account=request.user, **serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_200_OK)


class JobCountView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)

        class Meta:
            ref_name = 'JobCountIn'
            fields = ['id']

    class OutputSerializer(serializers.Serializer):
        count = serializers.IntegerField()

        class Meta:
            ref_name = 'JobCountOut'
            fields = ['count']

    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(query_serializer=InputSerializer, responses={200: OutputSerializer})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = count_job(**serializer.validated_data)
        return Response(self.OutputSerializer(result).data, status=status.HTTP_200_OK)


class JobPictureView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            set_job_picture(request.user, request.data['id'], request.data['file'])
        except KeyError:
            raise ParseError("'file' and/or 'id' field missing.")
        return Response("Uploaded.", status=status.HTTP_201_CREATED)
