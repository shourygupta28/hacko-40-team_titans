from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password=None):
        user = self.model(email=email, is_staff=True, is_superuser=True)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
	"""docstring for User"""
	username			= None
	email 				= models.EmailField(verbose_name='Email Address', unique=True)
	name 				= models.CharField(max_length=50)
	contact_no 			= PhoneNumberField(blank=False, null=False, help_text='Add country code before the contact no.')
	account_no			= models.CharField(max_length=80, validators=[MinLengthValidator(10)], default="0X00000000")
	ratings				= models.IntegerField(default=0)
	is_student			= models.BooleanField(default=False)
	is_company 			= models.BooleanField(default=False)
	USERNAME_FIELD 		= 'email' 
	user_permissions 	= None
	groups 				= None
	REQUIRED_FIELDS 	= []

	objects = CustomUserManager()

	def __str__(self):
		return self.email

class Rating(models.Model):
	rated_by			= models.ForeignKey(User, null=True, limit_choices_to={'is_student': True}, on_delete=models.CASCADE, related_name='rating')
	rating_of			= models.ForeignKey(User, null=True, limit_choices_to={'is_student': True}, on_delete=models.CASCADE, related_name='myrating')
	ratings				= models.IntegerField(default=0)
