
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

class Chronology extends Exercise {

    constructor(exercise_id) {
        super(exercise_id)
        this.variantList = document.querySelector('#'+exercise_id);
        this.variants = Array.from(this.variantList.querySelectorAll('.variant'));
        this.initEventListeners();
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
                console.log(event.path);
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

        this.variantList.addEventListener('dragstart', (evt) => {
            if (evt.target.classList.contains('variant')) {
                evt.target.classList.add('selected');
            }
        });

        this.variantList.addEventListener('dragend', (evt) => {
            if (evt.target.classList.contains('variant')) {
                evt.target.classList.remove('selected');
            }
        });

        this.variantList.addEventListener('dragover', (evt) => {
            evt.preventDefault();

            if (!evt.target.classList.contains('variant')) {
                return;
            }

            let activeElement = this.variantList.querySelector('.selected');
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

            this.variantList.insertBefore(activeElement, nextElement);
        });
    }

    getData() {
        let variants = this.variantList.querySelectorAll('.variant');

        let data = [];
        for (let variant of variants) {
            data.push(parseInt(variant.dataset.id));
        }
        return data;
    }
}