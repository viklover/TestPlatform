
class Exercise {

    constructor(exercise_id) {
        this.exercise_id = exercise_id;
        this.body = document.querySelector('#'+exercise_id);
    }

    get_id() {
        return this.exercise_id;
    }

}