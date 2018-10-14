// All index (login) page scripts
"use strict"

jQuery( document ).ready(function() {


//---------------------------------------------
// About -modal
//---------------------------------------------

// Get the modal
var modal = $( "#about-modal" );
// Get the button that opens the modal
var btn = $( "#upper-menu-about-btn" );
// When the user clicks on the button, open the modal
btn.click(function() {
  if (modal.css("display") == "none") {
    modal.css("display", "block");
  }
  else {
    modal.css("display", "none");
  }
});
// When the user clicks on the modal, close the it
modal.click(function() {
  if (modal.css("display") != "none") {
    modal.css("display", "none");
  }
});

//---------------------------------------------
// Login
//---------------------------------------------
let login_btn = $( "#index-login-btn" );
login_btn.click(function() {
  // Get value from game selector
  let game_val = $( "[name=gamesel]:checked" ).val();
  let dnd = "dnd";
  let dnd_path = "main.html";
  let shadowrun = "sh";
  let shadowrun_path = "main.html";

  if ( game_val ) {
    console.log("game:" + game_val);
    if ( game_val == dnd ) {
      window.location = dnd_path;
    }
    else if ( game_val == shadowrun ) {
      window.location = shadowrun_path;
    }
    else {
      console.log("Unknown gametype: " + game_val );
    }
  }
  else {
    // TODO: Modal pop instead!
    alert("No game chosen!");
  }
});

}); // end jQuery( document ).ready
