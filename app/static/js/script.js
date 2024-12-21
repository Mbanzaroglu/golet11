document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        // 3 saniye sonra show kaldırılıp fade ekleniyor
        setTimeout(() => {
            message.classList.remove('show');
            message.classList.add('fade');
            // 2 saniyelik transition bitince DOM’dan tamamen kaldırılıyor
            setTimeout(() => message.remove(), 2000);
        }, 3000);
    });
});
