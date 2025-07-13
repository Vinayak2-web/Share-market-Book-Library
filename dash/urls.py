from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('',views.view,name='view'),
    
    path('home/',views.homeview,name='homeview'),
    
    
]
