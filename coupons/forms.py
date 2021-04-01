from .models import PurchasedCoupons, AvailableCoupons
from django import forms

class NewPurchasedCoupons(forms.ModelForm):
	class Meta:
		model = PurchasedCoupons
		fields = ['coupon', 'unique_code', 'owner']

class AddCoupons(forms.ModelForm):
	class Meta:
		model = AvailableCoupons
		fields = ['description', 'cost']