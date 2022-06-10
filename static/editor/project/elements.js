
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

        this.save_button = this.body.querySelector('.button-save-changes');
        this.changesManager = new ChangesManager(this.save_button);

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
                    'title': title,
                    'only_title': true
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

    save_button_show() {
        this.save_button.classList.toggle('hidden', false);
    }

    save_button_hide() {
        this.save_button.classList.toggle('hidden', true);
    }
}

// CHRONOLOGY

class ChronologyVariant {

    constructor(body) {
        console.log(body)
        if (body !== null && body !== undefined) {
            this.body = body;
            this.arrow_up = this.body.querySelector('.arrow-up');
            this.arrow_down = this.body.querySelector('.arrow-down');
            this.input = this.body.querySelector('input[type="text"]');
            this.button_remove = this.body.querySelector('.button-remove-variant');
            this.existing_obj = this.body.dataset.id !== undefined && this.body.dataset.id !== null;

            if (!(this.existing_obj)) {
                this.test_id = getRandomInt(100000, 999999);
            }
        } else {
            this.existing_obj = false;
        }
        this.exercise = null;
    }

    init(obj) {
        let obj_class = this;
        let exercise = obj;

        this.exercise = obj;

        console.log(exercise)

        this.input.onchange = function (e) {
            console.log(exercise)
            exercise.check(obj_class);
        };

        this.arrow_up.onclick = function () {
            exercise.replace_variant(obj_class, false);
        }

        this.arrow_down.onclick = function () {
            exercise.replace_variant(obj_class, true);
        }

        this.button_remove.onclick = function () {
            exercise.variants_list.removeChild(obj_class.body)
            exercise.remove_variant(obj_class);
        };
    }

    initDOM() {
        let variant = document.createElement('div');
        variant.innerHTML = `
            <div class="button button-remove-secondary button-remove-variant"></div>
            <input value="Новый элемент хронологии" type="text">
            <div class="arrows">
                <div class="arrow arrow-up"></div>
                <div class="arrow arrow-down"></div>
            </div>
        `
        variant.classList.add('variant');
        return new ChronologyVariant(variant);
    }

    getData() {
        let data = {};
        if (this.body.dataset.id !== undefined && this.body.dataset.id !== null) {
            data['id'] = parseInt(this.body.dataset.id);
        } else {
            data['test_id'] = this.test_id
        }
        data['content'] = this.input.value;
        data['order'] = parseInt(this.body.style.order);
        return data;
    }

}

class ChronologyExercise extends Exercise {

    constructor(elem) {
        super(elem);
        this.variants = [];
        this.removed_variants = [];
        this.variants_list = this.body.querySelector('.variants');
        this.add_variant_button = this.body.querySelector('.button-add-variant');

        this.description_title = this.body.querySelector('.description');

        for (let element of this.body.querySelectorAll('.variant')) {
            let variant = new ChronologyVariant(element);
            this.variants.push(variant);
        }
    }

    initEventListeners() {

        this.changesManager.addElement(this);

        let obj_class = this;
        let variants = this.variants;
        let variants_list = this.variants_list;
        let add_variant_button = this.add_variant_button;

        let save_button = this.save_button;

        for (let variant of variants) {
            variant.init(obj_class);
        }
        this.reorder_variants();

        add_variant_button.onclick = function () {
            let variant = new ChronologyVariant().initDOM();
            variants.push(variant);
            variant.init(obj_class);
            variants_list.appendChild(variant.body);
            obj_class.reorder_variants();

            obj_class.check();
        };

        save_button.onclick = function () {

            console.log('SEND UPDATES', {
                'element_id': parseInt(obj_class.body.dataset.id),
                'variants' : obj_class.getData(),
                'removed_variants': obj_class.removed_variants
            })

            $.ajax({
                url: 'change_element',
                type: "POST",
                data: {
                    'element_id': parseInt(obj_class.body.dataset.id),
                    'variants' : JSON.stringify(obj_class.getData()),
                    'removed_variants': JSON.stringify(obj_class.removed_variants)
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrfcookie());
                },
                success: function (data) {
                    console.log(data)

                    if ('new_ids' in data) {

                        for (const [test_id, new_id] of Object.entries(data['new_ids'])) {
                            for (let variant of obj_class.variants) {
                                console.log(variant)
                                if (!variant.existing_obj && parseInt(variant.test_id) == parseInt(test_id)) {
                                    variant.body.dataset.id = new_id.toString();
                                    variant.existing_obj = true;
                                    console.log('create id for ', variant, 'with id', new_id)
                                }
                            }
                        }
                    }

                    obj_class.changesManager.refresh()
                },
                error: function (error) {
                    console.log('ERROR');
                }
            });
        }

