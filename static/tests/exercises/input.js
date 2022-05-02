
class Input extends Exercise {

    constructor(exercise_id) {
        super(exercise_id);
        this.textarea = this.body.querySelector('textarea');
        this.textarea.addEventListener(
            "input",
            function () {
              this.style.height = 'auto';
              this.style.height = (this.scrollHeight) + 'px';
            },
            false
        );
    }

    getData() {
        return this.textarea.value;
    }
}
