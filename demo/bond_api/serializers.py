from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from rest_framework import serializers
from bond_api.models import Bond
from banxico_externalapi.models import Banxico
from banxico_externalapi.services import update_data_from_banxico




# class BondSerializer(serializers.Serializer):
#     class Meta:
#         model= Bond
#         fields = '__all__';

class IntegerSerializer(serializers.Serializer):
    bond_id=serializers.IntegerField(validators=[MinValueValidator(0),])

class BondBuySerializer(serializers.ModelSerializer):
    class Meta:
        model= Bond
        fields='__all__'

    def validate_buyer_id(self, value):

        if value is not None:
            raise serializers.ValidationError('Bonds has already been purchased')
        request = self.context.get('request', None)
        print(self.Meta.model.create_id)

        print(request.user)
        if self.Meta.model.create_id == request.user:
            raise serializers.ValidationError('It is a bond that you are selling.')
        return value
    


    def update(self, instance, validated_data):
        print(validated_data)
        request = self.context.get('request', None)
        validated_data['buyer_id']=request.user
        return super().update(instance, validated_data) 
    
    


class BondPesosSerializer(serializers.ModelSerializer):
    class Meta:
        model= Bond
        fields = '__all__'
        #fields=('id','type', 'total_sell', 'price_total',)
        #read_only_fields = ['create_id','buyer_id']
    
    def validate_type(self, value):
        print("Estoy en valid type")
        print(value)
        type_serializer = TypeSerializer(data=value)
        if not type_serializer.is_valid():
            raise ValidationError(type_serializer.errors)
        return value
    
    def to_internal_value(self, data):
        #print('internal')
        price_total=data.get('price_total')
        print(data)
        # Validation
        price_serializer = PriceSerializer(data=data)
        if not price_serializer.is_valid():
              raise ValidationError('The price_total should have a valid format.')
        #print(type(data))
        
        data['price_total']=price_total.replace(',','')
        #print('internal')
        return data

    def to_representation(self, instance):
        data=super(BondPesosSerializer,self).to_representation(instance)
        # print(data)
        # print(data['price_total'])
        price_totaltemp="${:,.4f} MXN".format(Decimal(data['price_total']))
        data['price_total']=price_totaltemp
        return data
        # return {
        #     'id':instance['id'],
        #     'type':instance['type'],
        #     'total_sell':instance['total_sell'],
        #     'price_total': price_total,
        #     'create_id': instance['create_id'],
        #     'buyer_id': instance['buyer_id']
        # }

    def create(self,validated_data):
        print(validated_data)
        request = self.context.get('request', None)
        validated_data['create_id']=request.user
        return Bond.objects.create(**validated_data)
    



class BondDollarsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Bond
        fields = '__all__'
    def to_representation(self, instance):

                


        data=super(BondDollarsSerializer,self).to_representation(instance)
        update_data_from_banxico()
        dollar_price=Banxico.objects.first().dollar_price
        price_totaltemp="${:,.4f} USD".format(Decimal(data['price_total'])/Decimal(dollar_price))
        data['price_total']=price_totaltemp
        return data








regex_pesos = RegexValidator(r'^(100,000,000.0000|((([1-9]\d|[1-9]),\d{3}|[1-9]\d|[1-9]),\d{3}|[1-9]\d{2}|[1-9]\d|\d)(\.\d{4}))$', "The type should be be alphanumeric from 8 to 40 characters.")

class PriceSerializer(serializers.Serializer):
    price_total=serializers.CharField(
        max_length=40,
        validators=[regex_pesos]
        )

regex_type = RegexValidator(r'^(\d|[a-zA-Z]){8,40}$', "The type should be be alphanumeric from 8 to 40 characters.")

class TypeSerializer(serializers.Serializer):
    type= serializers.CharField(
        max_length=40,
        validators=[regex_type]
    )