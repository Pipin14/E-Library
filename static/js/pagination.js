document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1;
    const totalPages = 5;

    const pageStatus = document.getElementById('pageStatus');
    const firstPageButton = document.getElementById('firstPage');
    const prevPageButton = document.getElementById('prevPage');
    const nextPageButton = document.getElementById('nextPage');
    const lastPageButton = document.getElementById('lastPage');

    function updatePagination() {
        pageStatus.textContent = `Page ${currentPage} of ${totalPages}`;
        firstPageButton.disabled = currentPage === 1;
        prevPageButton.disabled = currentPage === 1;
        nextPageButton.disabled = currentPage === totalPages;
        lastPageButton.disabled = currentPage === totalPages;
    }

    firstPageButton.addEventListener('click', function () {
        currentPage = 1;
        updatePagination();
    });

    prevPageButton.addEventListener('click', function () {
        if (currentPage > 1) {
            currentPage--;
            updatePagination();
        }
    });

    nextPageButton.addEventListener('click', function () {
        if (currentPage < totalPages) {
            currentPage++;
            updatePagination();
        }
    });

    lastPageButton.addEventListener('click', function () {
        currentPage = totalPages;
        updatePagination();
    });

    updatePagination();
});