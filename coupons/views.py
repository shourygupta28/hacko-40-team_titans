from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.db.models import Q
from TTR.app import balance

# Create your views here.
def available(request, id=None):
	user_account = request.user.account_no
	user_balance = balance(user_account)
	user = request.user
	if id:
		coupon = AvailableCoupons.objects.get(id=id)
		if user.coins <= coupon.cost:
			messages.add_message(request, messages.INFO, 'You don\'t have enough coins to buy.')
		else:
			unique_code = get_random_string(length=8)

			Purchased = PurchasedCoupons.objects.create(coupon=coupon, unique_code=unique_code, owner=user)
			user.coins = user.coins - coupon.cost
			print(user.coins)
			user.save()
	coupons = AvailableCoupons.objects.order_by('-id')
	user = request.user

	context = {
		'user_balance' : user_balance,
		'coupons' : coupons,
	}
	return render(request, 'coupons/available_coupons.html', context)

def purchased(request, id=None):
	user_account = request.user.account_no
	user_balance = balance(user_account)
	coupons = PurchasedCoupons.objects.filter(owner=request.user)
	context = {
		'user_balance' : user_balance,
		'coupons': coupons,
	}
	return render(request, 'coupons/purchased_coupons.html', context)

def issued_coupons(request, pk = None):	
	user_account = request.user.account_no
	user_balance = balance(user_account)
	# q = request.GET['q']
	coupons = PurchasedCoupons.objects.filter(coupon__company=request.user)
	# if(q):
	# 	coupons = coupon.filter(Q(unique_code__icontains=q))
	if pk:
		to_del = coupons.filter(id=pk)
		to_del.delete()

	context = {
		'user_balance' : user_balance,
		'coupons': coupons,
	}
	return render(request, 'coupons/dashboard.html', context)

def dashboard(request):
	user_account = request.user.account_no
	user_balance = balance(user_account)
	coupons = PurchasedCoupons.objects.filter(coupon__company=request.user)
	context = {
		'user_balance' : user_balance,
		'coupons': coupons,
	}
	return render(request, 'coupons/dashboard.html', context)


def add_coupon(request):
	user_account = request.user.account_no
	user_balance = balance(user_account)
	if(request.method == 'POST'):
		form = AddCoupons(request.POST)
		if form.is_valid():
			form.instance.company = request.user
			form.instance.active = True
			form.save()
			return redirect('dashboard')
	
	form = AddCoupons()
	context = {
		'user_balance' : user_balance,
		'form' : form,
	}
	return render(request, 'coupons/add_coupon.html', context)