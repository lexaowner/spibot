console.log('It is start page')

let numb_one = 5;
let numb_two = 52;

console.log(numb_one + numb_two)

var myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})