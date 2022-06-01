

let left_arrow = document.querySelector('.arrow-left');
let right_arrow = document.querySelector('.arrow-right');

let current_view = -2;
let tasks_list = document.querySelector('.dragscroll')

console.log(tasks_list.offsetWidth)

function scrolled(scrollBar) {
    console.log(scrollBar.offsetWidth, scrollBar.scrollLeft, scrollBar.scrollWidth)
    if (scrollBar.offsetWidth === scrollBar.scrollWidth) {
        return 2;
    }
    if (scrollBar.scrollLeft < 2)
        return 0;
    if (scrollBar.scrollWidth - scrollBar.offsetWidth < Math.round(scrollBar.scrollLeft) + 5)
        return 1;
    return -1;
}

function updateScrollArrows() {
    let scroll_status = scrolled(tasks_list);

    if (current_view === scroll_status) {
        return;
    }

    switch (scroll_status) {
        case 0:
            left_arrow.classList.add('hidden');
            right_arrow.classList.remove('hidden');
            // left_arrow.classList.toggle('hidden', true);
            // right_arrow.classList.toggle('hidden', false);
            break;
        case 1:
            left_arrow.classList.remove('hidden');
            right_arrow.classList.add('hidden');
            break;
        case 2:
            left_arrow.classList.add('hidden');
            right_arrow.classList.add('hidden');
            break;
        default:
            left_arrow.classList.remove('hidden');
            right_arrow.classList.remove('hidden');
    }

    current_view = scroll_status;
}

tasks_list.addEventListener('scroll', updateScrollArrows)
updateScrollArrows()

window.addEventListener("resize", updateScrollArrows, false);