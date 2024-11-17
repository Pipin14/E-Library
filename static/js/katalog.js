$(document).ready(function() {
    $(".bookmark-btn").on("click", function() {
        var button = $(this);
        var bookId = button.data("book-id");

        $.ajax({
            type: "POST",
            url: "{% url 'toggle_favorite' 0 %}".replace('0', bookId),
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}',
            },
            success: function(response) {
                if (response.success) {
                    if (response.is_favorite) {
                        button.html('<i class="fas fa-star"></i>');
                    } else {
                        button.html('<i class="far fa-star"></i>');
                    }
                } else {
                    alert("Error: " + response.error);
                }
            },
            error: function() {
                alert("An error occurred while toggling the favorite.");
            }
        });
    });
});


document.getElementById('favoriteFilter').addEventListener('change', function() {
    this.form.submit();
});

function goToFirstPage() {
    window.location.href = '?page=1';
}

function goToPrevPage() {
    let currentPage = parseInt(new URLSearchParams(window.location.search).get('page')) || 1;
    if (currentPage > 1) {
        window.location.href = `?page=${currentPage - 1}`;
    }
}

function goToNextPage() {
    let currentPage = parseInt(new URLSearchParams(window.location.search).get('page')) || 1;
    window.location.href = `?page=${currentPage + 1}`;
}

function goToLastPage() {
    let totalPages = {{ books.paginator.num_pages }};
    window.location.href = `?page=${totalPages}`;
}