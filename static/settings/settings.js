let content_1 = document.querySelector('.content_settings_1');
let content_2 = document.querySelector('.content_settings_2');
let top_settings = document.querySelector('.top_settings');
let account_settings = document.querySelector('.account_settings');
let by_time = document.querySelector('.by_time');
content_2.style.display = 'none';

function showOption(el) {
    if (el.selectedIndex === 4) {
        by_time.style.display = 'block';
    }

    else if (el.selectedIndex === 1) {
        by_time.style.display = 'none';
    }

    else if (el.selectedIndex === 2) {
        by_time.style.display = 'none';
    }

    else if (el.selectedIndex === 3) {
        by_time.style.display = 'none';
    }
}

account_settings.onclick = function () {
    content_1.style.display = 'none';
    content_2.style.display = 'block';
    top_settings.classList.remove('top_settings');
    account_settings.classList.remove('account_settings');
    account_settings.classList.add('top_settings');
    top_settings.classList.add('account_settings');
}

top_settings.onclick = function () {
    content_1.style.display = 'block'
    content_2.style.display = 'none';
    top_settings.classList.remove('account_settings');
    account_settings.classList.remove('top_settings');
    top_settings.classList.add('top_settings');
    account_settings.classList.add('account_settings');
}