        super.initEventListeners();
    }

    getId() {
        return this.body.dataset.id;
    }

    getData() {
        let data = [];
        for (let variant of this.variants) {
            data.push(variant.getData());
        }
        console.log(data.sort(sort_by('order', false, parseInt)))
        return data;
    }

    check() {
        this.changesManager.check();
    }

    remove_variant(elem) {

        let index = this.variants.indexOf(elem);

        if (index === -1)
            return;

        this.variants.splice(index, 1);
        this.reorder_variants();

        if ('id' in elem.getData()) {
            this.removed_variants.push(elem.getData());
        }

        this.check();
    }

    replace_variant(elem, direction) {

        console.log('before_replace', 'variants', this.variants)
        console.log(elem)

        let index = this.variants.indexOf(elem);

        console.log(index)

        if (direction && index + 1 < this.variants.length) {
            swap(this.variants, index + 1, index)
        } else if (!direction && index - 1 >= 0) {
            swap(this.variants, index - 1, index)
        }

        this.reorder_variants();
        this.check()
    }

    reorder_variants() {

        this.description_title.classList.toggle('hidden', this.variants.length !== 0);

        for (let i = 0; i < this.variants.length; ++i) {
            this.variants[i].body.style.order = (i + 1);
        }
    }
}

// MATCH

class MatchVariant {

    constructor(body) {

        if (body === null || body === undefined) {
            return;
        }

        this.body = body;
        this.input = body.querySelector('.variant-content');
        this.remove_button = body.querySelector('.button-remove-variant');

        this.column = null;

        this.existing_obj = this.body.dataset.id !== undefined && this.body.dataset.id !== null;

        if (!(this.existing_obj)) {
            this.test_id = getRandomInt(100000, 999999);
        }
    }

    init(column) {

        let obj = this;

        console.log('column', column)

        this.column = column;

        this.remove_button.onclick = function () {
            column.remove_variant(obj);
        };

        console.log(this.input)

        this.input.onchange = function () {
            console.log('change input')
            column.check();
        };
    }

    initDOM() {
        let element = document.createElement('div');
        element.innerHTML = `
            <hr class="line">
            <div class="button button-remove-secondary button-remove-variant"></div>
            <input value="Новый вариант" type="text" class="variant-content">
        `;
        element.classList.add('variant');

        return new MatchVariant(element);
    }

    getData() {
        let data = {};
        if (this.existing_obj) {
            data['id'] = parseInt(this.body.dataset.id);
        } else {
            data['test_id'] = this.test_id
        }
        data['content'] = this.input.value;
        return data;
    }

}

class MatchColumn {

    constructor(body) {

        if (body === null || body === undefined) {
            return;
        }

        this.body = body;
        this.variants = [];
        this.removed_variants = [];
        this.input = body.querySelector('.column-title');
        this.variants_list = body.querySelector('.variants');
        this.remove_button = body.querySelector('.button-remove-column');
        this.add_variant_button = body.querySelector('.button-add-variant');

        this.exercise = null;
        this.existing_obj = this.body.dataset.id !== undefined && this.body.dataset.id !== null;

        if (!(this.existing_obj)) {
            this.test_id = getRandomInt(100000, 999999);
        }

        for (let element of this.body.querySelectorAll('.variant')) {
            let variant = new MatchVariant(element);
            variant.init(this);
            this.variants.push(variant)
        }
    }

    init(exercise) {

        let obj = this;

        this.exercise = exercise;

        this.add_variant_button.onclick = function () {

            let variant = new MatchVariant().initDOM();
            obj.variants.push(variant);
            obj.variants_list.appendChild(variant.body);
            variant.init(obj);

            obj.check();
        }

        this.input.onchange = function () {
            exercise.check();
        }

        this.remove_button.onclick = function () {
            exercise.remove_column(obj);
        };

    }

    initDOM() {
        let element = document.createElement('div');
        element.innerHTML = `
            <header class="column-head">
                <div class="button button-remove-secondary button-remove-column"></div>
                <input value="Новая колонка" type="text" class="column-title">
            </header>
            <div class="variants hidden">
                <hr class="line-vertical">
            </div>
            <div class="button button-secondary-reverse button-add-variant">Добавить новый вариант</div>
        `;
        element.classList.add('column');

        return new MatchColumn(element);
    }

