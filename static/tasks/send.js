
let accept_button = document.querySelector('.accept-button');

accept_button.onclick = function () {
    let request = new XMLHttpRequest();
    request.open("GET", 'send', false);
    request.setRequestHeader("Content-Type", "application/plain");
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            let json = JSON.parse(request.responseText);
            console.log(json)
        }
    };
    console.log(JSON.stringify(task.getData()))
    request.send(JSON.stringify(task.getData()));
}
