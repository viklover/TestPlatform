
let upload_button = document.querySelector('.upload-file-button');
let file_uploader = document.querySelector('.file-uploader');

let icon_preview = document.querySelector('.image_icon');

upload_button.addEventListener('click', function () {
    file_uploader.click();
});

file_uploader.addEventListener('change', function (event) {
    const [file] = file_uploader.files
    if (file) {
        icon_preview.src = URL.createObjectURL(file)
    }
});
