
let changesManager = new ChangesManager('.button-save-changes');

let elementsManager = new ElementsManager();
elementsManager.setChangesManager(changesManager);

for (let element of document.querySelectorAll('.elements-list__item')) {

    let obj = null;

    switch (element.dataset.type) {
        case 'chronology':
            obj = new ChronologyElement(element);
            break;
        case 'match':
            obj = new MatchElement(element);
            break;
        case 'radio':
            obj = new RadioElement(element);
            break;
        case 'statements':
            obj = new StatementsElement(element);
            break;
        case 'input':
            obj = new InputElement(element);
            break;
        case 'answer':
            obj = new AnswerElement(element);
            break;
        case 'exercise':
            obj = new Exercise(element);
            break;
        default:
            obj = new Element(element);

    }

    obj.setManager(elementsManager);
    obj.initEventListeners();

    console.log(obj)

    elementsManager.addElement(obj);
}
changesManager.addElement(elementsManager);


let button = document.querySelector('.button-save-changes');
button.onclick = function () {
    changesManager.sendUpdates()
};
