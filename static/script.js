
let open_modalwindow = function (modalwindow_id) {
    let element = document.querySelector(modalwindow_id);
    element.classList.add('modal-window-active');

    let background = document.querySelector('.modal-background');
    background.classList.add('modal-background-active');
    background.onclick = function () {
        element.classList.remove('modal-window-active');
        background.classList.remove('modal-background-active');
    }
}

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

function checkRectOverlap(elem1, elem2) {
    const rect1 = [
        [elem1.getBoundingClientRect().x, elem1.getBoundingClientRect().y],
        [elem1.getBoundingClientRect().right, elem1.getBoundingClientRect().bottom]
    ];

    const rect2 = [
        [elem2.getBoundingClientRect().x, elem2.getBoundingClientRect().y],
        [elem2.getBoundingClientRect().right, elem2.getBoundingClientRect().bottom]
    ]

    if ((rect1[0][0] < rect2[0][0] && rect2[0][0] < rect1[1][0])
        || (rect1[0][0] < rect2[1][0] && rect2[1][0] < rect1[1][0])
        || (rect2[0][0] < rect1[0][0] && rect1[1][0] < rect2[1][0])) {
        if ((rect1[0][1] < rect2[0][1] && rect2[0][1] < rect1[1][1])
            || (rect1[0][1] < rect2[1][1] && rect2[1][1] < rect1[1][1])
            || (rect2[0][1] < rect1[0][1] && rect1[1][1] < rect2[1][1])) {
            return true;
        }
    }
    return false;
}

const getNextElement = (cursorPosition, currentElement) => {
    const currentElementCoord = currentElement.getBoundingClientRect();
    const currentElementCenter = currentElementCoord.y + currentElementCoord.height / 2;

    return (cursorPosition < currentElementCenter) ?
        currentElement :
        currentElement.nextElementSibling;
};

const compareObjects = (a, b) => {
 if (a === b) return true;

 if (typeof a != 'object' || typeof b != 'object' || a == null || b == null) return false;

 let keysA = Object.keys(a), keysB = Object.keys(b);

 if (keysA.length != keysB.length) return false;

 for (let key of keysA) {
   if (!keysB.includes(key)) return false;

   if (typeof a[key] === 'function' || typeof b[key] === 'function') {
     if (a[key].toString() != b[key].toString()) return false;
   } else {
     if (!compareObjects(a[key], b[key])) return false;
   }
 }

 return true;
}

function combineObjects(e1, e2) {
  return Object.assign({}, e1, e2);
}

var csrfcookie = function() {
    var cookieValue = null,
        name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

let swap = function (list, a, b) {
    let temp = list[b];
    list[b] = list[a];
    list[a] = temp;
}

const sort_by = (field, reverse, primer) => {

  const key = primer ?
    function(x) {
      return primer(x[field])
    } :
    function(x) {
      return x[field]
    };

  reverse = !reverse ? 1 : -1;

  return function(a, b) {
    return a = key(a), b = key(b), reverse * ((a > b) - (b > a));
  }
}

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min; //Максимум не включается, минимум включается
}