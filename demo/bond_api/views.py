from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from bond_api.models import Bond
from bond_api.serializers import ( BondPesosSerializer,
                                    BondBuySerializer,
                                    IntegerSerializer,BondDollarsSerializer)



class BondsAPIView(APIView):
    #serializer_class =BondPesosSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        # current_user = request.user
        # print(current_user.id)
        bonds = Bond.objects.all()
        bonds_serializer = BondPesosSerializer(bonds, many=True)
        return Response(bonds_serializer.data,status =status.HTTP_200_OK)

        
class BondsDollarsAPIView(APIView):
    #serializer_class =BondPesosSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # current_user = request.user
        # print(current_user.id)
        bonds = Bond.objects.all()
        bonds_serializer = BondDollarsSerializer(bonds, many=True)
        return Response(bonds_serializer.data,status =status.HTTP_200_OK)



class Sell_BondsAPIView(APIView):
    serializer_class =BondPesosSerializer
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        print(request.data)
        bond_id_serializer=IntegerSerializer(data=request.data)
    
        if bond_id_serializer.is_valid():
            print("Pase primera validacion")
            bond=Bond.objects.all().get(id=request.data['bond_id'])
           
            if(bond is None):
                return Response("Error - Bond not found", status=status.HTTP_400_BAD_REQUEST)
            bondrequest=model_to_dict(bond)
            print("Bond(bond)")
            print(bond, bondrequest)
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



            


# class BondView(APIView):
#     throttle_scope = 'general_calls'
#     permission_classes = (IsAuthenticated,)
#     @detail_route(methods=['post'])
#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)



# class BondsViewSet(viewsets.ModelViewSet):
#     serializer_class = BondPesosSerializer
#     queryset=models.Bond.objects.all()

    # def get_queryset(self,pk=None):
    #     if(pk is None):
    #         return self.get_serializer().Meta.model.objects.all()
    #     return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # def list(self,request):
    #     bond_serializer=self.get_serializer(self.queryset,many=True)
    #     return Response(bond_serializer.data,status= status.HTTP_200_OK)
    # throttle_scope = 'general_calls'
    # #permission_classes = (IsAuthenticated,)
    # def list(self, request):
    #     serializer_class = BondPesosSerializer
    #     queryset= models.Bond.objects.all()
 
