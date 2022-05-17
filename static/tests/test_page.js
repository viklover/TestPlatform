let form = document.querySelector('#form-comments');
form.addEventListener('submit', function (e) {
    e.preventDefault();

    $.ajax({
      type:"POST",
      url: form.getAttribute('action'),
      data: $(this).serialize(),
      success: setTimeout(() => {window.location.reload()}, 500)
    });
})

