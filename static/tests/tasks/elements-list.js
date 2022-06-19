
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
                case 'images':
                    obj = new Images(exercise);
                    break;
                case 'matchlist':
                    obj = new MatchList(exercise);
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

let task_manager = new TaskManager(document.querySelector('.elements-list'))
task_manager.initObjs();
task_manager.initEventListeners();


$(function () {
    $(".slb").simplebox({
        fadeSpeed: 200,
        darkMode: true
    });
});

Pred.onclick = function() {

    Pred.classList.toggle("choice-chosed")

    let tdPred = Pred.querySelectorAll("td")
    if (Pred.classList.contains("choice-chosed")) {
        let done = document.createElement("div")
        done.classList.add("material-symbols-outlined")
        done.classList.add("btn")
        done.classList.add("done-btn")
        done.textContent = "check_circle"
        tdPred[tdPred.length - 1].append(done)
    } else {
        tdPred[tdPred.length - 1].removeChild(Pred.querySelector('.done-btn'));
    }

    for (let q = 0; q < trPreds.length; q++) {
        if (trPreds[q].dataset.id !== Pred.dataset.id) {
            if (trPreds[q].classList.contains("choice-chosed")) {
                let td_elems = trPreds[q].querySelectorAll('td');
                td[td_elems.length - 1].removeChild(td_elems.querySelector('.done-btn'));
            }
            trPreds[q].classList.remove("choice-chosed")
        }
    }
}