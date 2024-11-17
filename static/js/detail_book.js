document.addEventListener("DOMContentLoaded", function () {
    // Toggle deskripsi (short description & full description)
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

    // Pastikan elemen-elemen modal delete ada
    const deleteButtonMain = document.getElementById('deleteButtonMain');
    const cancelButton = document.getElementById('cancelButton');
    const confirmDeleteButton = document.getElementById('confirmDeleteButton');
    const deleteModal = document.getElementById('deleteModal');

    if (deleteButtonMain && cancelButton && confirmDeleteButton && deleteModal) {
        deleteButtonMain.addEventListener('click', function(event) {
            event.preventDefault();
            deleteModal.classList.remove('hidden');
        });

        cancelButton.addEventListener('click', function() {
            deleteModal.classList.add('hidden');
        });

        confirmDeleteButton.addEventListener('click', function() {
            const bookId = deleteButtonMain.getAttribute('data-id');
            window.location.href = "{% url 'delete_book' book.id %}".replace('book.id', bookId);
        });
    }

    // Pastikan elemen-elemen preview ada
    const previewModal = document.getElementById("previewModal");
    const previewButton = document.getElementById("previewButton");
    const closePreviewButton = document.getElementById("closePreviewButton");
    const previousButton = document.getElementById("previousButton");
    const nextButton = document.getElementById("nextButton");
    const pdfPreview = document.getElementById("pdfPreview");

    if (
        !previewModal ||
        !previewButton ||
        !closePreviewButton ||
        !previousButton ||
        !nextButton ||
        !pdfPreview
    ) {
        console.error("One or more required elements are not found in the DOM.");
        return; // Berhenti jika ada elemen yang tidak ditemukan
    }

    let pdfDoc = null;
    let currentPage = 1;

    previewButton.addEventListener("click", function () {
        const bookPdfUrl = this.getAttribute("data-pdf-url");
        if (!bookPdfUrl) {
            console.error("No PDF URL found for preview.");
            return;
        }

        previewModal.classList.remove("hidden");
        currentPage = 1;
        loadPdfPage(bookPdfUrl, currentPage);
    });

    closePreviewButton.addEventListener("click", function () {
        previewModal.classList.add("hidden");
    });

    previousButton.addEventListener("click", function () {
        if (currentPage > 1) {
            currentPage--;
            renderPage(currentPage);
        }
    });

    nextButton.addEventListener("click", function () {
        if (currentPage < pdfDoc.numPages) {
            currentPage++;
            renderPage(currentPage);
        }
    });

    function loadPdfPage(bookPdfUrl, pageNumber) {
        pdfjsLib
            .getDocument(bookPdfUrl)
            .promise.then(function (loadedPdfDoc) {
                pdfDoc = loadedPdfDoc;
                renderPage(pageNumber);
            })
            .catch(function (error) {
                console.error("Error loading PDF:", error);
            });
    }

    function renderPage(pageNumber) {
        pdfDoc
            .getPage(pageNumber)
            .then(function (page) {
                const scale = 1.5;
                const viewport = page.getViewport({ scale: scale });
                const context = pdfPreview.getContext("2d");
                pdfPreview.width = viewport.width;
                pdfPreview.height = viewport.height;

                page
                    .render({
                        canvasContext: context,
                        viewport: viewport,
                    })
                    .promise.then(() => {
                        updateNavigationButtons(pageNumber);
                    });
            })
            .catch(function (error) {
                console.error("Error rendering page:", error);
            });
    }

    function updateNavigationButtons(pageNumber) {
        previousButton.disabled = pageNumber <= 1;
        nextButton.disabled = pageNumber >= pdfDoc.numPages;
    }

    // Event listener untuk toggle description jika ada tombolnya
    const readMoreButton = document.getElementById('read-more');
    if (readMoreButton) {
        readMoreButton.addEventListener('click', toggleDescription);
    }
});
