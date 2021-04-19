
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from AiContestWeb.snippets.model import Snippet
from AiContestWeb.snippets.serializer import SnippetSerializer
from AiContestWeb.uaa.permissions import IsStudentUser


@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsStudentUser, IsAuthenticated])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
