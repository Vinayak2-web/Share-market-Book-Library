from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('bookdetails/<slug>/',views.Book_details,name='details')
]
