from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from rest_framework import serializers
from bond_api.models import Bond
from bond_api.models import Bond

class IntegerSerializer(serializers.Serializer):
    bond_id=serializers.IntegerField(validators=[MinValueValidator(0),])
    