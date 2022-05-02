
class Statements extends Exercise {

    constructor(exercise_id) {
        super(exercise_id);
        this.variants = this.body.querySelectorAll('.variant');
        this.initEventListeners();
    }

    initEventListeners() {
        for (let variant of this.variants) {
            variant.addEventListener('click', function (){
                variant.classList.toggle('selected');
            })
        }
    }

    getData() {
        let data = []
        this.variants.forEach(function (variant) {
            if (variant.classList.contains('selected')) {
                data.push(parseInt(variant.dataset.id));
            }
        })
        return data;
    }
}