    remove_variant(variant) {
        this.variants_list.removeChild(variant.body);

        if ('id' in variant.getData()) {
            this.removed_variants.push(variant.getData());
        }

        this.variants.splice(this.variants.indexOf(variant), 1);

        this.check()
    }

    check() {
        this.variants_list.classList.toggle('hidden', this.variants.length === 0);
        this.exercise.check();
    }

    getData() {
        let data = {
            'variants': {
                'changes': [],
                'removed_variants': []
            },
            'content': ''
        };

        for (let variant of this.variants) {
            data['variants']['changes'].push(variant.getData());
        }

        for (let variant_data of this.removed_variants) {
            data['variants']['removed_variants'].push(variant_data);
        }

        if (this.existing_obj) {
            data['id'] = parseInt(this.body.dataset.id);
        } else {
            data['test_id'] = this.test_id
        }

        data['content'] = this.input.value;
        return data;
    }

}

class MatchExercise extends Exercise {

    constructor(elem) {
        super(elem);
        this.columns = [];
        this.removed_columns = [];
        this.columns_list = this.body.querySelector('.columns');
        this.add_column_button = this.body.querySelector('.button-add-column');

        this.description = this.body.querySelector('.description');

        for (let element of this.body.querySelectorAll('.column')) {
            let column = new MatchColumn(element);
            this.columns.push(column)
            column.init(this);
        }
    }

    initEventListeners() {

        let obj = this;

        this.changesManager.addElement(this);

        this.add_column_button.onclick = function () {
            let match = new MatchColumn().initDOM();
            obj.columns.push(match);
            match.init(obj);
            obj.columns_list.appendChild(match.body);

            obj.check();
        };

        this.save_button.onclick = function () {
            obj.save();
        };

        super.initEventListeners();
    }

    remove_column(column) {
        this.columns_list.removeChild(column.body);

        if ('id' in column.getData()) {
            this.removed_columns.push(column.getData());
        }

        this.columns.splice(this.columns.indexOf(column), 1);

        this.check()
    }

    getId() {
        return 'match-exercise';
    }

    getData() {
        let data = [];
        for (let column of this.columns) {
            data.push(column.getData());
        }
        console.log(data);
        return data;
    }

    save() {

        console.log({'columns': combineObjects(this.getData(), {'removed_columns': this.removed_columns})})

        console.log('SEND UPDATES', {
            'element_id': parseInt(this.body.dataset.id),
            'columns': {
                'changes': this.getData(),
                'removed_columns': this.removed_columns
            }
        })

        let obj = this;

        $.ajax({
            url: 'change_element',
            type: "POST",
            data: {
                'element_id': parseInt(this.body.dataset.id),
                'data': JSON.stringify({'columns': {
                    'changes': obj.getData(),
                    'removed_columns': this.removed_columns
                }})
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfcookie());
            },
            success: function (data) {

                for (const [column_test_id, new_id] of Object.entries(data['new_ids']['columns'])) {
                    for (let column of obj.columns) {
                        if (!column.existing_obj && parseInt(column.test_id) == parseInt(column_test_id)) {
                            column.body.dataset.id = new_id.toString();
                            column.existing_obj = true;
                            console.log('create id for ', column, 'with id', new_id)
                        }
                    }
                }

                for (const [variant_test_id, new_id] of Object.entries(data['new_ids']['variants'])) {
                    for (let column of obj.columns) {
                        for (let variant of column.variants) {
                            if (!variant.existing_obj && parseInt(variant.test_id) == parseInt(variant_test_id)) {
                                variant.body.dataset.id = new_id.toString();
                                variant.existing_obj = true;
                                console.log('create id for ', variant, 'with id', new_id)
                            }
                        }
                    }
                }

                obj.changesManager.refresh()
            },
            error: function (error) {
                console.log('ERROR');
            }
        });

    }

    check() {
        this.description.classList.toggle('hidden', this.columns.length !== 0)

        this.changesManager.check();
    }
}



class RadioExercise extends Exercise {

    constructor(elem) {
        super(elem);
    }

}

class StatementsExercise extends Exercise {

    constructor(elem) {
        super(elem);
    }

}

class InputExercise extends Exercise {

    constructor(elem) {
        super(elem);
    }

}

class AnswerExercise extends Exercise {

    constructor(elem) {
        super(elem);
    }

}

console.log(combineObjects({'a': 1, 'b': 2}, {'c': 3, 'b': 10}))

