// All index (login) page scripts
"use strict"

jQuery( document ).ready(function() {


//---------------------------------------------
// About -modal
//---------------------------------------------
let about_btn = $( "#upper-menu-about-btn" );
let about_modal = $( ".modal" );
let about_content = $( ".modal-content" );
let close_modal = $( "#about-close" );
about_btn.click(function() {
  $( ".modal, .modal-content" ).addClass( "active" );
});

close_modal.click(function() {
  $( ".modal, .modal-content" ).removeClass( "active" );
});


//---------------------------------------------
// Login
//---------------------------------------------
let login_btn = $( "#index-login-btn" );
login_btn.click(function() {
  // Get value from game selector
  let game_val = $( "[name=gamesel]:checked" ).val();
  let dnd = "dnd";
  let dnd_path = "dnd_index.html";
  let shadowrun = "sh";
  let shadowrun_path = "sh_index.html";

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
