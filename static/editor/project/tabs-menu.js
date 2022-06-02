
let tab_buttons = document.querySelectorAll('.tab-button');
let tabs = document.querySelectorAll('.tab');

let addListenerToTabButton = function (button) {
    button.onclick = function () {
        if (!button.classList.contains('active')) {
            for (let button of tab_buttons) {
                button.classList.remove('active')
            }
            for (let tab of tabs) {
                tab.classList.add('hidden');
            }
            button.classList.add('active');
            document.querySelector('.'+button.dataset.content).classList.remove('hidden')
        }
    }
}

for (let button of tab_buttons) {
    addListenerToTabButton(button);
}
