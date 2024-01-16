const tab_btns = document.querySelectorAll('.orders-btn')
const load_more_btn = document.querySelector('.load-more-btn')
let order_page_indicator = 2
let order_active_stage = 'new_order'
function get_HTML_for_order_and_load_btn_with_column_title(obj_array){
    let html =  `
                <div class="order">
                    <div class="order-id">Order ID</div>
                    <div class="customer-name">Customer Name</div>
                    <div class="customer-order-number">Customer order number</div>
                    <div class="order-time">Order time</div>
                </div>
                `
    obj_array.forEach((obj,index)=>{
        html +=  `
                    <a href="/order/${obj.order_id}" class="order">
                        <div class="order-id">${obj.order_id}</div>
                        <div class="customer-name">${obj.customer_name}</div>
                        <div class="customer-order-number">${obj.customer_order_number}</div>
                        <div class="order-time">${obj.timesince} ago</div>
                    </a> 
                `
    })
    return html
}
tab_btns.forEach((element,index)=>{
    element.addEventListener('click',(event)=>{
        tab_btns.forEach((element2,index2)=>{
            element2.classList.remove('tab-active')
        })
        event.target.classList.add('tab-active')
        order_page_indicator = 1
        if(event.target.classList.contains('new-orders')){
            order_active_stage = 'new_order'
        }
        else if(event.target.classList.contains('registered-orders')){
            order_active_stage = 'registered_orders'
        }
        else if(event.target.classList.contains('processing-orders')){
            order_active_stage = 'processing_orders'
        }
        else if(event.target.classList.contains('on-your-way-orders')){
            order_active_stage = 'on_your_way_orders'
        }
        else if(event.target.classList.contains('complete-orders')){
            order_active_stage = 'complete_orders'
        }
        let url = "?order_page_indicator="+order_page_indicator+"&order_stage="+order_active_stage;
        console.log(url)
        const xhr = new XMLHttpRequest()
        xhr.open("get", url, true)
        xhr.onload = () => {
            if(xhr.readyState === XMLHttpRequest.DONE){
                if(xhr.readyState == 4 && xhr.status == 200) {
                    let data = JSON.parse(xhr.response)
                    const html = get_HTML_for_order_and_load_btn_with_column_title(data.order_data)
                    document.querySelector('.order-container').innerHTML = html
                    if(data.load_more){
                        console.log(data.load_more)
                        load_more_btn.style.display = "block";
                    }else{
                        console.log(data.load_more)
                        load_more_btn.style.display = "none";
                    }
                    order_page_indicator++
                }
            }
        }
        xhr.send()
    })
})
function get_HTML_for_order_and_load_btn(obj_array){
    let html = ""
    obj_array.forEach((obj,index)=>{
        html +=  `
                    <a href="/order/${obj.order_id}" class="order">
                        <div class="order-id">${obj.order_id}</div>
                        <div class="customer-name">${obj.customer_name}</div>
                        <div class="customer-order-number">${obj.customer_order_number}</div>
                        <div class="order-time">${obj.timesince} ago</div>
                    </a> 
                `
    })
    return html
}
if(load_more_btn){
    load_more_btn.addEventListener('click',(event)=>{
        let url = "?order_page_indicator="+order_page_indicator+"&order_stage="+order_active_stage;
        const xhr = new XMLHttpRequest()
        xhr.open("get", url, true)
        xhr.onload = () => {
            if(xhr.readyState === XMLHttpRequest.DONE){
                if(xhr.readyState == 4 && xhr.status == 200) {
                    let data = JSON.parse(xhr.response)
                    const html = get_HTML_for_order_and_load_btn(data.order_data)
                    document.querySelector('.order-container').innerHTML += html
                    if(data.load_more){
                        console.log(data.load_more)
                        load_more_btn.style.display = "block";
                    }else{
                        console.log(data.load_more)
                        load_more_btn.style.display = "none";
                    }
                    order_page_indicator++
                }
            }
        }
        xhr.send()

    })
}