
document.querySelectorAll('.button').forEach((button) => {
    button.onclick = function () {
        if (button.classList.contains('new-window')) {
            window.open(button.dataset.url, '_blank').focus();
        } else {
            window.open(button.dataset.url, '_self').focus();
        }
    }
});
