document.addEventListener('DOMContentLoaded', function() {

    const selection = document.getElementById('product_options')

    fetch('http://127.0.0.1:8000/products/add_new_product/', {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
    })
    .then(response => response.json())
    .then(data => {

        console.log(data);

        data.results.forEach((product) => {

            const optionElement = document.createElement('option');
            optionElement.innerText = product;
            optionElement.value = product;
            selection.appendChild(optionElement)
        })
    })
    .catch(error => {
        console.log(error);
    })
});