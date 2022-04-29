
class Exercise {

    constructor(exercise_id) {
        this.exercise_id = exercise_id;
        this.body = document.querySelector('#'+exercise_id);
    }

    get_id() {
        return this.exercise_id;
    }

}

function moveElementByTouch(event, object, parentElement) {
    let touch = event.targetTouches[0];
    object.style.top = (touch.pageY - (parentElement.offsetTop) - (object.offsetHeight / 2)) + 'px';
    object.style.left = (touch.pageX - (parentElement.offsetLeft) - (object.offsetWidth / 2)) + 'px';
}

const getNextElement = (cursorPosition, currentElement) => {
    const currentElementCoord = currentElement.getBoundingClientRect();
    const currentElementCenter = currentElementCoord.y + currentElementCoord.height / 2;

    return (cursorPosition < currentElementCenter) ?
        currentElement :
        currentElement.nextElementSibling;
};

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

function findParentWithOneOfClasses(event, classes) {
    for (let i = 0; i < event.path.length - 3; ++i) {
        let item = event.path[i];
        for (let classname of classes) {
            if (item.classList.contains(classname)) {
                return item;
            }
        }
    }
    return null;
}

function findParentWithClass(event, classname) {
    for (let i = 0; i < event.path.length - 3; ++i) {
        let item = event.path[i];
        if (item.classList.contains(classname)) {
            return item;
        }
    }
    return null;
}