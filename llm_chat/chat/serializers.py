from rest_framework import serializers

class ChatSerializer(serializers.Serializer):
    user_message = serializers.CharField()
    llm_choice = serializers.ChoiceField(choices=['llm1', 'llm2'])