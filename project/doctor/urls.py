from django.urls import path
from . import views
from .views import ShowProfilePageView
from django.contrib.auth import views as auth_views
urlpatterns = [
	path('', views.home,name = 'doctorHome'),
	path('contact/', views.contact,name = 'contact'),
	path('about/', views.about,name = 'about'),
	path('signup/', views.handleSignup,name = 'signup'),
	path('dashboard/<int:pk>',views.dashboard,name = 'dashboard'),
	path('logout', views.handelLogout, name = "handleLogout"),
	path('<int:pk>/view_profile',ShowProfilePageView.as_view() ,name = 'profile'),
	path('edit_profile/', views.profile, name='edit_profile'),
	path('login/', auth_views.LoginView.as_view(template_name='doctor/login.html'), name='login'),
	path('doctor_list/', views.doctor_list,name = 'doctor_list'),
	path('checkdisease/', views.checkdisease,name = 'checkdisease'),
	path('payment/',view.payment,name='support')
]