from .models import Book
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookUploadForm

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
def favorit(request):
    return render(request, 'favorit/favorit.html')


def favorit(request):
    return render(request, 'favorit/favorit.html')
