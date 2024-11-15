
document.querySelectorAll('.bookmark-btn').forEach(button => {
    button.addEventListener('click', function () {
        const bookId = this.dataset.id;

        fetch(`/toggle_favorite/${bookId}/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const icon = this.querySelector('i');
                // Toggle the star icon
                if (data.is_favorite) {
                    icon.classList.remove('far');
                    icon.classList.add('fas');
                } else {
                    icon.classList.remove('fas');
                    icon.classList.add('far');
                }
            } else {
                alert(data.message);
            }
        });
    });
});
