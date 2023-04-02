let add_to_cart_btns = document.querySelectorAll(".add-to-cart-btn")
add_to_cart_btns.forEach(btn=> btn.addEventListener("click", addToCart))

function addToCart(e){
    let product_id = e.target.value;
    let url = "/add-to-cart";

    let data = {id:product_id};

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("num_of_items").innerHTML = data;
        console.log(data);
    })
    .catch(error=>{
        console.log(error);
    })
}
