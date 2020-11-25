from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView

from app.models.notification import Notification
from app.services.notification import list_notification


class NotificationListView(APIView):
    class InputSerializer(serializers.Serializer):
        t = serializers.IntegerField()

        class Meta:
            ref_name = 'NotificationListIn'
            fields = ['t']

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Notification
            ref_name = 'NotificationListOut'
            fields = '__all__'

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(query_serializer=InputSerializer, responses={200: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = list_notification(account=request.user, **serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_200_OK)
