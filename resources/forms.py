from .models import Resource
from django import forms

class NewResourceForm(forms.ModelForm):
	class Meta:
		model = Resource
		fields = ['title', 'description', 'cost', 'subject', 'pdf_file']

class UpdateResourceForm(forms.ModelForm):
	class Meta:
		model = Resource
		fields = ['title', 'description', 'cost']