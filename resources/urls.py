from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('resources/', all_resources, name='all-resources'),
    path('new/resource/', post_resource, name='post_resource'),
    path('like1/<int:pk>/', like_resource_1, name='like_resource_1'),
    path('dislike1/<int:pk>/', dislike_resource_1, name='dislike_resource_1'),
    path('like2/<int:pk>/', like_resource_2, name='like_resource_2'),
    path('dislike2/<int:pk>/', dislike_resource_2, name='dislike_resource_2'),
    path('like3/<int:pk>/', like_resource_3, name='like_resource_3'),
    path('dislike3/<int:pk>/', dislike_resource_3, name='dislike_resource_3'),
    path('update/resource/<int:pk>/', update_resource, name='update_resource'),
    path('delete/<int:pk>/', delete_resource, name='delete_resource'),
    path('', my_posted_resources, name='my_posted_resources'),
    path('my/bought/resources/', my_bought_resources, name='my_bought_resources'),
    # path('my/posted/resources/', my_posted_resources, name='my_posted_resources'),
    path('buy/resource/<int:pk>', buy_resource, name='buy_resource'),
    path('pdf/<int:id>', pdf, name='pdf'),
]