
class Answer extends Exercise {

    constructor(exercise_id) {
        super(exercise_id);
        this.input = this.body.querySelector('input');
    }

    getData() {
        return this.input.value;
    }

}
