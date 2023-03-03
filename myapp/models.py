from django.db import models
from random import choices
from secrets import choice
from turtle import position
from django.db import models
from django.utils import timezone


user_type = (
	("operator", "operator"),
	("manager", "manager"),
)

# Create your models here.
class User_rgp(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	password=models.CharField(max_length=100)
	usertype=models.CharField(max_length=100,choices=user_type)
	

	def __str__(self):
		return self.fname+" "+self.lname

class Rgp_entry(models.Model):
	cpname=models.CharField(max_length=100)
	dpname=models.CharField(max_length=100)
	spname=models.CharField(max_length=100)
	desc=models.CharField(max_length=100)
	unit=models.CharField(max_length=100)
	qty=models.CharField(max_length=100)
	remarks=models.CharField(max_length=100)
	date=models.DateTimeField(default=timezone.now)
	made_on = models.DateTimeField(default=timezone.now)
	current_status = models.CharField(max_length=10, default="Entry")
	

	def __str__(self):
		return self.cpname+" "+self.dpname
	
class Nrgp_entry(models.Model):
	cpname=models.CharField(max_length=100)
	dpname=models.CharField(max_length=100)
	spname=models.CharField(max_length=100)
	desc=models.CharField(max_length=100)
	unit=models.CharField(max_length=100)
	qty=models.CharField(max_length=100)
	remarks=models.CharField(max_length=100)
	date=models.DateTimeField(default=timezone.now)
	made_on = models.DateTimeField(default=timezone.now)
	current_status = models.CharField(max_length=10, default="Entry")
	

	def __str__(self):
		return self.cpname+" "+self.dpname

