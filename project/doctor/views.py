from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth  import authenticate,  login, logout
from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Contact,Doctor
# Create your views here.
def home(request):
	return render(request,'doctor/home.html')
	
def about(request):
	# return HttpResponse('hr')
	return render(request,'doctor/about.html')
	
def contact(request):
	# name=request.post['name']
	if(request.method=='POST'):
		name=request.POST['name']
		email=request.POST['email']
		content=request.POST['content']
		contact=Contact(name=name,email=email,content=content)
		contact.save()
		messages.success(request,"Your query is sent successfully !!!")
		
	return render (request,"doctor/contact.html")

def dashboard(request,pk):
	doctor=Doctor.objects.get(id=pk)
	context={'doctor':doctor}
	return render(request,'doctor/dashboard.html',context)
	

def handleSignup(request):
	if(request.method=='POST'):

		username=request.POST['name']
		email=request.POST['email']
		pass1=request.POST['pass1']
		pass2=request.POST['pass2']
		fname=request.POST['first_name']
		lname=request.POST['last_name']
		if pass1!=pass2:
			# TODO: write code...
			
			messages.error(request,"please fill form correctly")
			return redirect('doctorHome')
	
	
			
		
		myuser=User.objects.create_user(username,email,pass1)
		myuser.first_name=fname
		myuser.last_name=lname
		# myuser.city=city
		# myuser.tag=[]
		# for i in tag:
		# 	myuser.tag.insert(tag)
		myuser.save()
		messages.success(request,"Your Account is successfully created!!!")
		return redirect('doctorHome')
	
def handeLogin(request):
  if request.method=="POST":
  	loginusername=request.POST['loginusername']
  	loginpassword=request.POST['loginpassword']
  	user=authenticate(username= loginusername, password= loginpassword)
  	if user is not None:
  		login(request, user)
  		messages.success(request, "Successfully Logged In")
  		return redirect("doctorHome")
  	else:
  		messages.error(request, "Invalid credentials! Please try again")
  		return redirect("doctorHome")
  return HttpResponse("404- Not found")
  
  
def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('doctorHome')
    
    
class ShowProfilePageView(DetailView):
	model = Doctor
	template_name = 'doctor/user_profile.html'

	def get_context_data(self, *args, **kwargs):
		#users = Profile.objects.all()
		context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
		
		page_user = get_object_or_404(Doctor, id=self.kwargs['pk'])

		context["page_user"] = page_user
		return context
		
class EditProfilePageView(UpdateView):
	model=Doctor
	template_name = 'doctor/edit_profile.html'
	
	
