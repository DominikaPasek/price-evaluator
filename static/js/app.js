document.addEventListener('DOMContentLoaded', function() {

    const show_category_form = document.getElementById('category_form_btn');
    const category_form = document.getElementById('category_form');

    show_category_form.addEventListener('click', function(event){

        event.preventDefault();

        if (category_form.style.display === 'none') {
            category_form.style.display = 'block';
        }
        else {
            category_form.style.display = 'none';
        }
    })
});
