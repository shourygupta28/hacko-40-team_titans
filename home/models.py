from django.db import models
from user.models import User
import datetime

class Feed(models.Model):
	post_type = (('Doubt', 'Doubt'),
				('News', 'News'),)

	author 				= models.ForeignKey(User, related_name = 'author', on_delete=models.CASCADE, null=True)
	title 				= models.CharField(max_length=50)
	post_type			= models.CharField(choices=post_type, max_length=5)
	description			= models.CharField(max_length=500)
	image 				= models.ImageField(default='feed/default.jpg', upload_to='feed/', null=True, blank=True)   
	date				= models.DateField(default=datetime.date.today(), null=True, blank=True) 

	def __str__(self):
		return self.title

class Comments(models.Model):
	by_user 			= models.ForeignKey(User, related_name= 'by_user', on_delete=models.CASCADE, null=False, blank=False)
	feed 				= models.ForeignKey(Feed, related_name= 'feed', on_delete=models.CASCADE, null=True, blank=True)
	text 				= models.CharField(max_length=200, null=False, blank=False)
	date				= models.DateField(default=datetime.date.today(), null=True, blank=True)