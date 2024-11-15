from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookUploadForm
from django.http import JsonResponse
from .models import Book, Favorite
from .forms import BookForm
from django.contrib import messages
from katalog.utils import analyze_text

import logging

logger = logging.getLogger(__name__)


@login_required
def katalog(request):
    books = Book.objects.all()
    return render(request, 'katalog/katalog.html', {'books': books})


@login_required
def katalog_view(request):
    books = Book.objects.all()
    return render(request, 'katalog/katalog.html', {'books': books})

@login_required
def book_list(request):
    books = Book.objects.all()
    print(books)
    return render(request, 'katalog/book_list.html', {'books': books})


@login_required
def upload_book(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('katalog')
            except Exception:
                form.add_error(
                    None, "Terjadi kesalahan saat menyimpan buku. Silakan coba lagi.")
    else:
        form = BookUploadForm()

    return render(request, 'katalog/upload_buku.html', {'form': form})

@login_required
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)

    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    
    return redirect(request.META.get('HTTP_REFERER', 'katalog'))

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    relevant_words = ["contoh", "kata", "relevan"]  
    context = {
        'book': book,
        'relevant_words': relevant_words,
    }

    return render(request, 'katalog/book_detail.html', context)

from django.contrib import messages

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Buku "{book.title}" berhasil diupdate.')
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'katalog/edit_book.html', {'form': form, 'book': book})


def delete_book(request, book_id):
    # Ambil objek buku berdasarkan ID
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        # Hapus buku jika request POST
        book.delete()
        # Beri pesan sukses
        messages.success(request, f'Buku "{book.title}" berhasil dihapus.')
        # Redirect ke halaman katalog setelah penghapusan
        return redirect('katalog')
    
    # Jika bukan POST, tampilkan halaman detail buku untuk konfirmasi
    return render(request, 'book_detail.html', {'book': book})


@login_required
def analyze_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    relevant_words = analyze_text(book.description)  # Fungsi untuk analisis teks
    
    return render(request, 'katalog/analyze_book.html', {'book': book, 'relevant_words': relevant_words})
