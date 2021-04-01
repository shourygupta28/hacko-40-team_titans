from .models import *
from django import forms

class AnswerForm(forms.ModelForm):
	class Meta():
		model = Feed
		fields = ['title', 'post_type', 'description', 'image']

class UpdateFeedForm(forms.ModelForm):
	class Meta():
		model = Feed
		fields = ['description', 'image']

class AddComment(forms.ModelForm):
	class Meta():
		model = Comments
		fields = ['text']