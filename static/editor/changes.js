
class ChangesManager {

    constructor() {
        this.elements = [];
        this.elements_data = {};
        this.changes_exists = false;

        this.editorBarButton = document.querySelector('.editor-bar');

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
            console.log(elem, this.elements_data[elem.getId()])
            console.log(elem, this.elements_data[elem.getId()])
            console.log(elem.getData(), this.elements_data[elem.getId()])
            if (!compareObjects(elem.getData(), this.elements_data[elem.getId()])) {
                this.updates[elem.getId()] = elem.getData();
                changes = true;
            }
        }

        console.log(this.updates)

        this.changes_exists = changes;
        this.setButtonVisibility(changes);
    }

    setButtonVisibility(opacity) {
        this.editorBarButton.classList.toggle('hidden', !opacity);
    }

    sendUpdates() {

        console.log('HELLO WORLD', this.updates)

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
                console.log('SUCCESS');
            },
            error: function (error) {
                console.log('ERROR');
            }
        });

        // console.log(csrfcookie())
        // let request = new XMLHttpRequest();
        // request.open('POST', '', true);
        // request.setRequestHeader('Content-Type', 'application/json');
        // request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
        // // request.setRequestHeader('X-CSRFToken', csrfcookie());
        // request.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value);
        // // request.setRequestHeader('A', 1);
        // // request.setRequestHeader('content', '{\"a\": 1}');
        // request.send(JSON.stringify(this.updates));
    }

}
