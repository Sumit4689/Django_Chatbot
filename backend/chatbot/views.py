from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .rag.chain import get_chatbot
from .rag.ingest import ingest_data


@api_view(['POST'])
def chat(request):
    """Handle chat requests."""
    question = request.data.get('question', '')
    
    if not question:
        return Response(
            {'error': 'Question is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        chatbot = get_chatbot()
        response = chatbot.get_response(question)
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def clear_history(request):
    """Clear conversation history."""
    try:
        chatbot = get_chatbot()
        chatbot.clear_history()
        return Response(
            {'message': 'History cleared successfully'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def ingest(request):
    """Ingest documents and create vector store."""
    try:
        vectorstore = ingest_data()
        if vectorstore:
            return Response(
                {'message': 'Documents ingested successfully'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'No documents found to ingest'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health(request):
    """Health check endpoint."""
    return Response({'status': 'ok'}, status=status.HTTP_200_OK)

