from django.contrib import admin
from .models import User, Rating

# Register your models here.


admin.site.register(User)
admin.site.register(Rating)