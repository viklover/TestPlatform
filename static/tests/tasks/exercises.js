
class Exercise {

    constructor(body) {
        if (body === undefined || body === null) {
            return;
        }
        this.exercise_id = body.dataset.id;
        this.body = body;
    }

    setManager(manager) {
        this.manager = manager;
    }

    initEventListeners() {

    }

    getId() {
        return this.exercise_id;
    }

    getData() {
        return [];
    }
}


class Chronology extends Exercise {

    constructor(body) {
        super(body)
        if (!this.body.classList.contains('variants')) {
            this.body = this.body.querySelector('.variants');
        }
        this.variants = Array.from(this.body.querySelectorAll('.variant'));
    }

    initEventListeners() {
        this.initMobileListeners()
        this.initDesktopListeners()
    }

    initMobileListeners() {

        let exercise = this;

        function addMobileListener(variant) {

            function createVariant() {
                let empty_variant = document.createElement('div');
                empty_variant.classList.add('variant');
                empty_variant.classList.add('empty');
                empty_variant.style.opacity = '0';
                empty_variant.innerHTML = variant.innerHTML;
                return empty_variant;
            }

            function getVariants(event) {
                return Array.from(event.path[1].querySelectorAll('.variant'));
            }

            variant.ontouchstart = function (event) {

                if (!event.target.classList.contains('variant')) {
                    return;
                }

                variant.classList.add('selected');
                variant.style.position = 'absolute';

                let parentElement = event.path[1]
                let variants = getVariants(event);

                function moveElement(event) {
                    let touch = event.targetTouches[0];
                    variant.style.top = (touch.pageY - (parentElement.offsetTop) - (variant.offsetHeight / 2)) + 'px';
                    variant.style.left = (touch.pageX - (parentElement.offsetLeft) - (variant.offsetWidth / 2)) + 'px';
                }
                moveElement(event);

                let spaceElement = createVariant();
                parentElement.insertBefore(spaceElement, variant);

                let hoverElement = null;

                variant.ontouchmove = function (event) {
                    event.preventDefault();

                    moveElement(event);

                    for (let item of variants) {
                        if (!item.classList.contains('hover') && checkRectOverlap(variant, item)) {
                            if (hoverElement != null) {
                                hoverElement.classList.remove('hover')
                            }
                            item.classList.add('hover');
                            hoverElement = item;
                        }
                    }
                }

                variant.ontouchend = function (event) {
                    variant.classList.remove('selected');
                    variant.style.position = 'static';

                    if (hoverElement === null) {
                        spaceElement.remove();
                        exercise.manager.check();
                        return;
                    }

                    hoverElement.classList.remove('hover');

                    parentElement.insertBefore(variant, hoverElement);
                    spaceElement.remove();

                    if (variants.indexOf(hoverElement) > variants.indexOf(variant)) {
                        parentElement.insertBefore(variant, hoverElement.nextElementSibling);
                    } else {
                        parentElement.insertBefore(variant, hoverElement);
                    }

                    exercise.manager.check();
                }
            }
        }

        for (let variant of this.variants) {
            addMobileListener(variant);
        }
    }

    initDesktopListeners() {

        let exercise = this;

        for (let variant of this.variants) {
            variant.draggable = true;
        }

        this.body.addEventListener('dragstart', (evt) => {
            if (evt.target.classList.contains('variant')) {
                evt.target.classList.add('selected');
            }
        });

        this.body.addEventListener('dragend', (evt) => {
            if (evt.target.classList.contains('variant')) {
                evt.target.classList.remove('selected');
                exercise.manager.check();
            }
        });

        this.body.addEventListener('dragover', (evt) => {
            evt.preventDefault();

            if (!evt.target.classList.contains('variant')) {
                return;
            }

            let activeElement = this.body.querySelector('.selected');
            let currentElement = evt.target;

            const isMoveable = activeElement !== currentElement &&
                currentElement.classList.contains('variant');

            if (!isMoveable) {
                return;
            }

            const nextElement = getNextElement(evt.clientY, currentElement);

            if (
                nextElement &&
                activeElement === nextElement.previousElementSibling ||
                activeElement === nextElement
            ) {
                return;
            }

            console.log(activeElement, nextElement)

            this.body.insertBefore(activeElement, nextElement);
        });
    }

