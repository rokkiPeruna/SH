"use strict"

var main_lobby_menu_bar = new Vue({
  el: ".menu-bar",
  data: {

  },
  methods: {
    onMainLeftPressed: function() {
      if ( !mlobby_cont.show_lcont ) {
        mlobby_cont.show_lcont = !mlobby_cont.show_lcont;
        mlobby_cont.show_mcont = false;
        mlobby_cont.show_rcont = false;
      }
    },
    onMainMiddlePressed: function() {
      if ( !mlobby_cont.show_mcont ) {
        mlobby_cont.show_mcont = !mlobby_cont.show_mcont;
        mlobby_cont.show_lcont = false;
        mlobby_cont.show_rcont = false;
      }
    },
    onMainRightPressed: function() {
      if ( !mlobby_cont.show_rcont ) {
        mlobby_cont.show_rcont = !mlobby_cont.show_rcont;
        mlobby_cont.show_lcont = false;
        mlobby_cont.show_mcont = false;
      }
    }
  }

}); // end main_lobby_menu_bar Vue

var mlobby_cont = new Vue({
  el: "#app-container",
  data: {
    show_lcont: false,
    show_mcont: false,
    show_rcont: false
  }
}); // end mlobby_cont Vue
