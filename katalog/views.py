import fitz
import logging
from .models import Book
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookUploadForm
from .models import Book, Favorite
from .forms import BookForm
from django.contrib import messages
from katalog.utils import analyze_text
from django.db.models import Q
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)


@login_required
def katalog(request):
    books = Book.objects.all()
    return render(request, 'katalog/katalog.html', {'books': books})


@login_required
def katalog_view(request):
    query = request.GET.get('query', '')
    books = Book.objects.all()
    
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(publication_year__icontains=query)
        )

    paginator = Paginator(books, 8)
    page_number = request.GET.get('page', 1)
    books_page = paginator.get_page(page_number)

    return render(request, 'katalog/katalog.html', {'books': books_page, 'query': query})


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
    favorite, created = Favorite.objects.get_or_create(
        user=request.user, book=book)

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


@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            for field in form.changed_data:
                setattr(book, field, form.cleaned_data[field])
            book.save()
            messages.success(
                request, f'Buku "{book.title}" berhasil diupdate.')
            return redirect('book_detail', book_id=book.id)
        else:
            messages.error(
                request, 'Terjadi kesalahan saat mengupdate buku. Silakan periksa kembali.')

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
    # Fungsi untuk analisis teks
    relevant_words = analyze_text(book.description)

    return render(request, 'katalog/analyze_book.html', {'book': book, 'relevant_words': relevant_words})


@login_required
def preview_book(request, book_id, page_number=1):
    book = get_object_or_404(Book, id=book_id)
    pdf_path = book.pdf_file.path

    # Membuka PDF dengan PyMuPDF
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count

    # Pastikan page_number valid
    if page_number < 1:
        page_number = 1
    elif page_number > total_pages:
        page_number = total_pages

    # Mengonversi halaman PDF menjadi gambar
    # PyMuPDF page indexing starts from 0
    page = doc.load_page(page_number - 1)
    pix = page.get_pixmap()
    img_path = f"media/preview_images/{book.id}_page_{page_number}.png"
    pix.save(img_path)

    # Menyusun URL untuk Previous dan Next buttons
    prev_page = page_number - 1 if page_number > 1 else None
    next_page = page_number + 1 if page_number < total_pages else None

    return render(request, 'katalog/preview_book.html', {
        'book': book,
        'page_number': page_number,
        'total_pages': total_pages,
        'img_path': img_path,
        'prev_page': prev_page,
        'next_page': next_page
    })
