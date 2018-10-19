// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// All index (login) page scripts
// NOTE: For Django and Vue using {{}} -delimiters by default, Vue's
// delimiters are changed to [[]]
"use strict"

//---------------------------------------------
// About -modal
//---------------------------------------------
var index_vue = new Vue({
  // Owner
  el: '#app-container',
  // Modified delimiters
  delimiters: [ "[[", "]]" ],
  // Instance variables
  data: {
    menu_title: "ABOUT",
    show_modal: false,
  },
  // Methods bound to events (or something else)
  methods: {
    showModal: function() {
      this.show_modal = !this.show_modal;
      if ( this.show_modal ) this.menu_title = "CLOSE";
      else this.menu_title = "ABOUT";
      console.debug("Show modal: " + this.show_modal);
    }
  }
}); // Vue #app-container
