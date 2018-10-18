// All index (login) page scripts
"use strict"

//---------------------------------------------
// About -modal
//---------------------------------------------
new Vue({
  // Owner
  el: '#app-container',
  // Instance variables
  data: {
    menu_title: "ABOUT",
    show_modal: false,
    user_name: "",
    password: "",
    remember_me: true,
    rm_storage_id: "index_remember_me",
    dummy_image_src:""
  },
  // Methods bound to events (or something else)
  methods: {
    showModal() {
      this.show_modal = !this.show_modal;
      if ( this.show_modal ) this.menu_title = "CLOSE";
      else this.menu_title = "ABOUT";
      console.debug("Show modal: " + this.show_modal);
    },
    tryLogin( ) {
      console.debug("Trying to log...");
      if ( this.remember_me ) {
        localStorage.setItem( this.rm_storage_id, this.user_name );
      }
      else { //Remove from localStorage
        localStorage.removeItem( this.rm_storage_id );
      }
      // Post username and password to server
      var request = new Request("images/helgawuolikoski.jpg", {
        method: "get"
      });
      var sucee = false;
      fetch( request ).then(function(response) {
        sucee = true;
      }).catch(function(err) {
        alert("Wrong password: " + err);
      });
      this.dummy_image_src = "images/helgawuolikoski.jpg";
    }
  },
  // When instance is created
  mounted: function() {
    let rm = localStorage.getItem( this.rm_storage_id );
    if ( typeof rm !== undefined ) {
      this.user_name = rm;
    }
    else {
      this.user_name = null;
    }
  }

}); // Vue #app-container