    getData() {
        let variants = this.body.querySelectorAll('.variant');

        let data = [];
        for (let variant of variants) {
            data.push(parseInt(variant.dataset.id));
        }
        return data;
    }
}


class Match extends Exercise {

    constructor(body) {
        super(body);
        this.variants = Array.from(this.body.querySelectorAll('.variant'));
    }

    initEventListeners() {
        this.initMobileListeners()
        this.initDesktopListeners()
    }

    initMobileListeners() {

        let exercise = this;

        function addMobileListener(variant) {

            function createVariant() {
                let empty_variant = document.createElement('div');
                empty_variant.classList.add('variant');
                empty_variant.classList.add('empty');
                empty_variant.style.opacity = '0';
                empty_variant.innerHTML = variant.innerHTML;
                return empty_variant;
            }

            variant.ontouchstart = function (event) {
                event.preventDefault();

                // PREPARE VARIABLES FOR MOVE TOUCH FUNCTION
                let activeElement = event.target;
                activeElement.classList.add('selected');
                activeElement.style.position = 'absolute';

                let parentElement = findParentWithOneOfClasses(event, ['variants', 'cell']);

                moveElementByTouch(event, activeElement, parentElement);

                // CREATE SPACE ELEMENT
                let spaceElement = createVariant();
                parentElement.insertBefore(spaceElement, activeElement);

                // CREATE OTHER EVENT LISTENERS

                let body = findParentWithClass(event, 'match');

                let hoverElement = null;
                let hoverElements = Array.from(
                    body.querySelectorAll('.variant')
                ).concat(Array.from(body.querySelectorAll('.element')));

                if (hoverElements.indexOf(activeElement.parentElement.parentElement) !== -1) {
                    hoverElements.splice(hoverElements.indexOf(activeElement.parentElement.parentElement), 1);
                }

                if (body.querySelector('.variants').querySelectorAll('.variant').length === 0) {
                    hoverElements.push(body.querySelector('.variants-section'));
                }

                activeElement.ontouchmove = function (event) {
                    moveElementByTouch(event, activeElement, parentElement);

                    for (let item of hoverElements) {
                        if (!item.classList.contains('hover') && checkRectOverlap(activeElement, item)) {
                            if (hoverElement != null) {
                                hoverElement.classList.remove('hover')
                            }
                            item.classList.add('hover');
                            hoverElement = item;
                        }
                    }
                }

                activeElement.ontouchend = function (event) {
                    // REMOVE MOVE TOUCH
                    activeElement.classList.remove('selected');
                    activeElement.style.position = 'static';

                    spaceElement.remove();

                    if (hoverElement == null) {
                        exercise.manager.check();
                        return;
                    }

                    hoverElement.classList.remove('hover');

                    if (hoverElement.classList.contains('variants-section')) {
                        hoverElement.querySelector('.variants').append(activeElement);

                    } else if (hoverElement.classList.contains('element')) {
                        hoverElement.querySelector('.cell').append(activeElement);

                    } else if (hoverElement.classList.contains('variant')) {
                        let localParent = hoverElement.parentElement;
                        let listOfParent = Array.from(localParent.children);

                        if (listOfParent.indexOf(hoverElement) > listOfParent.indexOf(variant)) {
                            localParent.insertBefore(variant, hoverElement.nextElementSibling);
                        } else {
                            localParent.insertBefore(variant, hoverElement);
                        }
                    }

                    exercise.manager.check();
                }
            }
        }

        for (let variant of this.variants) {
            addMobileListener(variant);
        }
    }

    initDesktopListeners() {

        let exercise = this;

        for (let variant of this.variants) {
            variant.draggable = true;
        }

        this.body.addEventListener('dragstart', (evt) => {
            if (evt.target.classList.contains('variant')) {
                evt.target.classList.add('selected');
            }
        });

        this.body.addEventListener('dragend', (evt) => {
            if (evt.target.classList.contains('variant')) {
                evt.target.classList.remove('selected');
                exercise.manager.check();
            }
        });

        this.body.addEventListener('dragover', (evt) => {
            evt.preventDefault();

            let currentElement = findParentWithOneOfClasses(evt, ['variant', 'element', 'variants-section']);

            if (currentElement == null) {
                return;
            }

            let activeElement = this.body.querySelector('.selected');

            if (activeElement.classList.contains('variant')) {

                if (currentElement.classList.contains('variant')) {

                    if (!(activeElement !== currentElement)) {
                        return;
                    }

                    const nextElement = getNextElement(evt.clientY, currentElement);

                    if (
                        nextElement &&
                        activeElement === nextElement.previousElementSibling ||
                        activeElement === nextElement
                    ) {
                        return;
                    }

                    currentElement.parentElement.insertBefore(activeElement, nextElement);

                } else if (currentElement.classList.contains('element')) {
                    currentElement.querySelector('.cell').append(activeElement);
                } else if (currentElement.classList.contains('variants-section')) {
                    currentElement.querySelector('.variants').append(activeElement);
                }
            }
        });
    }

