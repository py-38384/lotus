var updateBtns = document.getElementsByClassName("update-cart");

function roundNumber(num, scale) {
  if(!("" + num).includes("e")) {
    return +(Math.round(num + "e+" + scale)  + "e-" + scale);
  } else {
    var arr = ("" + num).split("e");
    var sig = ""
    if(+arr[1] + scale > 0) {
      sig = "+";
    }
    return +(Math.round(+arr[0] + "e" + sig + (+arr[1] + scale)) + "e-" + scale);
  }
}

function getToken(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
var csrftoken = getToken("csrftoken");

function getRadioSelected(name) {
  var ele = document.getElementsByName(name);
  for (let i = 0; i < ele.length; i++) {
    if (ele[i].checked) {
      return ele[i].dataset.value;
    }
  }
  return "not available";
}

function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  let expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";domain=;path=/";
}

function update_cart(){
  let cart_items_count = 0
  let total_cart_items = document.getElementsByClassName('total_cart_items');
  let cart = getCookie('cart');
  if(cart){
    cart = JSON.parse(cart)
    for(let key in cart){
      cart_items_count+=Number(cart[key]['quantity']);
    }
    for(let i = 0;i<total_cart_items.length;i++){
      total_cart_items[i].innerHTML = cart_items_count;
    }
  }else{
    for(let i = 0;i<total_cart_items.length;i++){
      total_cart_items[i].innerHTML = cart_items_count;
    }
  }
}
if (user === "AnonymousUser") {
  update_cart();
}


