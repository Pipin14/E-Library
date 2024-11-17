from django.contrib.auth.decorators import login_required
from .models import Book, Favorite
from django.http import JsonResponse
from django.shortcuts import render
from katalog.models import Book


@login_required
def favorit(request):
    favorite_books = Book.objects.filter(is_favorite=True)
    return render(request, 'favorit/favorit_buku.html', {'favorite_books': favorite_books})

def favorite_books_view(request):
    favorit_books = Book.objects.filter(is_favorite=True)
    return render(request, 'favorit/favorit_buku.html', {'favorit_books': favorit_books})

# @login_required
# def favorite_books(request):
#     favorites = Favorite.objects.filter(user=request.user)
#     books = [favorite.book for favorite in favorites]
#     return render(request, 'favorit/favorit_buku.html', {'books': books})
