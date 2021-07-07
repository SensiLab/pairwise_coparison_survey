let form = document.getElementById('vote');
let submit = document.getElementById('castVote');
let a = document.getElementById('a');
let img_a = document.getElementById('img-a');
let img_col_a = document.getElementById('img-col-a');
let b = document.getElementById('b');
let img_col_b = document.getElementById('img-col-b');
let img_b = document.getElementById('img-b')
let c = document.getElementById('c');
let img_c = document.getElementById('btn-c');
// let counter = document.getElementById('counter').data('counter');
var count = $('#counter').data('counter');


form.addEventListener('input', () => {
    submit.removeAttribute('disabled');

    if(a.checked) {
        // img_col_a.addAttribute('active');
        img_a.classList.add("img-hl");
        img_b.classList.remove("img-hl");
        img_c.classList.remove("img-hl");

        // console.log("A is selected");
      }else if(b.checked) {
        img_a.classList.remove("img-hl");
        img_b.classList.add("img-hl");
        img_c.classList.remove("img-hl");
        // console.log("B is selected");
      }else if(c.checked){
        img_a.classList.remove("img-hl");
        img_b.classList.remove("img-hl");
        img_c.classList.add("img-hl");
      }
});

document.getElementById('exit-btn').onclick = function(){
    location.href='/exit';
}

function openModal() {
  document.getElementById("backdrop").style.display = "block";
  document.getElementById("msgModal").style.display = "block";
  document.getElementById("msgModal").classList.add("show");

}

function closeModal() {
  document.getElementById("backdrop").style.display = "none";
  document.getElementById("msgModal").style.display = "none";
  document.getElementById("msgModal").classList.remove("show");
}

var modal = document.getElementById("msgModal");

window.onclick = function (event) {
  if(event.target == modal){
    closeModal();
  }
}
document.onreadystatechange = function () {
  if(document.readyState == "complete" && (count == 10)){
    openModal();
  }
}

document.getElementById('close-modal').onclick = function() {
  closeModal();
}

document.getElementById('exit-btn2').onclick = function() {
  location.href='/exit';
}


