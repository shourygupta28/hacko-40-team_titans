from django.db import models
from user.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class AvailableCoupons(models.Model):
    company                     = models.ForeignKey(User, limit_choices_to={'is_company': True}, on_delete=models.PROTECT)
    description                 = models.TextField()
    cost                        = models.IntegerField(default=0)
    active                      = models.BooleanField(default=True)
    def __str__(self):
        return self.company.name + self.description

class PurchasedCoupons(models.Model):
    coupon                      = models.ForeignKey(AvailableCoupons, on_delete=models.CASCADE)
    unique_code                 = models.CharField(max_length=10, unique=True, default="XXXXXXXX")
    owner                       = models.ForeignKey(User, limit_choices_to={'is_student': True}, on_delete=models.CASCADE)

    def __str__(self):
        return self.unique_code