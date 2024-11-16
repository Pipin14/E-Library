function toggleDescription() {
    var shortDescription = document.getElementById("short-description");
    var fullDescription = document.getElementById("full-description");
    var btnText = document.getElementById("read-more-text");
    var arrowIcon = document.getElementById("arrow-icon");

    if (fullDescription.classList.contains("hidden")) {
        shortDescription.classList.add("hidden");
        fullDescription.classList.remove("hidden");
        btnText.innerHTML = "Sembunyikan";
        arrowIcon.classList.add("rotate-180");
    } else {
        shortDescription.classList.remove("hidden");
        fullDescription.classList.add("hidden");
        btnText.innerHTML = "Baca Selengkapnya";
        arrowIcon.classList.remove("rotate-180");
    }
}


document.addEventListener('DOMContentLoaded', function () {
    const bookmarkButtons = document.querySelectorAll('.bookmark-btn');

    bookmarkButtons.forEach(button => {
        button.addEventListener('click', function () {
            const bookId = this.getAttribute('data-id');
            fetch(`/favorit/toggle_favorite/${bookId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({ 'book_id': bookId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const icon = this.querySelector('svg');
                    if (data.is_favorite) {
                        icon.setAttribute('fill', 'currentColor');
                    } else {
                        icon.setAttribute('fill', 'none'); 
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    document.getElementById('deleteButtonMain').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('deleteModal').classList.remove('hidden');
    });

    document.getElementById('cancelButton').addEventListener('click', function() {
        document.getElementById('deleteModal').classList.add('hidden');
    });

    document.getElementById('confirmDeleteButton').addEventListener('click', function() {
        const bookId = document.getElementById('deleteButtonMain').getAttribute('data-id');
        window.location.href = "{% url 'delete_book' book.id %}".replace('book.id', bookId);
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const previewButton = document.getElementById('previewButton');
    const previewModal = document.getElementById('previewModal');
    const closePreviewButton = document.getElementById('closePreviewButton');
    const previousButton = document.getElementById('previousButton');
    const nextButton = document.getElementById('nextButton');
    const pdfPreview = document.getElementById('pdfPreview');

    let currentPage = 1;
    let pdfDoc = null;
    let bookPdfUrl = ''; // Variabel untuk menyimpan URL PDF

    // Menangani klik pada tombol Preview
    previewButton.addEventListener('click', function () {
        bookPdfUrl = this.getAttribute('data-pdf-url');
        console.log("Preview button clicked, URL:", bookPdfUrl);
        
        // Menambahkan query parameter timestamp untuk menghindari cache
        const timestamp = new Date().getTime(); // Mendapatkan timestamp saat ini
        const updatedPdfUrl = `${bookPdfUrl}?t=${timestamp}`; // Menambahkan parameter waktu pada URL PDF

        previewModal.classList.remove('hidden'); // Menampilkan modal
        currentPage = 1; // Reset halaman ke 1
        loadPdfPage(updatedPdfUrl, currentPage); // Menampilkan halaman pertama dengan file PDF yang terbaru
    });

    // Menangani klik pada tombol Previous
    previousButton.addEventListener('click', function () {
        if (currentPage > 1) {
            currentPage--;
            loadPdfPage(bookPdfUrl, currentPage);
        }
    });

    // Menangani klik pada tombol Next
    nextButton.addEventListener('click', function () {
        if (currentPage < pdfDoc.numPages) {
            currentPage++;
            loadPdfPage(bookPdfUrl, currentPage);
        }
    });

    // Menangani klik pada tombol Close (untuk menutup modal)
    closePreviewButton.addEventListener('click', function () {
        previewModal.classList.add('hidden'); // Menyembunyikan modal
    });

    // Fungsi untuk memuat halaman PDF
    function loadPdfPage(bookPdfUrl, pageNumber) {
        // Pastikan dokumen PDF di-reload setiap kali file PDF berubah
        pdfjsLib.getDocument(bookPdfUrl).promise.then(function (pdfDoc_) {
            pdfDoc = pdfDoc_; // Menyimpan dokumen PDF yang dimuat
            renderPage(pageNumber); // Merender halaman yang diminta
        }).catch(function (error) {
            console.error('Error loading PDF: ', error);
        });
    }

    // Fungsi untuk merender halaman PDF ke canvas
    function renderPage(pageNumber) {
        pdfDoc.getPage(pageNumber).then(function (page) {
            const scale = 1.5; // Menyesuaikan skala rendering
            const viewport = page.getViewport({ scale: scale });
            const context = pdfPreview.getContext('2d');
            pdfPreview.height = viewport.height;
            pdfPreview.width = viewport.width;

            // Merender halaman PDF pada canvas
            page.render({
                canvasContext: context,
                viewport: viewport
            });

            // Memperbarui status tombol navigasi
            updateNavigationButtons(pageNumber);
        });
    }

    // Fungsi untuk memperbarui status tombol navigasi
    function updateNavigationButtons(pageNumber) {
        previousButton.disabled = (pageNumber <= 1); // Tombol Previous dinonaktifkan jika di halaman pertama
        nextButton.disabled = (pageNumber >= pdfDoc.numPages); // Tombol Next dinonaktifkan jika di halaman terakhir
    }
});
