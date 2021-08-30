from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
    def get(self, request):
        users=User.objects.all()
        users_serializer=UserSerializer(users,many=True)
        return Response(users_serializer.data)
 


    

