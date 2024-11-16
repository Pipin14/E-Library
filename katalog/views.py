import os
import fitz
import spacy
import logging
from collections import Counter
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Favorite
from .forms import BookUploadForm, BookForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

logger = logging.getLogger(__name__)


import spacy
from collections import Counter

# Load model multibahasa
nlp = spacy.load("xx_ent_wiki_sm")

def analyze_text(text):
    doc = nlp(text.lower())
    
    filtered_words = [token.text for token in doc if token.is_alpha]
    
    word_counts = Counter(filtered_words)
    most_common_words = [word for word, count in word_counts.most_common(20)]
    
    return most_common_words


# Fungsi untuk ekstraksi teks dari PDF
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        logger.error(f"Error dalam ekstraksi teks: {str(e)}")
        return ""

@login_required
def katalog(request):
    books = Book.objects.all()
    return render(request, 'katalog/katalog.html', {'books': books})


@login_required
def katalog_view(request):
    query = request.GET.get('query', '')
    favorite_filter = request.GET.get('favorite', 'all')
    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(publication_year__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        )

    if favorite_filter == 'favorite':
        books = books.filter(is_favorite=True)
    elif favorite_filter == 'notFavorite':
        books = books.filter(is_favorite=False)

    paginator = Paginator(books, 8)
    page_number = request.GET.get('page', 1)
    books_page = paginator.get_page(page_number)

    return render(request, 'katalog/katalog.html', {
        'books': books_page,
        'query': query,
        'favorite': favorite_filter
    })


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
    try:
        book = get_object_or_404(Book, id=book_id)
    except Exception as e:
        logger.error(f"Error fetching book with id {book_id}: {e}")
        raise

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
    relevant_words = ["kata relevan", "kata yang relevan"]
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


@login_required
def delete_book(request, book_id):
    # Ambil objek buku berdasarkan ID
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.delete()
        messages.success(request, f'Buku "{book.title}" berhasil dihapus.')
        return redirect('katalog')

    return render(request, 'book_detail.html', {'book': book})


@login_required
def analyze_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if not book.pdf_file:
        messages.error(request, 'File PDF tidak tersedia untuk buku ini.')
        return redirect('katalog')

    pdf_path = book.pdf_file.path

    if not os.path.exists(pdf_path):
        messages.error(request, 'File PDF tidak ditemukan di server.')
        return redirect('katalog')

    pdf_text = extract_text_from_pdf(pdf_path)
    combined_text = f"{book.description} {pdf_text}"
    relevant_words = analyze_text(combined_text)

    return render(request, 'katalog/book_detail.html', {
        'book': book,
        'relevant_words': relevant_words
    })

@login_required
def preview_book(request, book_id, page_number=1):
    book = get_object_or_404(Book, id=book_id)
    pdf_path = book.pdf_file.path

    doc = fitz.open(pdf_path)
    total_pages = doc.page_count

    if page_number < 1:
        page_number = 1
    elif page_number > total_pages:
        page_number = total_pages

    page = doc.load_page(page_number - 1)
    pix = page.get_pixmap()
    img_path = f"media/preview_images/{book.id}_page_{page_number}.png"
    pix.save(img_path)

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
