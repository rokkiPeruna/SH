"use strict"

jQuery( document ).ready( function() {

// Create character info from JSON loaded from server
$.ajax({
  dataType: "json",
  url: "game_data/character_template.json",
  mimeType: "application/json"
})
.done( function( data ) {
  console.log("Read character file " + data.file_name);
  console.log("File data: " + data[data.data]);
  // Get all main sections TODO: Better description
  var index = 0;
  data = data[data.data]; // See .json -file for funny looking syntax
  for ( let msect in data ) {
    // Make main section div and button
    let msect_id = "msect-" + index;
    let inner_content_id = "inner-contect-" + index;
    let msect_btn_id = "msect-btn-" + index;
    let div = $( "<div />", { id: msect_id} );
    div.hide(); // Hidden by default
    let btn = $( "<button />", { type:"button", id: msect_btn_id } );
    btn.html( msect.toUpperCase() );
    // Add div and btn to main-secs div, NOTE: Order matters!
    $( "#character-main-secs" ).append( btn);
    $( "#character-main-secs" ).append( div );
    // Add inner content of main section to div TODO: More flexible
    for ( let inner in data[msect] ) {
      // console.log("Inner key: " + inner);
      // console.log("Inner value: " + data[msect][inner]);
      let p = "<p class='character-inner-attr'>"+inner+": "+data[msect][inner]+"</p>";
      div.append( p );
    }
    // NOTE: If index gets referenced after this, logic fails!
    index++;
    // Add callback to button for hiding/showing inner content
    btn.click( function() {
      if ( div.is(":visible") ) {
        div.hide();
      }
      else {
        div.show();
      }
    });
  }
})
.fail( function() {
  alert("Failed to load character!");
});

});// end jQuery( document ).ready
