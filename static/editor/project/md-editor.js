let edit_info_tab = document.querySelector('.edit-info');
let button_md_save = document.querySelector('.button-save-md');

$("#edit-info-form").on("submit", function(e) {

    let dataString = $(this).serialize();

    $.ajax({
        type: "POST",
        url: "upload_description/",
        data: dataString,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrfcookie());
        },
        success: function () {
            console.log('success')
            button_md_save.classList.add('not-allowed')
        }
    })

    e.preventDefault();
});

let simplemde = new SimpleMDE({
    autoDownloadFontAwesome: undefined,
    element: document.getElementById("edit-info"),
    spellChecker: false,
    autofocus: true,
    togglePreview: true
});
simplemde.codemirror.on("change", function(){
    document.querySelector('#edit-info').value = simplemde.value();
    if (button_md_save.classList.contains('not-allowed')) {
        button_md_save.classList.remove('not-allowed')
    }
});
simplemde.codemirror.on("refresh", function() {
    document.querySelector('.head').classList.toggle('hidden', simplemde.isFullscreenActive())
    edit_info_tab.classList.toggle('tab-relative', !simplemde.isFullscreenActive())
});
edit_info_tab.classList.add('hidden');
edit_info_tab.classList.remove('not-visible');