import os
import logging
import fitz
import spacy

from PIL import Image
from collections import Counter
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Book, Favorite
from .forms import BookForm


logger = logging.getLogger(__name__)

nlp = spacy.load("xx_ent_wiki_sm")


def analyze_text(text):
    doc = nlp(text.lower())

    filtered_words = [
        token.text for token in doc if token.is_alpha and not token.is_stop]
    word_counts = Counter(filtered_words)
    most_common_words = [word for word, count in word_counts.most_common(20)]

    return most_common_words


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
def katalog(request):
    books = Book.objects.all()
    return render(request, 'katalog/katalog.html', {'books': books})


@login_required
def katalog_view(request):
    query = request.GET.get('query', '').strip()
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
    page_number = request.GET.get('page') or 1
    books_page = paginator.get_page(page_number)
    context = {
        'books': books_page,
        'query': query,
        'favorite': favorite_filter,
    }

    return render(request, 'katalog/katalog.html', context)


@login_required
def book_list(request):
    books = Book.objects.all()
    print(books)
    return render(request, 'katalog/book_list.html', {'books': books})


@login_required
def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save(commit=False)
            pdf_file = request.FILES.get('pdf_file')

            if pdf_file:
                book.pdf_file = pdf_file
                book.save()
                pdf_path = os.path.join(
                    settings.MEDIA_ROOT, book.pdf_file.name)

                try:
                    doc = fitz.open(pdf_path)
                    page = doc.load_page(0)
                    pix = page.get_pixmap()
                    img_data = pix.tobytes("png")
                    img_name = f"{book.id}_cover.png"
                    img_file = ContentFile(img_data)
                    book.cover_image.save(img_name, img_file, save=True)
                except Exception as e:
                    messages.error(
                        request, f'Terjadi kesalahan saat memproses PDF: {str(e)}')
                    book.delete()
                    return redirect('upload_book')

            messages.success(
                request, f'Buku "{book.title}" berhasil diupload.')
            return redirect('katalog')
        else:
            messages.error(
                request, 'Terjadi kesalahan saat mengupload buku. Silakan periksa kembali.')
    else:
        form = BookForm()

    return render(request, 'katalog/upload_buku.html', {'form': form})


def extract_cover_image_from_pdf(pdf_file):
    try:
        doc = fitz.open(pdf_file)
        page = doc.load_page(0)
        pix = page.get_pixmap()
        image_stream = BytesIO(pix.tobytes("png"))
        image = Image.open(image_stream)
        cover_image_name = f'books/covers/{pdf_file.name.replace(" ", "_")}_cover.png'
        cover_image_path = os.path.join(settings.MEDIA_ROOT, cover_image_name)
        image.save(cover_image_path)
        return InMemoryUploadedFile(image_stream, None, cover_image_name, 'image/png', image_stream.tell(), None)

    except Exception as e:
        print(f"Error extracting cover image: {str(e)}")
        return None


def toggle_favorite(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponseBadRequest("No Book matches the given query.")

    book.is_favorite = not book.is_favorite
    book.save()

    return redirect('katalog')


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
            book = form.save()
            pdf_file = request.FILES.get('pdf_file')
            if pdf_file:
                book.pdf_file = pdf_file
                book.save()
                pdf_path = os.path.join(
                    settings.MEDIA_ROOT, book.pdf_file.name)
                
                try:
                    doc = fitz.open(pdf_path)
                    page = doc.load_page(0)
                    pix = page.get_pixmap()
                    img_data = pix.tobytes("png")
                    img_name = f"{book.id}_cover.png"
                    img_file = ContentFile(img_data)
                    book.cover_image.save(img_name, img_file, save=True)
                except FileNotFoundError:
                    messages.error(
                        request, 'File PDF tidak ditemukan. Silakan coba lagi.')

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
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.delete()
        messages.success(request, f'Buku "{book.title}" berhasil dihapus.')
        return redirect('katalog')

    return render(request, 'book_detail.html', {'book': book})


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
    all_img_paths = []

    for i in range(total_pages):
        page = doc.load_page(i)
        pix = page.get_pixmap()
        all_img_path = f"media/preview_images/{book.id}_page_{i + 1}.png"
        pix.save(all_img_path)
        all_img_paths.append(all_img_path)
    
    prev_page = page_number - 1 if page_number > 1 else None
    next_page = page_number + 1 if page_number < total_pages else None

    return render(request, 'katalog/preview_book.html', {
        'book': book,
        'page_number': page_number,
        'total_pages': total_pages,
        'img_path': img_path,
        'all_img_paths': all_img_paths,
        'prev_page': prev_page,
        'next_page': next_page
    })
