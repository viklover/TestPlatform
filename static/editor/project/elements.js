
class Element {

    constructor(elem) {
        this.body = elem;
        this.manager = null;
        this.arrow_up = this.body.querySelector('.arrow-up');
        this.arrow_down = this.body.querySelector('.arrow-down');
        this.remove_button = this.body.querySelector('.button-remove-element');
        this.save_button = this.body.querySelector('.button-save-changes');

        this.changesManager = new ChangesManager(this.save_button);

        this.element_id = this.body.dataset.id;
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

        this.changesManager.addElement(this);
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

    check() {
        this.changesManager.check();
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

class StaticElement extends Element {

    constructor(elem) {
        super(elem);
    }

}

// CHRONOLOGY

class ChronologyVariant {

    constructor(body) {
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


        this.input.onchange = function (e) {
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

                    if ('new_ids' in data) {

                        for (const [test_id, new_id] of Object.entries(data['new_ids'])) {
                            for (let variant of obj_class.variants) {
                                if (!variant.existing_obj && parseInt(variant.test_id) == parseInt(test_id)) {
                                    variant.body.dataset.id = new_id.toString();
                                    variant.existing_obj = true;
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
        return data;
    }

    check() {
        super.check();
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

        let index = this.variants.indexOf(elem);

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

class MatchWrongVariant {

    constructor(body) {

        if (body === null || body === undefined) {
            return;
        }

        this.body = body;
        this.input = body.querySelector('.variant-content');
        this.remove_button = body.querySelector('.button-remove-variant');

        this.existing_obj = this.body.dataset.id !== undefined && this.body.dataset.id !== null;

        if (!(this.existing_obj)) {
            this.test_id = getRandomInt(100000, 999999);
        }
    }

    init(exercise) {

        let obj = this;

        this.remove_button.onclick = function () {
            exercise.remove_wrong_variant(obj);
        };

        this.input.onchange = function () {
            exercise.check();
        };
    }

    initDOM() {
        let element = document.createElement('div');
        element.innerHTML = `
            <div class="button button-remove-secondary button-remove-variant"></div>
            <input value="Этот вариант никуда не подойдёт :(" type="text" class="variant-content">
        `;
        element.classList.add('variant');

        return new MatchWrongVariant(element);
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

        this.column = column;

        this.remove_button.onclick = function () {
            column.remove_variant(obj);
        };

        this.input.onchange = function () {
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

        this.wrong_variants = [];
        this.removed_wrong_variants = [];
        this.wrong_variants_list = this.body.querySelector('.wrong-variants');
        this.add_wrong_variant_button = this.body.querySelector('.button-add-wrong-variant');
        this.description_wrong_variants = this.body.querySelector('.description-wrong-variants');

        for (let element of this.body.querySelectorAll('.column')) {
            let column = new MatchColumn(element);
            this.columns.push(column)
            column.init(this);
        }

        for (let element of this.wrong_variants_list.querySelectorAll('.variant')) {
            let variant = new MatchWrongVariant(element);
            this.wrong_variants.push(variant)
            variant.init(this);
        }
    }

    initEventListeners() {

        let obj = this;

        this.add_column_button.onclick = function () {
            let match = new MatchColumn().initDOM();
            obj.columns.push(match);
            match.init(obj);
            obj.columns_list.appendChild(match.body);

            obj.check();
        };

        this.add_wrong_variant_button.onclick = function () {
            let variant = new MatchWrongVariant().initDOM();
            obj.wrong_variants.push(variant);
            variant.init(obj);
            obj.wrong_variants_list.appendChild(variant.body);

            obj.check();
        }

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

    remove_wrong_variant(variant) {

        this.wrong_variants_list.removeChild(variant.body);

        if ('id' in variant.getData()) {
            this.removed_wrong_variants.push(variant.getData());
        }

        this.wrong_variants.splice(this.wrong_variants.indexOf(variant), 1);

        this.check()
    }

    getId() {
        return 'match-exercise';
    }

    getColumnsData() {
        let data = [];
        for (let column of this.columns) {
            data.push(column.getData());
        }
        return data;
    }

    getWrongVariantsData() {
        let data = [];
        for (let variant of this.wrong_variants) {
            data.push(variant.getData());
        }
        return data;
    }

    getData() {
        return {
            'columns': this.getColumnsData(),
            'wrong-variants': this.getWrongVariantsData()
        }
    }

    save() {

        console.log({'columns': combineObjects(this.getColumnsData(), {'removed_columns': this.removed_columns})})

        console.log('SEND UPDATES', {
            'element_id': parseInt(this.body.dataset.id),
            'columns': {
                'changes': this.getColumnsData(),
                'removed_columns': this.removed_columns
            },
            'wrong-variants': {
                'changes': this.getWrongVariantsData(),
                'removed_variants': this.removed_wrong_variants
            }
        })

        let obj = this;

        $.ajax({
            url: 'change_element',
            type: "POST",
            data: {
                'element_id': parseInt(this.body.dataset.id),
                'data': JSON.stringify({
                    'columns': {
                        'changes': obj.getColumnsData(),
                        'removed_columns': this.removed_columns
                    },
                    'wrong-variants': {
                        'changes': obj.getWrongVariantsData(),
                        'removed_variants': this.removed_wrong_variants
                    }
                })
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

                for (const [variant_test_id, new_id] of Object.entries(data['new_ids']['wrong-variants'])) {
                    for (let variant of obj.wrong_variants) {
                        if (!variant.existing_obj && parseInt(variant.test_id) == parseInt(variant_test_id)) {
                            variant.body.dataset.id = new_id.toString();
                            variant.existing_obj = true;
                            console.log('create id for ', variant, 'with id', new_id)
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
        this.description_wrong_variants.classList.toggle('hidden', this.wrong_variants.length === 0)

        super.check();
    }
}

// RADIO

class RadioVariant {

    constructor(body) {
        if (body === null || body === undefined)
            return;

        this.body = body;
        this.input = body.querySelector('input[type="radio"]');
        this.input_content = body.querySelector('input[type="text"]');
        this.remove_button = body.querySelector('.button-remove-variant');

        this.existing_obj = this.body.dataset.id !== undefined && this.body.dataset.id !== null;

        if (!(this.existing_obj)) {
            this.test_id = getRandomInt(100000, 999999);
        }
    }

    init(exercise) {

        let obj = this;
        this.exercise = exercise;

        this.remove_button.onclick = function () {
            exercise.remove_variant(obj);
        };

        this.input.onchange = function () {
            exercise.check();
        };

        this.input_content.onchange = function () {
            exercise.check();
        }
    }

    initDOM(exercise) {
        let element = document.createElement('div');
        element.innerHTML = `
            <div class="variant">
                <div class="button button-remove-secondary button-remove-variant"></div>
                <input type="radio" name="radio${exercise.element_id}">
                <input value="Новое утверждение" type="text" class="variant-content">
            </div>
        `;
        element.classList.add('variant');

        return new RadioVariant(element);
    }

    getValue() {
        return this.input.checked;
    }

    getData() {
        let data = {};
        if (this.existing_obj) {
            data['id'] = parseInt(this.body.dataset.id);
        } else {
            data['test_id'] = this.test_id
        }
        data['content'] = this.input_content.value;
        data['value'] = this.getValue();
        return data;
    }
}

class RadioExercise extends Exercise {

    constructor(elem) {
        super(elem);
        this.variants = [];
        this.removed_variants = [];
        this.variants_list = this.body.querySelector('.variants');
        this.add_variant_button = this.body.querySelector('.button-add-variant');

        this.description = this.body.querySelector('.description');

        for (let element of this.body.querySelectorAll('.variant')) {
            let variant = new RadioVariant(element);
            this.variants.push(variant)
            variant.init(this)
        }
    }

    initEventListeners() {

        let obj = this;

        this.add_variant_button.onclick = function () {
            let variant = new RadioVariant().initDOM(obj);

            if (obj.variants.length === 0) {
                variant.input.checked = true;
            }

            obj.variants.push(variant);
            variant.init(obj);
            obj.variants_list.appendChild(variant.body);

            obj.check();
        };

        this.save_button.onclick = function () {
            obj.save();
        };

        super.initEventListeners();
    }

    remove_variant(variant) {

        this.variants_list.removeChild(variant.body);

        if ('id' in variant.getData()) {
            this.removed_variants.push(variant.getData());
        }

        this.variants.splice(this.variants.indexOf(variant), 1);

        if (variant.getValue() && this.variants.length > 0) {
            this.variants[0].input.checked = true;
        }

        this.check()
    }

    check() {

        this.variants_list.classList.toggle('hidden', this.variants.length === 0)
        this.description.classList.toggle('hidden', this.variants.length !== 0)

        super.check();
    }

    save() {

        let obj = this;

        $.ajax({
            url: 'change_element',
            type: "POST",
            data: {
                'element_id': parseInt(obj.element_id),
                'variants': JSON.stringify(obj.getData()),
                'removed_variants': JSON.stringify(obj.removed_variants)
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfcookie());
            },
            success: function (data) {

                for (const [variant_test_id, new_id] of Object.entries(data['new_ids'])) {
                    for (let variant of obj.variants) {
                        if (!variant.existing_obj && parseInt(variant.test_id) == parseInt(variant_test_id)) {
                            variant.body.dataset.id = new_id.toString();
                            variant.existing_obj = true;
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

    getId() {
        return 'radio-exercise';
    }

    getData() {
        let data = [];
        for (let variant of this.variants) {
            data.push(variant.getData());
        }
        return data;
    }
}

// STATEMENTS

class StatementsVariant {

    constructor(body) {
        if (body === null || body === undefined)
            return;

        this.body = body;
        this.input = body.querySelector('input[type="checkbox"]');
        this.input_content = body.querySelector('input[type="text"]');
        this.remove_button = body.querySelector('.button-remove-variant');

        this.existing_obj = this.body.dataset.id !== undefined && this.body.dataset.id !== null;

        if (!(this.existing_obj)) {
            this.test_id = getRandomInt(100000, 999999);
        }
    }

    init(exercise) {

        let obj = this;
        this.exercise = exercise;

        this.remove_button.onclick = function () {
            exercise.remove_variant(obj);
        };

        this.input.onchange = function () {
            exercise.check();
        };

        this.input_content.onchange = function () {
            exercise.check();
        }
    }

    initDOM(exercise) {
        let element = document.createElement('div');
        element.innerHTML = `
            <div class="variant">
                <div class="button button-remove-secondary button-remove-variant"></div>
                <input type="checkbox" name="radio${exercise.element_id}">
                <input value="Новое утверждение" type="text" class="variant-content">
            </div>
        `;
        element.classList.add('variant');

        return new StatementsVariant(element);
    }

    getValue() {
        return this.input.checked;
    }

    getData() {
        let data = {};
        if (this.existing_obj) {
            data['id'] = parseInt(this.body.dataset.id);
        } else {
            data['test_id'] = this.test_id
        }
        data['content'] = this.input_content.value;
        data['value'] = this.getValue();
        return data;
    }
}

class StatementsExercise extends Exercise {

    constructor(elem) {
        super(elem);
        this.variants = [];
        this.removed_variants = [];
        this.variants_list = this.body.querySelector('.variants');
        this.add_variant_button = this.body.querySelector('.button-add-variant');

        this.description = this.body.querySelector('.description');

        for (let element of this.body.querySelectorAll('.variant')) {
            let variant = new StatementsVariant(element);
            this.variants.push(variant)
            variant.init(this)
        }
    }

    initEventListeners() {

        let obj = this;

        this.add_variant_button.onclick = function () {
            let variant = new StatementsVariant().initDOM(obj);

            obj.variants.push(variant);
            variant.init(obj);
            obj.variants_list.appendChild(variant.body);

            obj.check();
        };

        this.save_button.onclick = function () {
            obj.save();
        };

        super.initEventListeners();
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

        this.variants_list.classList.toggle('hidden', this.variants.length === 0)
        this.description.classList.toggle('hidden', this.variants.length !== 0)

        super.check();
    }

    save() {

        let obj = this;

        $.ajax({
            url: 'change_element',
            type: "POST",
            data: {
                'element_id': parseInt(obj.element_id),
                'variants': JSON.stringify(obj.getData()),
                'removed_variants': JSON.stringify(obj.removed_variants)
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfcookie());
            },
            success: function (data) {

                for (const [variant_test_id, new_id] of Object.entries(data['new_ids'])) {
                    for (let variant of obj.variants) {
                        if (!variant.existing_obj && parseInt(variant.test_id) == parseInt(variant_test_id)) {
                            variant.body.dataset.id = new_id.toString();
                            variant.existing_obj = true;
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

    getId() {
        return 'statements-exercise';
    }

    getData() {
        let data = [];
        for (let variant of this.variants) {
            data.push(variant.getData());
        }
        return data;
    }

}

// INPUT

class InputExercise extends Exercise {

    constructor(elem) {
        super(elem);
        this.textarea = this.body.querySelector('textarea');
    }

    initEventListeners() {

        let obj = this;

        this.textarea.addEventListener(
            "input",
            function () {
              this.style.height = 'auto';
              this.style.height = (this.scrollHeight) + 'px';
              obj.check();
            },
            false
        );

        this.textarea.style.height = (this.textarea.scrollHeight) + 'px';

        this.save_button.onclick = function () {
            obj.save();
        };


        super.initEventListeners();
    }

    getId() {
        return 'input-exercise';
    }

    getData() {
        return {
            'prepared_answer': this.textarea.value
        }
    }

    save() {
        let obj = this;

        $.ajax({
            url: 'change_element',
            type: "POST",
            data: {
                'element_id': parseInt(obj.element_id),
                'prepared_answer': obj.textarea.value
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfcookie());
            },
            success: function (data) {
                obj.changesManager.refresh()
            },
            error: function (error) {
                console.log('ERROR');
            }
        });
    }
}

// ANSWER

class AnswerExercise extends Exercise {

    constructor(elem) {
        super(elem);
        this.input = this.body.querySelector('.input-content');
    }

    initEventListeners() {

        let obj = this;

        this.input.onchange = function () {
            console.log('update')
            obj.check();
        }

        this.save_button.onclick = function () {
            obj.save();
        };

        super.initEventListeners();
    }

    getId() {
        return 'answer-exercise';
    }

    getData() {
        return {
            'answer': this.input.value
        }
    }

    save() {
        let obj = this;

        $.ajax({
            url: 'change_element',
            type: "POST",
            data: {
                'element_id': parseInt(obj.element_id),
                'answer': obj.input.value
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfcookie());
            },
            success: function (data) {
                obj.changesManager.refresh()
            },
            error: function (error) {
                console.log('ERROR');
            }
        });
    }
}

// IMAGES

class ImagesPicture {

    constructor(body) {

        if (body === null || body === undefined)
            return;

        this.body = body;
        this.input = this.body.querySelector('.input-content');
        this.remove_button = body.querySelector('.button-remove-picture');

        this.img = this.body.querySelector('img');

        this.existing_obj = this.body.dataset.id !== undefined && this.body.dataset.id !== null;

        if (!(this.existing_obj)) {
            this.test_id = getRandomInt(100000, 999999);
        }
    }

    init(exercise) {

        let obj = this;
        this.exercise = exercise;

        this.remove_button.onclick = function () {
            exercise.remove_picture(obj);
        };

        this.body.onclick = function () {
            obj.body.classList.toggle('checked');
            exercise.check()
        };
    }

    setFormData(formData) {
        this.formData = formData;
    }

    initDOM(picture_url) {
        let element = document.createElement('div');
        element.innerHTML = `
            <div class="picture-borders">
                <img class="image" src="${picture_url}">
            </div>
            <div class="picture-bar">
                <div class="button button-remove-secondary button-remove-picture"></div>
            </div>
        `;
        element.classList.add('picture');

        return new ImagesPicture(element);
    }

    getData() {
        let data = {};
        if (this.existing_obj) {
            data['id'] = parseInt(this.body.dataset.id);
        } else {
            this.formData.append('checked', this.body.classList.contains('checked'))
            return this.formData;
        }
        data['image'] = this.img.src;
        data['checked'] = this.body.classList.contains('checked');
        data['element_id'] = this.exercise.element_id
        return data;
    }
}

class ImagesExercise extends Exercise {

    constructor(elem) {
        super(elem);
        this.pictures = [];
        this.removed_pictures = [];
        this.pictures_list = this.body.querySelector('.pictures');

        this.add_picture_button = this.body.querySelector('.button-add-picture');

        this.input_file = this.body.querySelector('.picture-uploader');
        this.file_uploader_form = this.body.querySelector('.file-uploader-form');

        this.description = this.body.querySelector('.description');

        for (let element of this.body.querySelectorAll('.picture')) {
            let picture = new ImagesPicture(element);
            this.pictures.push(picture)
            picture.init(this)
        }
    }

    initEventListeners() {

        let obj = this;

        this.add_picture_button.onclick = function () {
            obj.input_file.click();
        }

        this.file_uploader_form.addEventListener('submit', function (e) {
            e.preventDefault();
        });

        this.input_file.addEventListener('change', function (event) {
            const [file] = obj.input_file.files;
            let formData = new FormData(obj.file_uploader_form);

            let picture = new ImagesPicture().initDOM(URL.createObjectURL(file));
            obj.pictures.push(picture);
            picture.init(obj);
            picture.setFormData(formData);
            obj.pictures_list.appendChild(picture.body);

            obj.check();

            // for (var pair of formData.entries()) {
            //     console.log(pair[0]+ ', '+ pair[1]);
            // }
        });

        this.save_button.onclick = function () {
            obj.save();
        }

        // this.add_variant_button.onclick = function () {
        //     let variant = new StatementsVariant().initDOM(obj);
        //
        //     obj.variants.push(variant);
        //     variant.init(obj);
        //     obj.variants_list.appendChild(variant.body);
        //
        //     obj.check();
        // };

        super.initEventListeners();
    }

    remove_picture(picture) {
        this.pictures_list.removeChild(picture.body);

        if ('id' in picture.getData()) {
            this.removed_pictures.push(picture.getData());
        }

        this.pictures.splice(this.pictures.indexOf(picture), 1);

        this.check()
    }

    getId() {
        return 'images-exercise';
    }

    getData() {
        let data = [];
        for (let picture of this.pictures) {
            data.push(picture.getData());
        }
        return data;
    }

    check() {
        this.pictures_list.classList.toggle('hidden', this.pictures.length === 0);
        this.description.classList.toggle('hidden', this.pictures.length !== 0);

        super.check();
    }

    save() {

        let obj = this;

        for (let picture of this.pictures) {

            $.ajax({
                url: 'change_element',
                type: 'POST',
                data: picture.getData(),
                cache: picture.existing_obj,
                processData: picture.existing_obj,
                contentType: (picture.existing_obj ? 'application/x-www-form-urlencoded; charset=UTF-8' : false),
                error: function (xhr) {
                    alert(xhr.statusText);
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrfcookie());
                },
                success: function (res) {
                    if ('new_id' in res && !picture.existing_obj) {
                        picture.body.dataset.id = res['new_id'];
                        picture.existing_obj = true;
                    }
                }
            });
        }

        $.ajax({
            url: 'change_element',
            type: 'POST',
            data: {
                'element_id': obj.element_id,
                'removed_pictures': JSON.stringify(obj.removed_pictures)
            },
            error: function (xhr) {
                alert(xhr.statusText);
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfcookie());
            },
            success: function (res) {
                console.log(res);
            }
        });

        this.changesManager.refresh()

    }
}


// TITLE ELEMENT

class TitleElement extends StaticElement {

    constructor(elem) {
        super(elem);

        this.input = this.body.querySelector('.input-title');
    }

    initEventListeners() {

        let obj = this;

        this.input.onchange = function () {
            obj.check();
        }

        this.save_button.onclick = function () {
            obj.save();
        }

        super.initEventListeners();
    }

    remove_picture(picture) {
        this.pictures_list.removeChild(picture.body);

        if ('id' in picture.getData()) {
            this.removed_pictures.push(picture.getData());
        }

        this.pictures.splice(this.pictures.indexOf(picture), 1);

        this.check()
    }

    getId() {
        return 'title-element';
    }

    getData() {
        return {
            'title': this.input.value
        };
    }

    save() {

        let obj = this;

        $.ajax({
            url: 'change_element',
            type: 'POST',
            data: {
                'element_id': obj.element_id,
                'title': obj.input.value
            },
            error: function (xhr) {
                alert(xhr.statusText);
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfcookie());
            },
            success: function (res) {
                console.log('success');
            }
        });

        this.changesManager.refresh()
    }
}

// PICTURE ELEMENT

class PictureElement extends StaticElement {

    constructor(elem) {
        super(elem);

        this.picture = this.body.querySelector('.picture');
        this.input_file = this.body.querySelector('.picture-uploader');
        this.file_uploader_form = this.body.querySelector('.file-uploader-form');

        this.update_picture_button = this.body.querySelector('.button-update-picture')
    }

    initEventListeners() {

        let obj = this;

        this.update_picture_button.onclick = function () {
            obj.input_file.click();
        }

        this.file_uploader_form.addEventListener('submit', function (e) {
            e.preventDefault();
        });

        this.input_file.addEventListener('change', function (event) {
            const [file] = obj.input_file.files;
            obj.picture.src = URL.createObjectURL(file);
            obj.check();
        });

        this.save_button.onclick = function () {
            obj.save();
        }


        super.initEventListeners();
    }

    remove_picture(picture) {
        this.pictures_list.removeChild(picture.body);

        if ('id' in picture.getData()) {
            this.removed_pictures.push(picture.getData());
        }

        this.pictures.splice(this.pictures.indexOf(picture), 1);

        this.check()
    }

    getId() {
        return 'picture-element';
    }

    getData() {
        return {
            'picture': this.picture.src
        };
    }

    save() {

        let obj = this;

        $.ajax({
            url: 'change_element',
            type: 'POST',
            data: new FormData(obj.file_uploader_form),
            cache: false,
            processData: false,
            contentType: false,
            error: function (xhr) {
                alert(xhr.statusText);
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfcookie());
            },
            success: function (res) {
                console.log('success');
            }
        });

        this.changesManager.refresh()
    }
}

class QuoteElement extends StaticElement {

    constructor(elem) {
        super(elem);
        this.textarea = this.body.querySelector('textarea');
        this.input = this.body.querySelector('input[type="text"]');
    }

    initEventListeners() {

        let obj = this;

        this.input.onchange = function () {
            obj.check();
        }

        this.textarea.addEventListener(
            "input",
            function () {
              this.style.height = 'auto';
              this.style.height = (this.scrollHeight) + 'px';
              obj.check();
            },
            false
        );

        this.textarea.style.height = (this.textarea.scrollHeight) + 'px';

        this.save_button.onclick = function () {
            obj.save();
        };

        super.initEventListeners();
    }

    save() {
        let obj = this;

        $.ajax({
            url: 'change_element',
            type: "POST",
            data: {
                'element_id': parseInt(obj.element_id),
                'quote': obj.textarea.value,
                'author': obj.input.value
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfcookie());
            },
            success: function (data) {
                obj.changesManager.refresh()
            },
            error: function (error) {
                console.log('ERROR');
            }
        });
    }

    getId() {
        return 'quote-element';
    }

    getData() {
        console.log({'author': this.input.value, 'quote': this.textarea.value})
        return {'author': this.input.value, 'quote': this.textarea.value};
    }
}

class DocumentElement extends StaticElement {

    constructor(elem) {
        super(elem);
        this.textarea = this.body.querySelector('textarea');
        this.input = this.body.querySelector('input[type="text"]');
    }

    initEventListeners() {

        let obj = this;

        this.input.onchange = function () {
            obj.check();
        }

        this.textarea.addEventListener(
            "input",
            function () {
              this.style.height = 'auto';
              this.style.height = (this.scrollHeight) + 'px';
              obj.check();
            },
            false
        );

        this.textarea.style.height = (this.textarea.scrollHeight) + 'px';

        this.save_button.onclick = function () {
            obj.save();
        };

        super.initEventListeners();
    }

    save() {
        let obj = this;

        $.ajax({
            url: 'change_element',
            type: "POST",
            data: {
                'element_id': parseInt(obj.element_id),
                'content': obj.textarea.value,
                'name': obj.input.value
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfcookie());
            },
            success: function (data) {
                obj.changesManager.refresh()
            },
            error: function (error) {
                console.log('ERROR');
            }
        });
    }

    getId() {
        return 'document-element';
    }

    getData() {
        return {'name': this.input.value, 'content': this.textarea.value};
    }
}

class YandexMapsElement extends StaticElement {

    constructor(elem) {
        super(elem);
    }

    getId() {
        return 'maps-element';
    }

    getData() {
        return [];
    }
}