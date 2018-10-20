"use strict"

var main_menu = new Vue({


}); // end main_menu Vue


jQuery( document ).ready(function() {

//Add callbacks to buttons
let home_btn = $( "#upper-menu-home-btn" );
let home = $( ".home" );
let chr_btn = $( "#upper-menu-character-btn" );
let chr = $( ".character" );
let cont_btn = $( "#upper-menu-contacts-btn" );
let cont = $( ".contacts" );

let anim_time_ms = 500;
let height_offset = 50;
let btns_height = home_btn.height() + height_offset;

home_btn.click(function( e ) {
  e.preventDefault();
  let pos = home.offset().top - btns_height;
  $( "html, body" ).animate( { scrollTop: pos }, anim_time_ms );
});
chr_btn.click(function( e ) {
  e.preventDefault();
  let pos = chr.offset().top - btns_height;
  $( "html, body" ).animate( { scrollTop: pos }, anim_time_ms );
});
cont_btn.click(function( e ) {
  e.preventDefault();
  let pos = cont.offset().top - btns_height;
  $( "html, body" ).animate( { scrollTop: pos }, anim_time_ms );
});

}); // end jQuery( document ).ready
