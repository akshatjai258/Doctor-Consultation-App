from django.urls import path
from . import views
from .views import ShowProfilePageView
from django.contrib.auth import views as auth_views
urlpatterns = [
	path('', views.home,name = 'doctorHome'),
	path('contact/', views.contact,name = 'contact'),
	path('about/', views.about,name = 'about'),
	path('signup/', views.handleSignup,name = 'signup'),
	path('logout', views.handelLogout, name = "handleLogout"),
	path('<int:pk>/view_profile',ShowProfilePageView.as_view() ,name = 'profile'),
	path('edit_profile/', views.profile, name='edit_profile'),
	path('login/', auth_views.LoginView.as_view(template_name='doctor/login.html'), name='login'),
	path('doctor_list/', views.doctor_list,name = 'doctor_list'),
	path('checkdisease/', views.checkdisease,name = 'checkdisease'),
	path('payment/',views.payment,name='payment'),
	path('reset_password/',auth_views.PasswordResetView.as_view(template_name="doctor/password_reset.html"),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="doctor/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="doctor/password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="doctor/password_reset_done.html"), name="password_reset_complete"),
]




'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''