"use strict"

var campaign_lobby_menu_bar = new Vue({
  el: ".menu-bar",
  data: {

  },
  methods: {
    onLeftPressed: function() {
      if ( !clobby_cont.show_lcont ) {
        clobby_cont.show_lcont = !clobby_cont.show_lcont;
        clobby_cont.show_mcont = false;
        clobby_cont.show_rcont = false;
      }
    },
    onMiddlePressed: function() {
      if ( !clobby_cont.show_mcont ) {
        clobby_cont.show_mcont = !clobby_cont.show_mcont;
        clobby_cont.show_lcont = false;
        clobby_cont.show_rcont = false;
      }
    },
    onRightPressed: function() {
      if ( !clobby_cont.show_rcont ) {
        clobby_cont.show_rcont = !clobby_cont.show_rcont;
        clobby_cont.show_lcont = false;
        clobby_cont.show_mcont = false;
      }
    }
  }

}); // end campaign_lobby_menu_bar Vue

var clobby_cont = new Vue({
  el: "#app-container",
  data: {
    show_lcont: false,
    show_mcont: false,
    show_rcont: false
  }
}); // end clobby_cont Vue
