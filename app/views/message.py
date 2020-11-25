from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView

from app.models.message import Message
from app.services.message import send_message, list_conversation, get_conversation


class MessageSendView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        type = serializers.CharField()
        content = serializers.CharField()

        class Meta:
            ref_name = 'MessageSendIn'
            fields = ['id', 'type', 'content']

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=InputSerializer, responses={201: "Message sent"})
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sent = send_message(account=request.user, **serializer.validated_data)
        if not sent:
            return Response("Message failed to send", status=status.HTTP_502_BAD_GATEWAY)
        return Response("Message sent", status=status.HTTP_201_CREATED)


class ConversationListView(APIView):
    class InputSerializer(serializers.Serializer):
        t = serializers.IntegerField()

        class Meta:
            ref_name = 'ConversationListIn'
            fields = ['t']

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        profile_picture = serializers.ImageField()
        last_message_content = serializers.CharField()
        last_message_timestamp = serializers.IntegerField()
        outgoing = serializers.BooleanField()

        class Meta:
            ref_name = 'ConversationListOut'
            fields = ['id', 'name', 'profile_picture', 'last_message_content',
                      'last_message_timestamp', 'outgoing']

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(query_serializer=InputSerializer, responses={200: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = list_conversation(account=request.user, **serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_200_OK)


class ConversationGetView(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        t = serializers.IntegerField()

        class Meta:
            ref_name = 'ConversationGetIn'
            fields = ['id', 't']

    class OutputSerializer(serializers.ModelSerializer):
        sender_id = serializers.SerializerMethodField()
        receiver_id = serializers.SerializerMethodField()

        def get_sender_id(self, obj):
            return obj.sender.id

        def get_receiver_id(self, obj):
            return obj.receiver.id

        class Meta:
            model = Message
            ref_name = 'ConversationGetOut'
            fields = ['sender_id', 'receiver_id', 'type', 'content', 'published_date']

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(query_serializer=InputSerializer, responses={200: OutputSerializer(many=True)})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        result = get_conversation(account=request.user, **serializer.validated_data)
        return Response(self.OutputSerializer(result, many=True).data, status=status.HTTP_200_OK)
