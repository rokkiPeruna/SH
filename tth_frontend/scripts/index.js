"use strict"

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
