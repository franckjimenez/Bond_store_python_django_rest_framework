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
            raise serializers.ValidationError(_('Bonds has already been purchased'),code='invalid')
        request = self.context.get('request', None)
        #print(self.Meta.model.create_id)

        #print(request.user)
        if self.Meta.model.create_id == request.user:
            raise serializers.ValidationError('It is a bond that you are selling.')
        return value

    def update(self, instance, validated_data):
        #print(validated_data)
        request = self.context.get('request', None)
        validated_data['buyer_id']=request.user
        return super().update(instance, validated_data) 
    
    


class BondPesosSerializer(serializers.ModelSerializer):
    class Meta:
        model= Bond
        fields=('id','type', 'total_sell', 'price_total',)
        read_only_fields = ['create_id','buyer_id']

    def to_internal_value(self, data):
        price_total=data.get('price_total')
        # Validation
        price_serializer = PriceSerializer(data=data)
        if not price_serializer.is_valid():
              raise serializers.ValidationError('The price_total should have a valid format.')
        
        data['price_total']=price_total.replace(',','')
        return super().to_internal_value(data)

    def to_representation(self, instance):
        data=super(BondPesosSerializer,self).to_representation(instance)
        price_totaltemp="${:,.4f} MXN".format(Decimal(data['price_total']))
        data['price_total']=price_totaltemp
        return data

    def create(self,validated_data):
        request = self.context.get('request', None)
        #print(validated_data)
        validated_data['create_id']=request.user
        bond=Bond(**validated_data)
        #print(validated_data)
        bond.save()
        return bond

    

class BondPesosListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Bond
        fields = '__all__'

    def to_representation(self, instance):
        data=super(BondPesosListSerializer,self).to_representation(instance)
        price_totaltemp="${:,.4f} MXN".format(Decimal(data['price_total']))
        data['price_total']=price_totaltemp
        return data

class BondDollarsListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Bond
        fields = '__all__'
    def to_representation(self, instance):
        data=super(BondDollarsListSerializer,self).to_representation(instance)
        update_data_from_banxico()
        dollar_price=Banxico.objects.first().dollar_price
        price_totaltemp="${:,.4f} USD".format(Decimal(data['price_total'])/Decimal(dollar_price))
        data['price_total']=price_totaltemp
        return data







#^(100,000,000.0000|([1-9]\d,\d\d\d,\d\d\d\d|[1-9],\d\d\d,\d\d\d|[1-9]\d\d,\d\d\d|[1-9]\d,\d\d\d|[1-9],\d\d\d|[1-9]\d\d|[1-9]\d|\d)(\.\d\d\d\d))$
#^(100,000,000.0000|((([1-9]\d|[1-9]),\d\d\d|[1-9]\d\d|[1-9]\d|[1-9]),\d\d\d|[1-9]\d\d|[1-9]\d|\d)(\.\d\d\d\d))$
#^(10{2},0{3},0{3}.0{4}|((([1-9]\d|[1-9]),\d{3}|[1-9]\d\d|[1-9]\d|[1-9]),\d{3}|[1-9]\d\d|[1-9]\d|\d)(\.\d{4}))$
regex_pesos = RegexValidator(r'^(10{2},0{3},0{3}.0{4}|((([1-9]\d|[1-9]),\d{3}|[1-9]\d\d|[1-9]\d|[1-9]),\d{3}|[1-9]\d\d|[1-9]\d|\d)(\.\d{4}))$', "Monetary value, range 0.0000 to 100,000,000.0000 with resolution of four decimal numbers.")
class PriceSerializer(serializers.Serializer):
    price_total=serializers.CharField(
        max_length=16,
        validators=[regex_pesos]
        )

regex_type = RegexValidator(r'^(\d|[a-zA-Z]){8,40}$', "The type should be be alphanumeric from 8 to 40 characters.")

class TypeSerializer(serializers.Serializer):
    type= serializers.CharField(
        max_length=40,
        validators=[regex_type]
    )