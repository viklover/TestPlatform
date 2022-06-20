
class ChangesManager {

    constructor(button) {
        this.elements = [];
        this.elements_data = {};
        this.changes_exists = false;

        this.editorBarButton = button;

        this.updates = {};
    }

    addElement(elem) {
        this.elements_data[elem.getId()] = elem.getData()
        this.elements.push(elem);
    }

    check() {
        let changes = false;
        this.updates = {};

        for (let elem of this.elements) {
            if (!compareObjects(elem.getData(), this.elements_data[elem.getId()])) {
                this.updates[elem.getId()] = elem.getData();
                changes = true;
            }
        }

        console.log(this.updates)

        // console.log(this.updates)

        this.changes_exists = changes;
        this.setButtonVisibility(changes);
    }

    refresh() {
        for (let elem of this.elements) {
            this.elements_data[elem.getId()] = elem.getData();
        }
        this.setButtonVisibility(false);
    }


    setButtonVisibility(opacity) {
        this.editorBarButton.classList.toggle('hidden', !opacity);
    }

    sendUpdates() {

        let obj = this;

        $.ajax({
            url: '',
            type: "POST",
            data: {
                'json': JSON.stringify(this.updates)
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfcookie());
            },
            success: function (data) {
                // window.location.reload();
                obj.refresh();
            },
            error: function (error) {
                console.log('ERROR');
            }
        });
    }

}
