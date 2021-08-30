from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from bond_api.models import Bond
from bond_api.serializers import ( BondPesosSerializer,
                                    BondBuySerializer,
                                    IntegerSerializer,
                                    BondPesosListSerializer,
                                    BondDollarsListSerializer)



class BondsAPIView(APIView):
    """
        GET:
        Return a list of bonds with the price in Mexican currency.
    """
    #serializer_class =BondPesosSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses={200: BondPesosListSerializer(many=True)})
    def get(self, request):
       
        # current_user = request.user
        # print(current_user.id)
        bonds = Bond.objects.all()
        bonds_serializer = BondPesosListSerializer(bonds, many=True)
        return Response(bonds_serializer.data,status =status.HTTP_200_OK)

        
class BondsDollarsAPIView(APIView):
    """
        GET:
        Return a list of bonds with the price in US dollars.
    """
    #serializer_class =BondPesosSerializer
    throttle_scope = 'general_calls'
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses={200: BondDollarsListSerializer(many=True)})
    def get(self, request):
        # current_user = request.user
        # print(current_user.id)
        bonds = Bond.objects.all()
        bonds_serializer = BondDollarsListSerializer(bonds, many=True)
        return Response(bonds_serializer.data,status =status.HTTP_200_OK)



class Sell_BondsAPIView(APIView):
    """
        Post:
        Create a new bond and associate create_id with the current user.
    """
    throttle_scope = 'general_calls'
    serializer_class =BondPesosSerializer
    permission_classes = (IsAuthenticated,)
    

    @swagger_auto_schema(responses={200: BondPesosSerializer(many=True)})
    def post(self, request, ):
        
        # print(request.data)

        current_user = request.user
        # print(current_user.id)
        # print(request.data)
        serializer = BondPesosSerializer(
            data=request.data,
            context={'request': request},
            many=isinstance(request.data,list)
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Buy_BondsAPIView(APIView):
    """
        Post:
        Update a bond because associate buyer_id with the current user.
    """
    throttle_scope = 'general_calls'
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        
        #print(request.data)
        bond_id_serializer=IntegerSerializer(data=request.data)
    
        if bond_id_serializer.is_valid():
            #print("Pase primera validacion")
            bond=Bond.objects.all().get(id=request.data['bond_id'])
           
            if(bond is None):
                return Response("Error - Bond not found", status=status.HTTP_400_BAD_REQUEST)
            bondrequest=model_to_dict(bond)
            #print("Bond(bond)")
            #print(bond, bondrequest)
            bondbuy_serializer=BondBuySerializer(
                                    bond,
                                    data=bondrequest,
                                    context={'request': request})
            if bondbuy_serializer.is_valid():
                bondbuy_serializer.save()
                return Response(bondbuy_serializer.data, status=status.HTTP_200_OK)
            else:
                
                return Response(bondbuy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(bond_id_serializer.errors, status=status.HTTP_400_BAD_REQUEST)