from django.shortcuts import render
from katalog.models import Book
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required   
from .models import Favorite


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


@login_required
def toggle_favorite(request, book_id):
    # Ambil objek Book berdasarkan ID
    book = get_object_or_404(Book, id=book_id)

    # Cek apakah sudah ada entry favorit untuk buku ini dan user yang bersangkutan
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)

    # Jika sudah ada, maka hapus
    if not created:
        favorite.delete()

    # Kembali ke halaman sebelumnya
    return redirect(request.META.get('HTTP_REFERER', 'katalog'))