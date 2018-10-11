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

  var index = 0;
  data = data[data.data]; // See .json -file for funny looking syntax
  // Read JSON-data recursicely
  function parse_data( data, is_top_elem, elem, to_append_to ) {
    let not_value = true;
    let index = 0;
    let to_appn_to = to_append_to;
    for ( let key in data ) {
      // console.log("Key name: " + key);
      // Key is a valid object
      if ( typeof data[key] == "object" && data[key] !== null) {
        if ( is_top_elem === true ){ //Create button for top element
          let key_id = "top-elem-" + index;
          let key_btn_id = "top-elem-btn-" + index++;

          // Add div and btn to elem, make div the next element to append to
          let div = $( "<div />", { id: key_id} );
          to_appn_to = div;
          div.hide(); // Hidden by default
          let btn = $( "<button />", { type:"button", id: key_btn_id } );
          btn.html( key.toUpperCase() );
          elem.append( btn);
          elem.append( div );
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
        else {
          let pass; //TODO: Handle inner objects
        }
      }
      // Key is list
      else if ( Array.isArray( data[key] ) ) {
        // Loop list items
        for ( let i = 0; i < data[key].length; i++ ) {
          parse_data( data[key][i], false);
        }
      }
      // Otherwise key is value. Give change to modify and stop recursion.
      else {
        not_value = false;
        if ( to_appn_to !== undefined ) {
          to_appn_to.append( "<p>"+ key + ": " + data[key] + " </p>");
        }
        else {
          console.log("Element to append to was undefined");
        }
      }
      // Call parser for inner objects and lists also, skip values!
      if ( not_value == true ) {
        // for ( let innerkey in data[key] ) {
          // parse_data( data[key][innerkey], false, elem, to_appn_to);
        // }
        parse_data( data[key], false, elem, to_appn_to);
      }

    }
  }
  // Call parse for the first time
  parse_data(
    data,
    true,
    $( "#character-main-secs" ),
    undefined); // Top level keys handle their HTML attachment
})
.fail( function() {
  alert("Failed to load character!");
});

});// end jQuery( document ).ready
