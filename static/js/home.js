let form = document.getElementById('user');
let submit = document.getElementById('submitButton');

form.addEventListener('input', () => {
    for(var i = 0, element; element = form.elements[i++];){
        if(element.tagName == 'SELECT'){
            if(element.options[element.selectedIndex].value != -1){
                submit.removeAttribute('disabled');
            } else {
                submit.setAttribute('disabled', 'disabled');
            }
        }
    }
});
