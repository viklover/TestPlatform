
class Exercise {

    constructor(exercise_id) {
        this.exercise_id = exercise_id;
    }

    get_id() {
        return this.exercise_id;
    }

}

let variants = document.querySelectorAll('.variant');

for (let variant of variants){
    variant.addEventListener('click', function (){
        variant.classList.toggle('blue');
    })
}

let variantes = document.querySelectorAll('.variantes')

for (let varianter of variantes){
    varianter.addEventListener('click', function (event) {
        varianter.classList.toggle('blue');
    })
}
