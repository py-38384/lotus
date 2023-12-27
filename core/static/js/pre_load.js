let review_stars = document.querySelectorAll('.review_star');
let review_page_indicator = 2;
for(let i=0;i<review_stars.length;i++){
  review_stars[i].addEventListener('click',)
}
function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return undefined;
}
function change_add_to_cart() {
  if (user === "AnonymousUser") {
    let add_to_cart_div = document.querySelector(".add_cart_div");
    let cart = getCookie("cart");
    if (cart) {
      cart = JSON.parse(cart);
      if (cart[product_id]) {
        add_to_cart_div.innerHTML = `<button
                  class="btn btn-primary px-3"
                  style="
                    background: grey;
                    cursor: default;
                    border: none;
                    pointer-events: none;
                  "
                  data-product="{{product.id}}"
                  data-action="add"
                >
                  <i class="fa fa-shopping-cart mr-1"></i> Added To Cart
                </button>`;
      }
    }
  }
}

// password to text function
function togglepass(ele) {
  if (ele.checked) {
    let password_fields = document.querySelectorAll("input[type=password]");
    for (let i = 0; i < password_fields.length; i++) {
      password_fields[i].type = "text";
    }
  } else {
    let password_fields = document.querySelectorAll("input[type=text]");
    for (let i = 0; i < password_fields.length; i++) {
      password_fields[i].type = "password";
    }
  }
}

function set_review_star(index) {
  let review_star_div = document.querySelector(".review_star_div");
  review_star_div_children = review_star_div.children;
  let review_star = document.getElementById("review-star-value");
  for (let i = 0; i < review_star_div_children.length; i++) {
    review_star_div_children[i].classList.remove("fa");
  }
  for (let i = 0; i < index; i++) {
    review_star_div_children[i].classList.add("fa");
  }
  review_star.value = index;
}

//review edit functions for product details page
function get_review_star(star) {
  let review_star = "";
    if (star == 1) {
      review_star = `
              <i class="fas fa-star"></i>
              <i class="far fa-star"></i>
              <i class="far fa-star"></i>
              <i class="far fa-star"></i>
              <i class="far fa-star"></i>
              `;
    } else if (star == 2) {
      review_star = `
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
              <i class="far fa-star"></i>
              <i class="far fa-star"></i>
              <i class="far fa-star"></i>
      `;
    } else if (star == 3) {
      review_star = `
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
              <i class="far fa-star"></i>
              <i class="far fa-star"></i>
      `;
    } else if (star == 4) {
      review_star = `
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
              <i class="far fa-star"></i>
      `;
    } else {
      review_star = `
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
      `;
    }
  return review_star;
}

function getReviewHtml(obj,see_more=false) {
  console.log(obj);
  let html = '';
  if(see_more){}else{
    html = '<h4 class="mb-4">' + obj["product_count"] + ' review for "' + obj["product"] + '"</h4>';
  }
  let review_action_buttons = ``;
  
  let review_count_a = document.querySelector(".review-count-a");
  if(review_count_a){
    review_count_a.innerHTML = `Reviews (${obj["product_count"]})`;
  }
  let review_star = "";
  for (let i = 0; i < obj["reviews"].length; i++) {
    if(obj['reviews'][i]['user']['user_email']===user){
      review_action_buttons = `
      <span class="review-action-button-edit review-action-button" onclick="edit_review(this,event,${obj["reviews"][i]["id"]})">Edit</span><span class="review-action-button-delete review-action-button" onclick="delete_review(this,event,${obj["reviews"][i]["id"]})">Delete</span>
      `;
    }else{
      review_action_buttons = ``;
    }
    review_star = get_review_star(obj["reviews"][i]["review_star"]);
    html += `
                  <div class="media mb-4 review_div_${obj["reviews"][i]["id"]}">
                    <a href="">
                    <img
                      src="${obj["reviews"][i]["user"]["user_image"]}/"
                      alt="Image"
                      class="img-fluid mr-3 mt-1"
                      style="width: 45px"
                    />
                    </a>
                    <div class="media-body">
                      <h6>
                        <a href="">${obj["reviews"][i]["user"]["user_name"]}</a><small> - <i>${obj["reviews"][i]["timesince"]}</i></small>
                      </h6>
                      <div class="text-primary mb-2">
                        ${review_star}
                      </div>
                      <p>
                        ${obj["reviews"][i]["comment"]}
                      </p>
                      <div class="review-action-button-div">
                        ${review_action_buttons}
                      </div>
                    </div>
                  </div>
    `;
  }
  return html;
}

