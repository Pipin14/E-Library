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
    let bookPdfUrl = '';

    previewButton.addEventListener('click', function () {
        bookPdfUrl = this.getAttribute('data-pdf-url');
        console.log("Preview button clicked, URL:", bookPdfUrl);
        
        const timestamp = new Date().getTime();
        const updatedPdfUrl = `${bookPdfUrl}?t=${timestamp}`;

        previewModal.classList.remove('hidden');
        currentPage = 1;
        loadPdfPage(updatedPdfUrl, currentPage);
    });

    previousButton.addEventListener('click', function () {
        if (currentPage > 1) {
            currentPage--;
            loadPdfPage(bookPdfUrl, currentPage);
        }
    });

    nextButton.addEventListener('click', function () {
        if (currentPage < pdfDoc.numPages) {
            currentPage++;
            loadPdfPage(bookPdfUrl, currentPage);
        }
    });

    closePreviewButton.addEventListener('click', function () {
        previewModal.classList.add('hidden');
    });

    function loadPdfPage(bookPdfUrl, pageNumber) {
        pdfjsLib.getDocument(bookPdfUrl).promise.then(function (pdfDoc_) {
            pdfDoc = pdfDoc_;
            renderPage(pageNumber);
        }).catch(function (error) {
            console.error('Error loading PDF: ', error);
        });
    }

    function renderPage(pageNumber) {
        pdfDoc.getPage(pageNumber).then(function (page) {
            const scale = 1.5;
            const viewport = page.getViewport({ scale: scale });
            const context = pdfPreview.getContext('2d');
            pdfPreview.height = viewport.height;
            pdfPreview.width = viewport.width;

            page.render({
                canvasContext: context,
                viewport: viewport
            });

            updateNavigationButtons(pageNumber);
        });
    }

    function updateNavigationButtons(pageNumber) {
        previousButton.disabled = (pageNumber <= 1);
        nextButton.disabled = (pageNumber >= pdfDoc.numPages);
    }
});
