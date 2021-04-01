from django.shortcuts import render, redirect
from .models import *
from user.models import User
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
# from Blockchainbackend.block import write_block, check_integrity
from TTR.app import balance


@login_required
def feeds_home(request):
	user_account = request.user.account_no
	user_balance = balance(user_account)
	if(request.method == 'POST'):
		form = AnswerForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.author = request.user
			form.save()
	
	form = AnswerForm()
	feeds   = Feed.objects.all()
	context = {
		'user_balance' : user_balance,
		'form' : form,
		'feeds'	 : feeds,
	}
	return render(request, 'home/all_feeds.html', context)

@login_required
def post_feed(request):
	user_account = request.user.account_no
	user_balance = balance(user_account)
	if(request.method == 'POST'):
		form = AnswerForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.author = request.user
			form.save()
			return redirect('feeds')
	
	form = AnswerForm()
	context = {
		'user_balance' : user_balance,
		'form' : form,
	}
	return render(request, 'home/post_feed.html', context)

@login_required
def delete_feed(request, pk):
	user_account = request.user.account_no
	user_balance = balance(user_account)
	feed = Feed.objects.get(id=pk)
	if(request.user == feed.author):
		feed.delete()
	else:
		messages.add_message(request, messages.INFO, 'You are not authorized to delete this feed.')

	return redirect('feeds')

@login_required
def my_post(request):
	user_account = request.user.account_no
	user_balance = balance(user_account)
	if(request.method == 'POST'):
		form = AnswerForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.author = request.user
			form.instance.date = datetime.date.today()
			form.save()
	
	form = AnswerForm()
	feeds   = Feed.objects.filter(author=request.user)
	context = {
		'user_balance' : user_balance,
		'form' : form,
		'feeds'	 : feeds,
	}
	return render(request, 'home/my_feeds.html', context)

@login_required
def update_feed(request, id=None):
	user_account = request.user.account_no
	user_balance = balance(user_account)
	feed = Feed.objects.get(id=id)
	if request.method == 'POST':
		if(request.user == feed.author):
			form = UpdateFeedForm(request.POST, request.FILES, instance=feed)
			if form.is_valid():
				form.save()
				return redirect('feeds')
		else:
			messages.add_message(request, messages.INFO, 'You are not authorized to edit this feed.')
	form = UpdateFeedForm(instance=feed)
	context = {
		'user_balance' : user_balance,
		'form' : form,
	}
	return render(request, 'home/update_feed.html', context)

@login_required
def feed_details(request, pk):
	user_account = request.user.account_no
	user_balance = balance(user_account)
	feed = Feed.objects.get(id = pk)
	comment = Comments.objects.filter(feed=feed).order_by('id')
	
	if(request.method == 'POST'):
		form = AddComment(request.POST)
		if form.is_valid():
			form.instance.by_user = request.user
			form.instance.feed = feed
			form.instance.date = datetime.date.today()
			form.save()
	form = AddComment()
	context = {
		'user_balance' : user_balance,
		'feed' : feed,
		'comment' : comment,
		'form' : form,
	}
	return render(request, 'home/feed_detail.html', context)

@login_required
def delete_comment(request, pk):
	comment = Comments.objects.get(id=pk)
	feed = Feed.objects.get(feed=comment).id
	if(comment):
		comment.delete()
	return redirect('feed_details', pk=feed)