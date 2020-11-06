from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Contact(models.Model):
	sno=models.AutoField(primary_key=True)
	name=models.CharField(max_length=250)
	email=models.CharField(max_length=250)
	content=models.CharField(max_length=300)
	
	
	def __str__(self):
		return "message from "+self.name
		
class Country(models.Model):
	country_name=models.CharField(max_length=255)
	def __str__(self):
		return self.country_name
		
class State(models.Model):
	state_name=models.CharField(max_length=255)
	def __str__(self):
		return self.state_name
		
class City(models.Model):
	city_name=models.CharField(max_length=255)
	def __str__(self):
		return self.city_name
	
class Specialization(models.Model):
	spec_name=models.CharField(max_length=255)
	def __str__(self):
		return self.spec_name

class Doctor(models.Model):
	user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
	profile_pic=models.ImageField(upload_to='images/profile', default="images/profile/default.png")
	city=models.ForeignKey(City,on_delete=models.CASCADE,null=True)
	phone=PhoneNumberField(null=True)
	Address=models.TextField(default="None")
	country=models.ForeignKey(Country,on_delete=models.CASCADE,null=True)
	state=models.ForeignKey(State,on_delete=models.CASCADE,null=True)
	specialization=models.ForeignKey(Specialization,on_delete=models.CASCADE,null=True)
	
	def __str__(self):
		return self.user.first_name + ' ' +self.user.last_name