from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor


class UserRegisterForm(UserCreationForm):
	
  email = forms.EmailField()
  first_name=forms.CharField()
  last_name=forms.CharField()

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class UserUpdateForm(forms.ModelForm):
	
  email = forms.EmailField()
  first_name=forms.CharField()
  last_name=forms.CharField()	
  class Meta:
      model = User
      fields = ['username', 'email','first_name','last_name']

class DoctorUpdateForm(forms.ModelForm):
	profile_pic = forms.ImageField(widget=forms.FileInput,)
	class Meta:
		model = Doctor
		fields = ['profile_pic','city','phone','Address','country','state']