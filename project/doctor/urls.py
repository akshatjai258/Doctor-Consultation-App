from django.urls import path
from . import views
from .views import ShowProfilePageView,EditProfilePageView
from django.contrib.auth import views as auth_views
urlpatterns = [
	path('', views.home,name = 'doctorHome'),
	path('contact/', views.contact,name = 'contact'),
	path('about/', views.about,name = 'about'),
	path('signup/', views.handleSignup,name = 'signup'),
	path('dashboard/<int:pk>',views.dashboard,name = 'dashboard'),
	path('logout', views.handelLogout, name = "handleLogout"),
	path('<int:pk>/view_profile',ShowProfilePageView.as_view() ,name = 'profile'),
	path('<int:pk>/edit_profile',EditProfilePageView.as_view() ,name = 'editprofile'),
	path('login/', auth_views.LoginView.as_view(template_name='doctor/login.html'), name='login'),
]