from django.shortcuts import render # type: ignore
from book.models import Book

def homeview(request):
    Books=Book.objects.all()
    return render(request,'dash/homeview.html',{'Books':Books})

def view(request):
    return render(request,'dash/view.html')