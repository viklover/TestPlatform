
class ChangesManager {

    constructor(button_id) {
        this.elements = [];
        this.elements_data = {};
        this.changes_exists = false;

        this.editorBarButton = document.querySelector(button_id);

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
                window.location.reload();
            },
            error: function (error) {
                console.log('ERROR');
            }
        });
    }

}
