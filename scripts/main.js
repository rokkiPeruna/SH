var newHeading = document.querySelector('h1');
newHeading.textContent = 'Helo maailma';

var contact_names = document.querySelectorAll("h2.contact_name")

for (i = 0; i < contact_names.length; i++){
  contact_names[i].onclick = function(){
    alert("FUCK THIS SHIT!")
  }
}
