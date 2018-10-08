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





}); // end jQuery( document ).ready
