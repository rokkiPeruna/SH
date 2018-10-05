"use strict";

jQuery( document ).ready( function() {

//Load contacts from file in server
$.ajax({
  dataType: "json",
  url: "game_data/contacts.json",
  mimeType: "application/json"
})
.done(function( data ) {
  console.log("Read file " + data.file_name);
  console.log("File data: " + data.contacts);
  for (var i = 0; i < data.contacts.length; i++ ) {
    let cont = data.contacts[i];
    $("#contacts-ulist").append( "<p>Name: "+cont.name+"<\p>" );
    $("#contacts-ulist").append( "<p>Likes me: "+cont.likes_me+"<\p>" );
    $("#contacts-ulist").append( "<p>Influence: "+cont.Influence+"<\p>" );
    $("#contacts-ulist").append( "<p>Story: "+cont.story+"<\p>" );
  }
})
.fail(function() {
  alert("Failed to load contacts!");
});

})// end jQuery( document ).ready
