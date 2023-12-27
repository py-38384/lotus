let password_fields = document.querySelectorAll('input[type=password]');
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