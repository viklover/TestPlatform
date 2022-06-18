
class Chronology extends Exercise {

    constructor(exercise_id) {
        super(exercise_id)
        if (!this.body.classList.contains('variants')) {
            this.body = this.body.querySelector('.variants');
        }
        this.variants = Array.from(this.body.querySelectorAll('.variant'));
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
                console.log('hello', event.path);
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