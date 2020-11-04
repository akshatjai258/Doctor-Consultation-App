from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth  import authenticate,  login, logout
from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Contact,Doctor
from .forms import UserRegisterForm,UserUpdateForm,DoctorUpdateForm
from django.contrib.auth.decorators import login_required
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
  if request.method == 'POST':
      form = UserRegisterForm(request.POST)
      if form.is_valid():
          form.save()
          username = form.cleaned_data.get('username')
          messages.success(request, f'Account created for {username}!')
          return redirect('doctorHome')
  else:
      form = UserRegisterForm()
  return render(request, 'doctor/register.html', {'form': form})
    
  
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
		
@login_required
def profile(request):
  if request.method == 'POST':
      u_form = UserUpdateForm(request.POST, instance=request.user)
      d_form = DoctorUpdateForm(request.POST,request.FILES,instance=request.user.doctor)
      if u_form.is_valid() and d_form.is_valid():
          u_form.save()
          d_form.save()
          messages.success(request, f'Your account has been updated!')
          return redirect("edit_profile")

  else:
      u_form = UserUpdateForm(instance=request.user)
      d_form = DoctorUpdateForm(instance=request.user.doctor)

  context = {
      'u_form': u_form,
      'd_form': d_form
  }

  return render(request, 'doctor/editprofile.html', context)



def doctor_list(request):
    doctors=Doctor.objects.all()
    context={'doctors':doctors}
    return render(request,'doctor/doctor_list.html',context)