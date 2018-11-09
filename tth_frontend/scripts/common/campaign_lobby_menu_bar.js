"use strict"

var campaign_lobby_menu_bar = new Vue({
  el: ".menu-bar",
  delimiters: ["[[", "]]"],
  data: {
    main_left_sect_title: "CHARACTERS",
    main_middle_sect_title: "STORY",
    main_right_sect_title: "NOTES",

    sec_left_sect_title: "",
    sec_middle_sect_title: "",
    sec_right_sect_title: "",

    sec_left_callback: undefined,
    sec_middle_callback: undefined,
    sec_right_callback: undefined,

    show_main_functionality: true
  },
  methods: {
    onMenuIconPressed: function() {
      this.show_main_functionality = !this.show_main_functionality;

    },
    onMainLeftPressed: function() {
      if ( !clobby_cont.show_lcont.value ) {
        clobby_cont.set_active_cont(clobby_cont.show_lcont);

      }
    },
    onMainMiddlePressed: function() {
      if ( !clobby_cont.show_mcont.value ) {
        clobby_cont.set_active_cont(clobby_cont.show_mcont);

      }
    },
    onMainRightPressed: function() {
      if ( !clobby_cont.show_rcont.value ) {
        clobby_cont.set_active_cont(clobby_cont.show_rcont);

      }
    },
    // Secondary functionalities are set as callbacks
    onSecLeftPressed: function() {
      console.log("Secondary left pressed");
    },
    onSecMiddlePressed: function() {
      console.log("Secondary middle pressed");
    },
    onSecRightPressed: function() {
      console.log("Secondary right pressed");
    }
  } // methods

}); // end campaign_lobby_menu_bar Vue

var clobby_cont = new Vue({
  el: "#app-container",
  data: {
    show_lcont: { value: true },
    show_mcont: { value: false },
    show_rcont: { value: false }
  },
  methods: {
    set_active_cont: function(to_show_cont) {
      this.show_lcont.value = false;
      this.show_mcont.value = false;
      this.show_rcont.value = false;
      to_show_cont.value = true;
    }
  }
}); // end clobby_cont Vue
