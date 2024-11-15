from .models import Book
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookUploadForm
from django.http import HttpResponse


@login_required
def katalog(request):
    return render(request, 'katalog/katalog.html')


@login_required
def katalog_view(request):
    return render(request, 'katalog/katalog.html')


# katalog/views.py


def book_list(request):
    books = Book.objects.all()
    return render(request, 'katalog/book_list.html', {'books': books})


# Fungsi untuk meng-upload buku
@login_required
def upload_book(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Menyimpan data buku
            # Mengarahkan ke halaman katalog setelah upload sukses
            return redirect('katalog')
    else:
        form = BookUploadForm()

    return render(request, 'katalog/upload_buku.html', {'form': form})

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Book
# from django.http import HttpResponse

# @login_required
# def upload_book(request):
#     if request.method == 'POST':
#         # Ambil data dari form secara manual
#         pdf_file = request.FILES.get('pdf_file')
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         author = request.POST.get('author')
#         publication_year = request.POST.get('publication_year')
#         genre = request.POST.get('genre')

#         # Validasi
#         if not pdf_file or not title or not description or not author or not publication_year or not genre:
#             return HttpResponse("Semua field harus diisi!", status=400)

#         # Simpan data ke database
#         book = Book(
#             title=title,
#             description=description,
#             author=author,
#             publication_year=publication_year,
#             genre=genre,
#             pdf_file=pdf_file
#         )
#         book.save()

#         # Redirect ke halaman katalog setelah upload sukses
#         return redirect('katalog')

#     return render(request, 'katalog/upload_book.html')



# Halaman Favorit
@login_required
def favorit(request):
    return render(request, 'favorit/favorit.html')


def favorit(request):
    return render(request, 'favorit/favorit.html')
