let password_fields = document.querySelectorAll('input[type=password]');
let main_color = "#FC96DA";
function togglepass(ele){
    if(ele.checked){
        for(let i = 0;i<password_fields.length;i++){
            password_fields[i].type = 'text';
        }
    }else{
        for(let i = 0;i<password_fields.length;i++){
            password_fields[i].type = 'password';
        }
    }
}
function activeSubmitBtn(ele){
    let submit_button = document.querySelector('form .signup');
    if(ele.checked){
        submit_button.style.pointerEvents = "auto";
        submit_button.style.backgroundColor = main_color;
    }else{
        submit_button.style.pointerEvents = "none";
        submit_button.style.backgroundColor = 'gray';
    }
}
//pointer-events: none;