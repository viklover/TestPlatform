
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


class ElementsManager {

    constructor() {
        this.elements_list = [];

        this.changesManager = null;
    }

    setChangesManager(manager) {
        this.changesManager = manager
    }

    addElement(elem) {
        elem.body.style.order = this.elements_list.length;
        this.elements_list.push(elem);
    }

    replace_element(elem, direction) {

        let index = this.elements_list.indexOf(elem);

        if (direction && index + 1 < this.elements_list.length) {
            swap(this.elements_list, index + 1, index)
        } else if (!direction && index - 1 >= 0) {
            swap(this.elements_list, index - 1, index)
        }

        this.reorder_elements();
        this.changesManager.check();
    }

    remove_element(elem) {

        let submit_button = document.querySelector('#remove_element').querySelector('.modal-window__button');
        submit_button.type = 'button'

        submit_button.onclick = function () {

            let element_id = parseInt(elem.body.dataset.id);

            $.ajax({
                url: 'remove_element',
                type: "POST",
                data: {
                    'element_id': element_id
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrfcookie());
                },
                success: function (data) {
                    window.location.reload();
                },
                error: function (error) {
                    console.log('ERROR');
                }
            });
        }

        open_modalwindow('#remove_element');
    }

    reorder_elements() {
        for (let i = 0; i < this.elements_list.length; ++i) {
            this.elements_list[i].body.style.order = (i + 1);
        }
    }

    getId() {
        return 'elements-ordering'
    }

    getData() {
        let data = [];
        for (let element of this.elements_list) {
            data.push(parseInt(element.body.dataset.id));
        }
        return data;
    }
}
