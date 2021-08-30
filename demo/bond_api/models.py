from decimal import Decimal
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from user_api.models import User
# Create your models here.

my_validator = RegexValidator(r'^(\d|[a-zA-Z]){8,40}$', "The type should be be alphanumeric from 8 to 40 characters.")


class Bond(models.Model):
    id=models.AutoField(primary_key=True)
    type=models.CharField(
        max_length=40,
        validators=[my_validator]
        )
    total_sell = models.PositiveSmallIntegerField(
        validators=[ MaxValueValidator(10000),MinValueValidator(1)],
        default=1
        )
    price_total =models.DecimalField(
        decimal_places=4,
        max_digits=13,
        validators=[ MaxValueValidator(Decimal('100000000.0000')),MinValueValidator(Decimal('0.0000'))],
        default=0.0000
        )
    create_id=models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )

    buyer_id=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyer_id',
        blank=True,
        null=True)
    
    class Meta:
        verbose_name='Bond'
        verbose_name_plural="Bonds"
        ordering=['id']

    def __str__(self):
        return self.type
