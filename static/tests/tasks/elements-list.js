
class TaskManager {

    constructor(body) {
        this.body = body;
        this.exercises = [];
        this.exercises_list = this.body.querySelectorAll('.exercise');

        this.changes_manager = new ChangesManager(document.querySelector('.button-save-changes'));
    }

    initObjs() {

        for (let exercise of this.exercises_list) {

            let obj = new Exercise(exercise);

            console.log(exercise.dataset.type)

            switch(exercise.dataset.type) {
                case 'chronology':
                    obj = new Chronology(exercise);
                    break;
                case 'match':
                    obj = new Match(exercise);
                    break;
            }

            obj.setManager(this);
            obj.initEventListeners();

            this.exercises.push(obj);
        }

    }

    initEventListeners() {
        this.changes_manager.addElement(this)
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
            data[exercise.exercise_id] = exercise.getData();
        }
        return data;
    }

}

let manager = new TaskManager(document.querySelector('.elements-list'))
manager.initObjs();
manager.initEventListeners();

