//Отображение первого вопроса
let numberOfQuestion = document.getElementById('numberOfQuestion');
numberOfQuestion.textContent = '1';
//Отоюражение закончилось
let question = document.getElementById('question');
const questions = [
    'Сформируй правильную хронологическую последовательность: '
]
question.textContent = questions[0];