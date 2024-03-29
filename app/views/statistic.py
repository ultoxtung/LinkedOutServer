from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from app.services.statistic import users_by_skill, jobs_by_skill


class UsersBySkillView(APIView):
    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        count = serializers.IntegerField()

        class Meta:
            ref_name = 'UsersBySkillOut'
            fields = ['name', 'count']

    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(responses={200: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        result = users_by_skill()
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_200_OK)


class JobsBySkillView(APIView):
    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        count = serializers.IntegerField()

        class Meta:
            ref_name = 'JobsBySkillOut'
            fields = ['name', 'count']

    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(responses={200: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        result = jobs_by_skill()
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_200_OK)
