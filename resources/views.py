from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from PyPDF2 import PdfFileWriter, PdfFileReader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from TTR.app import balance

# from Blockchainbackend.block import write_block, check_integrity

# Create your views here.
@login_required
def all_resources(request):
    user_account = request.user.account_no
    user_balance = balance(user_account)
    year = request.GET.get('year') or None
    branch = request.GET.get('branch') or None
    subject = request.GET.get('subject') or None

    resources = Resource.objects.order_by('-id')

    if(subject):
        resources = resources.filter(subject=subject)
    
    if(branch):
        resources = resources.filter(subject__yr_branch__branch=branch)
    
    if(year):
        resources = resources.filter(subject__yr_branch__year=year)

    context = {
        'user_balance' : user_balance,
        'resources' : resources,
    }
    return render(request, 'resources/all_resources.html', context)

@login_required
def post_resource(request):
    user_account = request.user.account_no
    user_balance = balance(user_account)
    if request.method == "POST":
        form = NewResourceForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save()
            pages_to_keep = [0] # page numbering starts from 0
            infile = PdfFileReader(f.pdf_file, 'rb')
            output = PdfFileWriter()

            for i in pages_to_keep:
                p = infile.getPage(i)
                output.addPage(p)

            with open('media/preview/'+str(f.id)+'_preview.pdf', 'wb+') as fi:
                output.write(fi)    

            f.preview = 'preview/'+str(f.id)+'_preview.pdf'
            f.owner_id = request.user
            f.save()

            return redirect('all-resources')

    else:
        form = NewResourceForm()

    context = {
        'user_balance' : user_balance,
        'form' : form,
    }

    return render(request, 'resources/resource_form.html', context)

@login_required
def like_resource_1(request, pk):
    resource = Resource.objects.filter(id=pk, buyer=request.user)
    if(resource.first()):
        resource.first().liked_by.add(request.user)
        resource.first().save()
    else:
        messages.add_message(request, messages.INFO, 'You\'ll need to buy this course to like it.')
    return redirect('all-resources')

@login_required
def dislike_resource_1(request, pk):
    res = get_object_or_404(Resource, id=pk)
    res.liked_by.remove(request.user)
    res.save()
    return redirect('all-resources')

def like_resource_2(request, pk):
    resource = Resource.objects.filter(id=pk, buyer=request.user)
    if(resource.first()):
        resource.first().liked_by.add(request.user)
        resource.first().save()
    else:
        messages.add_message(request, messages.INFO, 'You\'ll need to buy this course to like it.')
    return redirect('my_bought_resources')

@login_required
def dislike_resource_2(request, pk):
    res = get_object_or_404(Resource, id=pk)
    res.liked_by.remove(request.user)
    res.save()
    return redirect('my_bought_resources')

def like_resource_3(request, pk):
    resource = Resource.objects.filter(id=pk, buyer=request.user)
    if(resource.first()):
        resource.first().liked_by.add(request.user)
        resource.first().save()
    else:
        messages.add_message(request, messages.INFO, 'You\'ll need to buy this course to like it.')
    return redirect('my_posted_resources')

@login_required
def dislike_resource_3(request, pk):
    res = get_object_or_404(Resource, id=pk)
    res.liked_by.remove(request.user)
    res.save()
    return redirect('my_posted_resources')

@login_required
def update_resource(request, pk):
    user_balance = request.user.account_no
    resource = Resource.objects.get(id=pk)
    if(Resource.objects.get(id=pk).owner == request.user):
        if(request.method == 'POST'):
            form = UpdateResourceForm(request.POST, instance = resource)
            if form.is_valid():
                form.save()
                return redirect('my_posted_resources')
        form = UpdateResourceForm(instance = resource)
        context = {
            'user_balance' : user_balance,
            'form' : form,
        }
    else:
        return redirect('all-resources')
    return render(request, 'resources/resource_update.html', context)

@login_required
def delete_resource(request, pk):
    resource = get_object_or_404(Resource, id=pk)
    if(request.user == resource.owner):
        if not resource.buyer.exists():
            resource.delete()
        else:
            messages.add_message(request, messages.INFO, 'The resources that have been sold cannot be deleted.')
    return redirect('my_posted_resources')

@login_required
def my_posted_resources(request):
    user_account = request.user.account_no
    user_balance = balance(user_account)
    resources = Resource.objects.filter(owner=request.user)
    context = {
        'user_balance' : user_balance,
        'resources': resources,
    } 
    return render(request, 'resources/my_posted_resources.html', context)

@login_required
def my_bought_resources(request):
    user_account = request.user.account_no
    user_balance = balance(user_account)
    resources = Resource.objects.filter(buyer=request.user)
    context = {
        'user_balance' : user_balance,
        'resources': resources,
    } 
    return render(request, 'resources/my_bought_resources.html', context)

@login_required
def buy_resource(request, pk):
    resource = Resource.objects.get(id=pk)
    if(request.user.coins >= resource.cost):
        # write_block(str(request.user), str(resource.owner), resource.cost, resource.title)
        resource.buyer.add(request.user)
        resource.save()
        v = resource.owner
        u = request.user
        u.coins -= resource.cost
        v.coins += resource.cost
        u.save()
        v.save()
        return redirect('my_bought_resources')
    else:
        messages.add_message(request, messages.INFO, 'you don\'t have enough ecoins.')

    return redirect('all-resources')

def pdf(request, id):
    user_account = request.user.account_no
    user_balance = balance(user_account)
    resource = Resource.objects.get(id = id)

    context = {
        'user_balance' : user_balance,
        'resource' : resource,
    }

    return render(request, 'resources/pdf.html', context)