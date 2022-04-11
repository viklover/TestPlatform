
class Radio extends Exercise {

    constructor(exercise_id) {
        super(exercise_id);
        console.log(this.body)
        this.variants = this.body.querySelectorAll('.variant');
        this.initEventListeners();
    }

    initEventListeners() {
        for (let variant of this.variants) {

            let parent = document.querySelector('#'+this.exercise_id)

            variant.addEventListener('click', function () {

                parent.querySelectorAll('.variant').forEach(function (i) {
                    i.classList.remove('selected');
                });

                variant.classList.toggle('selected');
            })
        }
    }

    getData() {
        return parseInt(this.variants.querySelector('.selected').dataset.id);
    }
}
