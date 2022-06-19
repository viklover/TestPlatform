
class TaskManager {

    constructor(body) {
        this.body = body;
        this.exercises = [];
        this.exercises_list = this.body.querySelectorAll('.exercise');

        this.save_button = document.querySelector('.button-save-changes');

        this.changes_manager = new ChangesManager(document.querySelector('.button-save-changes'));
    }

    initObjs() {

        for (let exercise of this.exercises_list) {

            let obj = new Exercise(exercise);

            switch(exercise.dataset.type) {
                case 'chronology':
                    obj = new Chronology(exercise);
                    break;
                case 'match':
                    obj = new Match(exercise);
                    break;
                case 'statements':
                    obj = new Statements(exercise);
                    break;
                case 'radio':
                    obj = new Radio(exercise);
                    break;
                case 'input':
                    obj = new Input(exercise);
                    break;
                case 'answer':
                    obj = new Answer(exercise);
                    break;
            }

            obj.setManager(this);
            obj.initEventListeners();

            this.exercises.push(obj);
        }

    }

    initEventListeners() {
        this.changes_manager.addElement(this);

        let obj = this;

        this.save_button.addEventListener('click', function () {
            obj.save();
        });
    }

    getId() {
        return 'task-manager';
    }

    check() {
        this.changes_manager.check();
    }

    getData() {
        let data = {};
        for (let exercise of this.exercises) {
            if (exercise.exercise_id !== '')
                data[exercise.exercise_id] = exercise.getData();
        }
        return data;
    }

    save() {

        let obj = this;

        console.log(this.getData())

        $.ajax({
            url: '',
            type: "POST",
            data: {
                'json': JSON.stringify(obj.getData())
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfcookie());
            },
            success: function (data) {
                console.log(data)
                obj.changes_manager.refresh();
            },
            error: function (error) {
                console.log('ERROR');
            }
        });
    }
}

let manager = new TaskManager(document.querySelector('.elements-list'))
manager.initObjs();
manager.initEventListeners();

