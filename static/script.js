
document.querySelectorAll('*[data-url]').forEach((button) => {
    button.onclick = function () {
        if (button.classList.contains('new-window')) {
            window.open(button.dataset.url, '_blank').focus();
        } else {
            window.open(button.dataset.url, '_self').focus();
        }
    }
});

document.querySelectorAll('*[data-modalwindow]').forEach((modalwindow) => {
    modalwindow.onclick = function () {
        let element = document.querySelector(modalwindow.dataset.modalwindow);
        element.classList.add('modal-window-active');
        console.log(element)

        let background = document.querySelector('.modal-background');
        background.classList.add('modal-background-active');
        background.onclick = function () {
            element.classList.remove('modal-window-active');
            background.classList.remove('modal-background-active');
        }
    }
});
