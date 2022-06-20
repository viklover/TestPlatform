
class Exercise {

    constructor(exercise_id) {
        this.exercise_id = exercise_id;
        this.body = document.querySelector('#'+exercise_id);
    }

    getId() {
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