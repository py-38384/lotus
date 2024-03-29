
(function ($) {
  "use strict";

  // Dropdown on mouse hover
  $(document).ready(function () {
    function toggleNavbarMethod() {
      if ($(window).width() > 992) {
        $(".navbar .dropdown")
          .on("mouseover", function () {
            $(".dropdown-toggle", this).trigger("click");
          })
          .on("mouseout", function () {
            $(".dropdown-toggle", this).trigger("click").blur();
          });
      } else {
        $(".navbar .dropdown").off("mouseover").off("mouseout");
      }
    }
    toggleNavbarMethod();
    $(window).resize(toggleNavbarMethod);
  });

  // Back to top button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $(".back-to-top").fadeIn("slow");
    } else {
      $(".back-to-top").fadeOut("slow");
    }
  });
  $(".back-to-top").click(function () {
    $("html, body").animate({ scrollTop: 0 }, 1500, "easeInOutExpo");
    return false;
  });

  // Vendor carousel
  $(".vendor-carousel").owlCarousel({
    loop: true,
    margin: 29,
    nav: false,
    autoplay: true,
    smartSpeed: 1000,
    responsive: {
      0: {
        items: 2,
      },
      576: {
        items: 3,
      },
      768: {
        items: 4,
      },
      992: {
        items: 5,
      },
      1200: {
        items: 6,
      },
    },
  });

  // Related carousel
  $(".related-carousel").owlCarousel({
    loop: true,
    margin: 29,
    nav: false,
    autoplay: true,
    smartSpeed: 1000,
    responsive: {
      0: {
        items: 1,
      },
      576: {
        items: 2,
      },
      768: {
        items: 3,
      },
      992: {
        items: 4,
      },
    },
  });

  // Product Quantity
  $(".quantity button").on("click", function () {
    var button = $(this);
    var oldValue = button.parent().parent().find("input").val();
    if (button.hasClass("btn-plus")) {
      var newVal = parseFloat(oldValue) + 1;
    } else {
      if (oldValue > 0) {
        var newVal = parseFloat(oldValue) - 1;
      } else {
        newVal = 0;
      }
    }
    button.parent().parent().find("input").val(newVal);
  });
})(jQuery);

let price_checkbox = document.getElementsByClassName("price-checkbox");
for (let i = 0; i < price_checkbox.length; i++) {
  price_checkbox[i].addEventListener("click", function (e) {
    let param = "?price_range=";
    for (let j = 0; j < price_checkbox.length; j++) {
      if (price_checkbox[j].checked) {
        param += price_checkbox[j].dataset.range;
      }
    }
    if(param === "?price_range="){
        param = "?price_range=0";
    }
    let xhr = new XMLHttpRequest();
    xhr.open("get", param, true);
    xhr.onload = () => {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let data = xhr.response;
            document.querySelector('.product_div').innerHTML = data;
        }
      }
    }
    xhr.send()
  });
}


function get_your_orders_html(obj){
  let html = ``
  for (let ele of obj.order_array){
      html += `
      <a href="/your_order_details/${ele.order_id}" class="order">
        <div class="order-id">
          ${ele.order_id}
        </div>
        <div class="order-number">
          ${ele.customer_order_no}
        </div>
        <div class="order-time">
          ${ele.order_time}
        </div>
        <div class="order-status">
            <span class="${ele.order_status.toLowerCase()}">${ele.order_status}</span>
        </div>
      </a>
      `
  }
  return html
}


let current_page_num = 1
your_order_load_more_button = document.querySelector('.load-more-container button')
if(your_order_load_more_button){
  your_order_load_more_button.addEventListener('click',(e)=>{
    next_page = current_page_num+1
    let url = "?order_page_indicator="+next_page;
    console.log(url)
    let xhr = new XMLHttpRequest();
    xhr.open("get", url, true);
    xhr.onload = () => {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let data = JSON.parse(xhr.response);
            if(!data.load_more){
              e.target.style.display = "none";
            }
            console.log(data)
            const html = get_your_orders_html(data)
            document.querySelector('.your_order_container').innerHTML += html
            current_page_num++
        }
      }
    }
    xhr.send()
  })
}

const your_order_delete_button = document.querySelector('.your_order_delete_button')
if (your_order_delete_button){
  your_order_delete_button.addEventListener('click',(e)=>{
    order_id = e.target.dataset.id
    const param = "id="+order_id
    let url = "/your_order_delete/"
    let xhr = new XMLHttpRequest();
    xhr.open("post", url, true);
    xhr.onload = () => {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let data = JSON.parse(xhr.response);
            if(data.operation === "successful"){
              location.replace('/your_order/')
            }
            console.log(data)
        }
      }
    }
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send(param);
    })
}