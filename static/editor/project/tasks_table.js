
class TasksTable extends EditorObject {

    constructor(exercise_id) {
        super(exercise_id);

        this.VARIANT_CLASSNAME = 'variant';

        this.variants = Array.from(this.body.querySelectorAll('.' + this.VARIANT_CLASSNAME))
        this.initDesktopListeners();
    }

    initDesktopListeners() {
        for (let variant of this.variants) {
            variant.draggable = true;
        }

        this.body.addEventListener('dragstart', (evt) => {
            if (evt.target.classList.contains(this.VARIANT_CLASSNAME)) {
                evt.target.classList.add('selected');
            }
        });

        this.body.addEventListener('dragend', (evt) => {
            if (evt.target.classList.contains(this.VARIANT_CLASSNAME)) {
                evt.target.classList.remove('selected');
            }
        });

        this.body.addEventListener('dragover', (evt) => {
            evt.preventDefault();

            if (!evt.path[1].classList.contains(this.VARIANT_CLASSNAME)) {
                return;
            }

            let activeElement = this.body.querySelector('.selected');
            let currentElement = evt.path[1];

            const isMoveable = activeElement !== currentElement &&
                currentElement.classList.contains(this.VARIANT_CLASSNAME);

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

            let tbody = this.body.querySelector('tbody')
            tbody.insertBefore(activeElement, nextElement);

            this.manager.check();
        });
    }

    getData() {
        let variants = this.body.querySelectorAll('.' + this.VARIANT_CLASSNAME);

        let data = [];
        for (let variant of variants) {
            data.push(parseInt(variant.dataset.id));
        }
        return data;
    }
}
