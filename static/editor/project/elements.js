
class Element {

    constructor(elem) {
        this.body = elem;
        this.manager = null;
        this.arrow_up = this.body.querySelector('.arrow-up');
        this.arrow_down = this.body.querySelector('.arrow-down');
        this.remove_button = this.body.querySelector('.button-remove-element');
    }

    initEventListeners() {
        let manager = this.manager;
        let obj = this;

        this.arrow_up.onclick = function () {
            manager.replace_element(obj, 0);
        };
        this.arrow_down.onclick = function () {
            manager.replace_element(obj, 1);
        };
        this.remove_button.onclick = function () {
            manager.remove_element(obj)
        };
    }

    setManager(manager) {
        this.manager = manager;
    }

    replace_up() {
        this.manager.replace_element(this, 0);
    }

    replace_down() {
        this.manager.replace_element(this, 1);
    }
}


class Exercise extends Element {

    constructor(elem) {
        super(elem);

        this.title_input = this.body.querySelector('.title-input');
        this.title = this.title_input.value;
        this.edit_title_form = this.body.querySelector('.edit-title');
        this.start_edit_button = this.body.querySelector('.button-edit-title');
        this.save_title = this.body.querySelector('.button-save-edited-title');
        this.exercise_title = this.body.querySelector('.exercise-title');
        this.title_input.value = this.exercise_title.innerHTML;

        if (this.title !== "") {
            this.exercise_title.classList.toggle('hidden', false);
        }
    }

    initEventListeners() {

        let save_title = this.save_title;
        let edit_title_form = this.edit_title_form;
        let start_edit_button = this.start_edit_button;
        let title_input = this.title_input;
        let exercise_title = this.exercise_title;

        let element_id = this.body.dataset.id;

        start_edit_button.onclick = function () {
            start_edit_button.classList.toggle('hidden', true);
            edit_title_form.classList.toggle('hidden', false);
            save_title.classList.toggle('hidden', false);
            exercise_title.classList.toggle('hidden', true);
        };

        save_title.onclick = function () {
            this.title = title_input.value;
            let title = this.title;

            $.ajax({
                url: 'change_element',
                type: "POST",
                data: {
                    'element_id': element_id,
                    'title': title
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrfcookie());
                },
                success: function (data) {
                    start_edit_button.classList.toggle('hidden', false);
                    if (title === "") {
                        start_edit_button.innerHTML = 'Создать заголовок';
                        exercise_title.classList.toggle('hidden', true);
                    } else {
                        start_edit_button.innerHTML = 'Изменить заголовок';
                        exercise_title.classList.toggle('hidden', false);
                    }
                    exercise_title.innerHTML = title;
                    edit_title_form.classList.toggle('hidden', true);
                    save_title.classList.toggle('hidden', true);
                },
                error: function (error) {
                    console.log('ERROR');
                }
            });
        };

        super.initEventListeners();
    }
}


class ChronologyElement extends Exercise {

    constructor(elem) {
        super(elem);
    }

}

class MatchElement extends Exercise {

    constructor(elem) {
        super(elem);
    }

}

class RadioElement extends Exercise {

    constructor(elem) {
        super(elem);
    }

}

class StatementsElement extends Exercise {

    constructor(elem) {
        super(elem);
    }

}

class InputElement extends Exercise {

    constructor(elem) {
        super(elem);
    }

}

class AnswerElement extends Exercise {

    constructor(elem) {
        super(elem);
    }

}

