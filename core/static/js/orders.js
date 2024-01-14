const tab_btns = document.querySelectorAll('.orders-btn')
tab_btns.forEach((element,index)=>{
    element.addEventListener('click',(event)=>{
        tab_btns.forEach((element2,index2)=>{
            element2.classList.remove('tab-active')
        })
        event.target.classList.add('tab-active')
    })
})