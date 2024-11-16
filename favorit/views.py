from django.shortcuts import render
from katalog.models import Book
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required   
from .models import Favorite
from django.http import HttpResponseNotFound

@login_required
def favorit_books(request):
    favorit_books = Book.objects.filter(is_favorite=True, user=request.user)
    return render(request, 'favorit/favorit.html', {'favorit_books': favorit_books})


@login_required
def favorit(request):
    favorite_books = Book.objects.filter(is_favorite=True)
    return render(request, 'favorit/favorit_buku.html', {'favorite_books': favorite_books})

@login_required
def favorite_books(request):
    favorites = Favorite.objects.filter(user=request.user)
    books = [favorite.book for favorite in favorites]
    return render(request, 'favorit/favorit_buku.html', {'books': books})


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import Book, Favorite
from django.contrib.auth.decorators import login_required

@login_required
def toggle_favorite(request, book_id):
    print("Received book_id:", book_id)
    book = get_object_or_404(Book, id=book_id) 
    try:
        book = Book.objects.get(id=book_id)
        print(f"Book title: {book.title}")
    except Book.DoesNotExist:
        print(f"No book found with id: {book_id}")
        return HttpResponseNotFound("Book not found.")

    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'katalog'))