function post_review(e) {
  e.preventDefault();
  let review_star = document.getElementById("review-star-value").value;
  let comment = document.querySelector(".comment-box");
  let comment_value = comment.value;
  let review_id_hidden = document.getElementById('review-id-hidden');
  let url = "/add_review/";
  let param = '';
  if(review_id_hidden){
    param =
    "review_star=" +
    review_star +
    "&comment=" +
    comment_value +
    "&review_id="+
    review_id_hidden.value;
  }else{
    param =
      "product_id=" +
      product_id +
      "&review_star=" +
      review_star +
      "&comment=" +
      comment_value;
  }
  if (review_star > 0) {
    let xhr = new XMLHttpRequest();
    xhr.open("post", url, true);
    xhr.onload = () => {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.readyState == 4 && xhr.status == 200) {
          var data = JSON.parse(xhr.response);
          if(review_id_hidden){
            let review_id_hidden = document.getElementById('review-id-hidden');
            let review_header = document.querySelector(".review-header");
            let submit_comment = document.getElementById('submit_comment');
            submit_comment.value = "Leave Your Review";
            review_id_hidden.remove();
            review_header.innerHTML = "Leave a review";
          }
          comment.value = "";
          set_review_star(-1);
          let review_div = document.querySelector(".review-div");
          let html = getReviewHtml(data);
          review_div.innerHTML = html;
        }
      }
    };
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(param);
  }
}

function edit_review(element, event, review_id) {
  let comment_box = document.querySelector(".comment-box");
  let review_header = document.querySelector(".review-header");
  let url = "/get_review/";
  let param = "review_id=" + review_id;
  let xhr = new XMLHttpRequest();
  xhr.open("post", url, true);
  xhr.onload = () => {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.readyState == 4 && xhr.status == 200) {
        let data = JSON.parse(xhr.response);
        let form = document.querySelector('.review-form');
        let element = document.createElement('input');
        let submit_comment = document.getElementById('submit_comment');
        submit_comment.value = "Submit";
        element.setAttribute('type','hidden');
        element.setAttribute('value',review_id);
        element.setAttribute('id','review-id-hidden');
        form.appendChild(element)
        review_header.innerHTML = `Edit a review of your for this product`;
        if(data["comment"]){
          comment_box.value = data["comment"];
        }
        set_review_star(data['review_star']);
      }
    }
  };
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  xhr.send(param);
}

function edit_review_manage(element, event, review_id) {
  let comment_box = document.querySelector(".comment-box");
  let review_header = document.querySelector(".review-header");
  let url = "/get_review/";
  let param = "review_id=" + review_id;
  let xhr = new XMLHttpRequest();
  xhr.open("post", url, true);
  xhr.onload = () => {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.readyState == 4 && xhr.status == 200) {
        let data = JSON.parse(xhr.response);
        let form = document.querySelector('.review-form');
        let element = document.createElement('input');
        let submit_comment = document.getElementById('submit_comment');
        submit_comment.value = "Submit";
        element.setAttribute('type','hidden');
        element.setAttribute('value',review_id);
        element.setAttribute('id','review-id-hidden');
        form.appendChild(element)
        review_header.innerHTML = `Edit a review of your for this product`;
        if(data["comment"]){
          comment_box.value = data["comment"];
        }
        set_review_star(data['review_star']);
      }
    }
  };
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  xhr.send(param);
}

function delete_review(element, event, review_id) {
  let delete_confirm = confirm('Do you really want to delete this review?');
  let xhr = new XMLHttpRequest();
  url = "/delete_review/";
  param = "review_id="+review_id;
  xhr.open("post", url, true);
  xhr.onload = () => {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.readyState == 4 && xhr.status == 200) {
        let data = JSON.parse(xhr.response);
        let total_review = data['total_review'];
        let review_count_a = document.querySelector(".review-count-a");
        let review_header = document.querySelector('.review_header');
        
        review_count_a.innerHTML = `Reviews (${total_review})`;
        let deleted_review_div = document.querySelector(`.review_div_${review_id}`);
        if('success' in data){
          deleted_review_div.remove();
        }
        review_header.innerHTML = '<h4 class="mb-4">' + data['total_review'] + ' review for "' + data["product"] + '"</h4>';
      }
    }
  };
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  if(delete_confirm){
    xhr.send(param);
  }
}



