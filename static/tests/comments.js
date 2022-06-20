let sent_comment = document.getElementById('sent_comment');
let description_comment = document.getElementById('description_comment')
sent_comment.onclick = function (key, value) {
    let input_comment = document.getElementById('input').value;
    description_comment.textContent = input_comment;
    let comment = [];
    comment.push(input_comment);
    localStorage.setItem("myKey",JSON.stringify(comment));
    let memory = JSON.parse(localStorage.getItem("myKey"));
    console.log(memory);
}