
class Match extends Exercise {

    constructor(exercise_id) {
        super(exercise_id);
        this.cells = this.body.querySelectorAll('.element')[2];
        this.cell1 = this.body.querySelector('.cell');
        this.variants = Array.from(this.body.querySelectorAll('.variant'));
        this.initEventListeners()
    }

    initEventListeners() {
        this.initMobileListeners()
        this.initDesktopListeners()
    }

    initMobileListeners() {

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

            if (!evt.target.classList.contains('cell')) {
                return;
            }

            let activeElement = this.body.querySelector('.selected');
            let currentElement = evt.target;

            const isMoveable = activeElement !== currentElement &&
                currentElement.classList.contains('cell');

            console.log(currentElement, isMoveable)

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

            console.log(this.cells)

            this.cells.insertBefore(activeElement, nextElement);
        });
    }
}
