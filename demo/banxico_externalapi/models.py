from decimal import Decimal
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Banxico(models.Model):
    id=models.AutoField(primary_key=True)
    last_date=models.DateField()
    dollar_price=models.DecimalField(
        max_digits=8,
        decimal_places=4,
        default=0.0000,
        validators=[ MinValueValidator(Decimal('0.0000'))],
        )
    
    class Meta:
        verbose_name='banxico'
        verbose_name_plural="banxico"
        ordering=['last_date']

    def __str__(self):
        return self.type
