
class Task {

    constructor(task_number) {
        this.number = Object.freeze(task_number);
        this.exercises = [];
    }

    getNumber() {
        return this.number;
    }

    addExercise(exercise) {
        this.exercises.push(exercise);
    }

    addExercises(list) {
        this.exercises = list;
    }

    getData() {
        let data = {};
        for (let exercise of this.exercises) {
            data[exercise.getId()] = exercise.getData();
        }
        return data;
    }

    lockAllExercises() {
        for (let exercise of this.exercises) {
            exercise.lock();
        }
    }
}
