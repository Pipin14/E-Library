from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookUploadForm
from django.http import JsonResponse
from .models import Book, Favorite
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
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)

    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    
    return redirect(request.META.get('HTTP_REFERER', 'katalog'))


from django.shortcuts import render, get_object_or_404
from .models import Book

def book_detail(request, book_id):
    # Ambil buku berdasarkan ID
    book = get_object_or_404(Book, id=book_id)

    # Ambil kata-kata relevan untuk analisis (sesuaikan dengan implementasi Anda)
    relevant_words = ["contoh", "kata", "relevan"]  # Anda bisa mengganti dengan logika analisis Anda

    # Kirimkan context ke template
    context = {
        'book': book,
        'relevant_words': relevant_words,
    }

    return render(request, 'katalog/book_detail.html', context)
