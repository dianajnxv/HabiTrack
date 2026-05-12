from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import AIAgentService

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_endpoint(request):
    user_message = request.data.get('message')
    if not user_message:
        return Response({'error': 'No message provided'}, status=400)
        
    agent = AIAgentService(request.user)
    reply = agent.get_response(user_message)
    return Response({'reply': reply})