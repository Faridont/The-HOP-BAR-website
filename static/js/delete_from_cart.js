let delete_from_cart_btns = document.querySelectorAll(".delete-from-cart-btn");
delete_from_cart_btns.forEach(btn=> btn.addEventListener("click", deleteFromCart));

function deleteFromCart(e){
    let product_id = e.target.value;
    let url = "/delete-from-cart";

    let data = {id:product_id};

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data=>{
        console.log(data);
        if(data == 0) {
            document.getElementById("num_of_items").innerHTML = "";
            document.getElementById("cart-container").innerHTML = "<h2 class='hop-text-contrast-color mb-5 text-center'>В корзине пусто)</h2>";
        } else {
            document.getElementById("num_of_items").innerHTML = data;
        }
        document.getElementById(`product-tr-${product_id}`).remove();
    })
    .catch(error=>{
        console.log(error)
    })
}