for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function (e) {
    var productID = this.dataset.product;
    var action = this.dataset.action;
    var detail_add_to_cart = this.dataset.detailCart;
    var quantity = this.dataset.quantity;
    var orderItemId = this.dataset.orderItemId;
    var has_color = this.dataset.color;
    var has_size = this.dataset.size;
    var color = "Default";
    var size = "Default";



    if (user === "AnonymousUser") {
      let cart = getCookie('cart');
      if(cart){
        cart = JSON.parse(cart)
      }else{
        cart = {}
      }
      if(cart[productID]){
        let row = document.getElementById("product_row_number_" + productID);
        let item_total_price = document.getElementById("item_total_" + productID);
        let current_item_total = Number((item_total_price.innerText).substring(1, ));
        let price = this.dataset.price;
        price = Number(price);
        let subtotal = document.getElementById('subtotal');
        let current_subtotal = Number((subtotal.innerText).substring(1, ));
        let total = document.getElementById('total');
        let current_total = Number((total.innerText).substring(1, ));
        if(action === 'add'){
          if(quantity){
            quantity = document.getElementById("add_cart_quantity").value;
            quantity = Number(quantity);
            cart[productID]['quantity']+=quantity
          }else{
            cart[productID]['quantity']+=1
          }
          let after_item_total = price*Number(cart[productID]['quantity'])
          after_item_total = roundNumber(after_item_total,3)
          let item_total_difference = after_item_total-current_item_total;
          item_total_difference = roundNumber(item_total_difference,3);
          let after_subtotal = current_subtotal+item_total_difference;
          after_subtotal = roundNumber(after_subtotal,3)
          let after_total = current_total+item_total_difference;
          after_total = roundNumber(after_total,3)

          item_total_price.innerHTML = after_item_total+" TAKA";
          subtotal.innerHTML = after_subtotal+" TAKA";
          total.innerHTML = after_total+" TAKA";
          
        }else{
          if(quantity){
            quantity = document.getElementById("add_cart_quantity").value;
            quantity = Number(quantity);
            cart[productID]['quantity']-=quantity
          }else{
            cart[productID]['quantity']-=1
          }
          let after_item_total = price*Number(cart[productID]['quantity'])
          after_item_total = roundNumber(after_item_total,3)
          let item_total_difference = current_item_total-after_item_total;
          item_total_difference = roundNumber(item_total_difference,3);
          let after_subtotal = current_subtotal-item_total_difference;
          after_subtotal = roundNumber(after_subtotal,3)
          let after_total = current_total-item_total_difference;
          after_total = roundNumber(after_total,3)
          item_total_price.innerHTML = after_item_total+" TAKA";
          subtotal.innerHTML = after_subtotal+" TAKA";
          total.innerHTML = after_total+" TAKA";


          if(cart[productID]['quantity']<=0){
            delete cart[productID];
            row.remove();
          }
        }
      }else{
        if(action === 'add'){
          if(quantity){
            quantity = document.getElementById("add_cart_quantity").value;
            quantity = Number(quantity);
            cart[productID]={quantity:quantity}
          }else{
            cart[productID]={quantity:1}
          }
        }
      }
      setCookie('cart',JSON.stringify(cart),30)
      update_cart();
      change_add_to_cart();
    }else {
      if (detail_add_to_cart) {
        if (has_color) {
          color = getRadioSelected("color");
        }
        if (has_size) {
          size = getRadioSelected("size");
        }
      }
      updateUserOrder(productID, action, quantity, color, size, orderItemId);
    }
  });
}
function updateUserOrder(productId, action, quantity, color='default', size='default', orderItemId) {
  var url = "/update_item/";
  let param = null;
  if (quantity) {
    quantity = document.getElementById("add_cart_quantity").value;
    param =
      "productID=" +
      productId +
      "&action=" +
      action +
      "&quantity=" +
      quantity +
      "&color=" +
      color +
      "&size=" +
      size +
      "&order_item_id=" +
      orderItemId;
  } else {
    quantity = 1;
    param =
      "productID=" +
      productId +
      "&action=" +
      action +
      "&quantity=" +
      quantity +
      "&color=" +
      color +
      "&size=" +
      size +
      "&order_item_id=" +
      orderItemId;
  }

  let xhr = new XMLHttpRequest();
  xhr.open("post", url, true);
  xhr.onload = () => {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.readyState == 4 && xhr.status == 200) {
        var data = JSON.parse(xhr.response);
        if (Number(data["total_items"]) <= 0) {
          location.reload();
        }
        var row = document.getElementById("product_row_number_" + data["id"]);
        var product_total = document.getElementById("item_total_" + data["id"]);
        var subtotal = document.getElementById("subtotal");
        var total = document.getElementById("total");
        var cart = document.querySelectorAll(".cart-icon");

        if (subtotal && total) {
          subtotal.innerHTML = data["subtotal"]+" TAKA";
          total.innerHTML = data["total"]+" TAKA";
          product_total.innerHTML = data["total_price"]+" TAKA";
        }
        if (Number(data["quantity"]) <= 0) {
          row.remove();
        }
        for (let i = 0; i < cart.length; i++) {
          cart[i].innerText = data["total_items"];
        }
        if(document.querySelector(
          ".add_cart_div"
        )){
          document.querySelector(
            ".add_cart_div"
          ).innerHTML = `<button class="btn btn-primary px-3 cart_add"
                  style="background:grey;cursor:default;border:none;pointer-events: none;"
                  data-product="{{product.id}}"
                  data-action="add">
                    <i class="fa fa-shopping-cart mr-1"></i> Added To Cart
                  </button>`;
          try{
            document.querySelector(".size_div").remove();
          }catch(e){}
          
          try{
            document.querySelector(".color_div").remove();
          }catch(e){}
        }
        
      }
    }
  };
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  xhr.send(param);
}

function order_item_delete(ele) {
  product_id = ele.dataset.id;
  var url = "/order_item_delete/" + product_id + "/";
  if (user === "AnonymousUser") {
    let cart = getCookie('cart');
      if(cart){
        cart = JSON.parse(cart)
        if(cart[product_id]){
          var row = document.getElementById("product_row_number_" + product_id);
          delete cart[product_id];
          row.remove();
          setCookie('cart',JSON.stringify(cart),30)
          location.reload();
        }
      }
  }else{
      let xhr = new XMLHttpRequest();
      xhr.open("get", url, true);
      xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.readyState == 4 && xhr.status == 200) {
            location.reload();
          }
        }
      };
      xhr.send();
  }
}

function addTrailingZeros(num, totalLength) {
  return String(num).padEnd(totalLength, "0");
}
