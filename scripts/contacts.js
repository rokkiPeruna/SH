"use strict";

jQuery( document ).ready( function() {

//Load contacts from file in server
$.ajax({
  dataType: "json",
  url: "game_data/contacts.json",
  mimeType: "application/json"
})
.done(function( data ) {
  console.log("Read contact file " + data.file_name);
  console.log("File data: " + data[data.data]);
  // Loop all contacts
  for ( let i = 0; i < data.contacts.length; i++ ) {
    let cont = data.contacts[i];
    // Write key-value pairs to HTML
    for (let key in cont) {
      // console.log("Key: " + key + ", Value: " + cont[index]);
      //Keys starting with capital letter are visible in UI
      if (key[0] == key[0].toUpperCase())
        $("#contacts-ulist").append( "<p>"+key+": "+cont[key]+"<\p>" );
    }
    // Check if contacts has picture path and picture available
    if (cont.hasOwnProperty("image_path")) {
      let path = cont["image_path"];
      // Create button to show and hide image
      let btn_id = "img-btn-" + i;
      let img_id = "img-" + i;
      console.log("Loading picture from " +  path);
      let btn = $( "<button />", { type:"button", id: btn_id } );
      $("#contacts-ulist").append(btn);
      // Create image, hide by default
      let img = $( "<img />", { src:path, "id": img_id } );
      $("#contacts-ulist").append(img);
      //btn.append(img);
      img.hide();
      btn.html("Show picture");
      // Apply callback to button
      //$( "#"+btn_id ).click(function() {
      btn.click(function() {
        if ( img.is( ":visible" )) {
          img.hide();
          btn.html("Show picture")
        }
        else {
          img.show();
          btn.html("Hide picture")
        }
      });
    }
  }
})
.fail(function() {
  alert("Failed to load contacts!");
});

});// end jQuery( document ).ready
