let burger = document.getElementById('burger');
let burger_add = document.getElementById('burger_1');
let Avatar_click = document.getElementById('current-user_avatar');
let settings = document.getElementById('settings');

burger.onclick = function () {
 burger_add.classList.toggle('block_1');
}

Avatar_click.onclick = function () {
 settings.classList.toggle('block_1');
}