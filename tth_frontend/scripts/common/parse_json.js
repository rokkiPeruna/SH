"use strict"

// TODO: Move to conf file when such is created
var top_elem_prefix     = "top-elem-";
var top_elem_btn_prefix = "top-elem-btn-"
var modifier_id_prefix  = "mod-id-for-";

// Create proper modifier depending on the data type of the value
function create_modifier( key, value ) {
  if ( typeof value === "string" ) {
    let label_name = key;
    let id = modifier_id_prefix + label_name;
    let elem = //TODO: Move this to a separate HTML file
      "<div class='string-modifier'> \
         <p>"+key+"</p>\
         <label for='"+label_name+"'</label>\
         <input type='text' name='"+label_name+"' id='"+id+"' value='"+value+"'>\
      </div>";
    return elem;
  }
  else if ( typeof value === "number" ) {
    let label_name = key;
    let id = modifier_id_prefix + label_name;
    let elem = //TODO: Move this to a separate HTML file
      "<div class='number-modifier'> \
         <p>"+key+"</p>\
         <label for='"+label_name+"'</label>\
         <input type='number' name='"+label_name+"' id='"+id+"' value='"+value+"'>\
      </div>";
    return elem;
  }
  else {
    return "<p>PASKAAAA</p>";
  }
}

jQuery( document ).ready( function() {

// Create character info from JSON loaded from server
$.ajax({
  dataType: "json",
  url: "game_data/sh_character_template.schema.json",
  mimeType: "application/json"
})
.done( function( data ) {

  //NOTE: TESTING
  var element = document.getElementById( "json-editor-placeholder" );
  var editor = new JSONEditor( element, {
    ajax:                     true,
    disable_array_add:        true,
    disable_array_delete:     true,
    disable_array_reorder:    true,
    disable_collapse:         true,
    disable_edit_json:        true,
    disable_properties:       true,
    array_controls_top:       true,
    form_name_root:           "val-form-",
    iconlib:                  null,
    no_additional_properties: false,
    refs:                     {},
    required_by_default:      false,
    keep_oneof_values:        true,
    schema:                   {},
    show_errors:              "interactions",
    startval:                 null,
    // template:                 default,
    theme:                    "html",
    display_required_only:    false,
    prompt_before_delete:     true
  });
  JSONEditor.defaults.options.object_layout = "grid";
  editor.setValue(data[data.data]);


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
          let key_id = top_elem_prefix + index;
          let key_btn_id = top_elem_btn_prefix + index++;

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
          to_appn_to.append( create_modifier( key, data[key] ) );
        }
        else {
          console.log("Element to append to was undefined");
        }
      }
      // Call parser for inner objects and lists also, skip values!
      if ( not_value == true ) {
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
