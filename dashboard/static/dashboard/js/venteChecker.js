function validationForm() {
    var selected_product = document.v_form.produit.value;
    var price_cfa = selected_product.split('/').pop(); // taking last element that is the price
    var price = Number(price_cfa.trim().split(' ')[0]);
    // --------------------------------- We Got the price
    var sale_price = document.v_form.price.value;
    var sale_price = Number(sale_price)
        // ---------------------------------- We Got the sale price too
    if (sale_price < price) {
        alert('Attention vous vendez a un prix bas');
    } else {
        return true;
    }
}