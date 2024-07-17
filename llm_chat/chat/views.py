from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatSerializer
from django.conf import settings
from transformers import pipeline

# Load LLMs
llm1 = pipeline('conversational', model="microsoft/DialoGPT-medium")
llm2 = pipeline('conversational', model="facebook/blenderbot-400M-distill")

# Select LLM based on user choice
LLM_MAP = {
    'llm1': llm1,
    'llm2': llm2,
}

class ChatAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            user_message = serializer.validated_data['user_message']
            llm_choice = serializer.validated_data['llm_choice']
            llm = LLM_MAP[llm_choice]

            # Generate response from the selected LLM
            response = llm(user_message)
            response_text = response[0]['generated_text']

            # Save chat to MongoDB
            settings.db.chats.insert_one({
                'user_message': user_message,
                'response_text': response_text,
                'llm_choice': llm_choice,
            })

            return Response({'response': response_text}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatHistoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        llm_choice = request.query_params.get('llm_choice')
        if llm_choice:
            chats = list(settings.db.chats.find({'llm_choice': llm_choice}))
        else:
            chats = list(settings.db.chats.find())
        
        for chat in chats:
            chat['_id'] = str(chat['_id'])
        
        return Response(chats, status=status.HTTP_200_OK)