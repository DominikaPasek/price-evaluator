document.addEventListener('DOMContentLoaded', function() {

    const buttons = document.querySelectorAll('.show_content');

    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            // const buttons = document.querySelectorAll('.show_content');
            // console.log(buttons)
            const products = e.target.parentElement.nextElementSibling.nextElementSibling;
            if (products.style.display === 'block') {
                products.style.display = 'none';
                button.innerText = 'Pokaż';
            } else {
                products.style.display = 'block';
                button.innerText = 'Ukryj';
            }
        })
    });
});