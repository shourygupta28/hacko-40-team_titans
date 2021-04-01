from django.db import models
from user.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator

class YrBranch(models.Model):
    year                        = models.IntegerField(default=0)
    branch                      = models.CharField(default='', max_length=50)

    def __str__(self):
        return str(self.year) + "_" + str(self.branch)

class Subject(models.Model):
    subject_code 				= models.CharField(unique=True, max_length=10)
    subject_name                = models.CharField(default='', max_length=100)
    yr_branch                   = models.ManyToManyField(YrBranch)
    visibilty                   = models.BooleanField(default=True)

    def __str__(self):
        return self.subject_code

class Resource(models.Model):
    pdf_file                    = models.FileField(default='', upload_to='resources/',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    preview                     = models.FileField(default='', upload_to='preview/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    owner                       = models.ForeignKey(User, null = True, limit_choices_to={'is_student': True}, on_delete=models.CASCADE)
    cost                        = models.IntegerField(default=0)
    buyer                       = models.ManyToManyField(User, limit_choices_to={'is_student': True}, related_name='bought_resources')
    liked_by                    = models.ManyToManyField(User, limit_choices_to={'is_student': True}, related_name='liked_resources')
    title                       = models.CharField(default=0, max_length=100)
    description                 = models.TextField(default='')
    subject                     = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.title