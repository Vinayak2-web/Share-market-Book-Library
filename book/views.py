from django.shortcuts import render, get_object_or_404
from .models import Book

def Book_details(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'book/details.html', {'book': book})
