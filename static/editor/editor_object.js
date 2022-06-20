
class EditorObject {

    constructor(element_id) {
        this.manager = null;
        this.body = document.querySelector('#' + element_id);
    }


    getId() {
        return this.body.id;
    }

    setManager(manager) {
        this.manager = manager;
    }

}
