
let changesManager = new ChangesManager(document.querySelector('#save_schema'));

let elementsManager = new ElementsManager();
elementsManager.setChangesManager(changesManager);

for (let element of document.querySelectorAll('.elements-list__item')) {

    let obj = null;

    switch (element.dataset.type) {
        case 'chronology':
            obj = new ChronologyExercise(element);
            break;
        case 'match':
            obj = new MatchExercise(element);
            break;
        case 'radio':
            obj = new RadioExercise(element);
            break;
        case 'statements':
            obj = new StatementsExercise(element);
            break;
        case 'input':
            obj = new InputExercise(element);
            break;
        case 'answer':
            obj = new AnswerExercise(element);
            break;
        case 'exercise':
            obj = new Exercise(element);
            break;
        case 'images':
            obj = new ImagesExercise(element);
            break;

        case 'title':
            obj = new TitleElement(element);
            break;
        case 'picture':
            obj = new PictureElement(element);
            break;
        case 'quote':
            obj = new QuoteElement(element);
            break;
        case 'document':
            obj = new DocumentElement(element);
            break;
        case 'maps':
            obj = new YandexMapsElement(element);
            break;
        default:
            obj = new Element(element);
    }

    obj.setManager(elementsManager);
    obj.initEventListeners();

    elementsManager.addElement(obj);
}
changesManager.addElement(elementsManager);


let button = document.querySelector('#save_schema');
button.onclick = function () {
    changesManager.sendUpdates()
};