    getData() {
        let elements = this.body.querySelectorAll('.element');

        let data = {'-1': []};

        for (let element of elements) {
            let index = parseInt(element.dataset.id);
            data[index] = [];
            for (let variant of element.querySelectorAll('.variant')) {
                data[index].push(parseInt(variant.dataset.id));
            }
        }

        for (let variant of this.body.querySelector('.variants').querySelectorAll('.variant')) {
            data['-1'].push(parseInt(variant.dataset.id))
        }

        return data;
    }
}



class Statements extends Exercise {

    constructor(body) {
        super(body);
        this.variants = this.body.querySelectorAll('.variant');
    }

    initEventListeners() {

        let obj = this;

        for (let variant of this.variants) {
            variant.addEventListener('click', function (){
                variant.classList.toggle('selected');
                obj.manager.check();
            })
        }
    }

    getData() {
        let data = []
        this.variants.forEach(function (variant) {
            if (variant.classList.contains('selected')) {
                data.push(parseInt(variant.dataset.id));
            }
        })
        return data;
    }
}


class Radio extends Exercise {

    constructor(body) {
        super(body);
        this.variants = this.body.querySelectorAll('.variant');
        this.initEventListeners();
    }

    initEventListeners() {

        let obj = this;

        for (let variant of this.variants) {

            variant.addEventListener('click', function () {

                obj.body.querySelectorAll('.variant').forEach(function (i) {
                    i.classList.remove('selected');
                });

                variant.classList.toggle('selected');

                obj.manager.check();
            })
        }
    }

    getData() {

        let variant = this.body.querySelector('.selected');

        if (variant !== undefined)
            return parseInt(this.body.querySelector('.selected').dataset.id);
    }
}


class Input extends Exercise {

    constructor(body) {
        super(body);
        this.textarea = this.body.querySelector('textarea');
    }

    initEventListeners() {

        let obj = this;

        this.textarea.addEventListener(
            "input",
            function () {
              this.style.height = 'auto';
              this.style.height = (this.scrollHeight) + 'px';
              obj.manager.check();
            },
            false
        );
    }

    getData() {
        return this.textarea.value;
    }
}


class Answer extends Exercise {

    constructor(body) {
        super(body);
        this.input = this.body.querySelector('input');
    }

    initEventListeners() {

        let obj = this;

        this.input.addEventListener('input', function () {
            obj.manager.check();
        });
    }

    getData() {
        return this.input.value;
    }

}

class Images extends Exercise {

    constructor(body) {
        super(body);
    }

    initEventListeners() {

        let obj = this;

        for (let picture of this.body.querySelectorAll('.picture')) {
            picture.addEventListener('click', function () {
                picture.classList.toggle('checked');
                obj.manager.check();
            })
        }
    }

    getData() {
        let data = [];
        for (let picture of this.body.querySelectorAll('.picture')) {
            if (picture.classList.contains('checked'))
                data.push(parseInt(picture.dataset.id));
        }
        return data;
    }

}

class MatchList extends Exercise {

    constructor(body) {
        super(body);
    }

    initEventListeners() {

        let obj = this;

        for (let key of this.body.querySelectorAll('.key')) {
            let select = key.querySelector('.select-value');
            select.onchange = function () {
                obj.manager.check()
            }
        }
    }

    getData() {
        let data = {};
        for (let key of this.body.querySelectorAll('.key')) {
            let value = key.querySelector('.select-value').value;
            if (value === '') {
                value = null;
            } else {
                value = parseInt(value);
            }
            data[key.dataset.id] = value;
        }
        console.log(data);
        return data;
    }

}
