from django.urls import path
from . import views
from .views import ShowProfilePageView,EditProfilePageView
urlpatterns = [
	path('', views.home,name = 'doctorHome'),
	path('contact/', views.contact,name = 'contact'),
	path('about/', views.about,name = 'about'),
	path('signup/', views.handleSignup,name = 'signup'),
	path('dashboard/<int:pk>',views.dashboard,name = 'dashboard'),

	path('login', views.handeLogin, name = "handleLogin"),
	path('logout', views.handelLogout, name = "handleLogout"),
	path('<int:pk>/view_profile',ShowProfilePageView.as_view() ,name = 'profile'),
	path('<int:pk>/edit_profile',EditProfilePageView.as_view() ,name = 'editprofile'),

]