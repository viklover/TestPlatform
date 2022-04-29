
class Match extends Exercise {

    constructor(exercise_id) {
        super(exercise_id);
        this.variants = Array.from(this.body.querySelectorAll('.variant'));
        this.initEventListeners()
    }

    initEventListeners() {
        this.initMobileListeners()
        this.initDesktopListeners()
    }

    initMobileListeners() {

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

                    if (hoverElement == null) return;

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
                }
            }
        }

        for (let variant of this.variants) {
            addMobileListener(variant);
        }
    }

    initDesktopListeners() {

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

        let data = {};

        for (let element of elements) {
            let index = parseInt(element.dataset.id);
            data[index] = [];
            for (let variant of element.querySelectorAll('.variant')) {
                data[index].push(parseInt(variant.dataset.id));
            }
        }
        return data;
    }
}
