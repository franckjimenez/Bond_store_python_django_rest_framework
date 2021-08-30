from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from user_api.serializers import UserSerializer
from user_api.models import User


class HelloView(APIView):
    throttle_scope = 'general_calls'
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class UsersAPIView(APIView):
    throttle_scope = 'general_calls'
    #permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def post(self, request, ):
        """
        Post:
        Create a new bond and associate create_id with the current user.
        """

        serializer = UserSerializer( data=request.data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 


    