function see_more(){
  let url = '/get_reviews/';
  param = "review_page_indicator="+review_page_indicator+"&product_id="+product_id;
  review_div = document.querySelector('.review-div')
  let xhr = new XMLHttpRequest();
  xhr.open("post", url, true);
  xhr.onload = () => {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.readyState == 4 && xhr.status == 200) {
        var data = JSON.parse(xhr.response);
        let html = getReviewHtml(data,true);
        review_div.innerHTML+=html;
        review_page_indicator++;
        update_see_more_button_existence();
      }
    }
  };
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  xhr.send(param);
}

//close bootstrap model
function closeOneModal(modalId) {

  // get modal
  const modal = document.getElementById(modalId);

  // change state like in hidden modal
  modal.classList.remove('show');
  modal.setAttribute('aria-hidden', 'true');
  modal.setAttribute('style', 'display: none');

   // get modal backdrop
   const modalBackdrops = document.getElementsByClassName('modal-backdrop');

   // remove opened modal backdrop
    document.body.removeChild(modalBackdrops[0]);
}

//review edit functions for manage account
function edit_review_for_manage_account(element,event,review_id){
  let url = "/get_review/";
  let param = "review_id=" + review_id;
  let xhr = new XMLHttpRequest();
  xhr.open("post", url, true);
  xhr.onload = () => {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.readyState == 4 && xhr.status == 200) {
        let data = JSON.parse(xhr.response);
        let form = document.querySelector('.review-form');
        let element = document.createElement('input');
        let comment_box = document.querySelector('.comment-box');
        element.setAttribute('type','hidden');
        element.setAttribute('value',review_id);
        element.setAttribute('id','review-id-hidden');
        form.appendChild(element)
        if(data["comment"]){
          comment_box.value = data["comment"];
        }
        set_review_star(data['review_star']);
      }
    }
  };
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  xhr.send(param);
}
function delete_review_confirm_for_manage_account_activate(element,event,review_id){
  let body = document.querySelector('body');
  let confirm_wrapper = document.querySelector('.confirm-wrapper'); 
  confirm_wrapper.style.display = 'flex';
  let ok_button = document.querySelector('.ok-button button'); 
  ok_button.onclick = function (){delete_review_for_manage_account(review_id)};
  body.style.overflow = 'hidden';
}
function delete_review_confirm_for_manage_account_close(){
  let body = document.querySelector('body');
  let confirm_wrapper = document.querySelector('.confirm-wrapper');
  confirm_wrapper.style.display = 'none';
  body.style.overflow = 'scroll';
}
function delete_review_for_manage_account(review_id){
  delete_review_confirm_for_manage_account_close();
  let review_div = document.querySelector(`.review_div_${review_id}`);
  let xhr = new XMLHttpRequest();
  url = "/delete_review/";
  param = "review_id="+review_id;
  xhr.open("post", url, true);
  xhr.onload = () => {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.readyState == 4 && xhr.status == 200) {
        review_div.remove();
      }
    }
  };
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", csrftoken);
  xhr.send(param);
}
function edited_review_post_for_manage_account(event){
  event.preventDefault();
  let review_star = document.getElementById("review-star-value").value;
  let comment = document.querySelector(".comment-box");
  let comment_value = comment.value;
  let review_id_hidden = document.getElementById('review-id-hidden');
  let url = "/add_review_for_account_manage/";
  let param =
    "review_star=" +
    review_star +
    "&comment=" +
    comment_value +
    "&review_id="+
    review_id_hidden.value;
  if (review_star > 0) {
    let xhr = new XMLHttpRequest();
    xhr.open("post", url, true);
    xhr.onload = () => {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.readyState == 4 && xhr.status == 200) {
          var data = xhr.response;
          closeOneModal('account-review-edit-form');
          review_id_hidden.remove();
          comment.value = "";
          set_review_star(-1);
          let review_div = document.querySelector(".review-div");
          review_div.innerHTML = data;
        }
      }
    };
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(param);
  }
}