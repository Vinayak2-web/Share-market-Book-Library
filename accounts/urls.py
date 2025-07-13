from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('otp/<str:en_uname>/', views.otpview, name='otp'),
    path('identify/', views.identifyview, name='identifyview'), 
    path('resetpassword/<str:en_uname>/',views.resetpassword,name='resetpassword'),  
     
]
