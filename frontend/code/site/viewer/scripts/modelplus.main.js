// TODO - learn headers for globals...

/**
 * The ModelPlus variables and functions are being moved to this namespace to avoid clutering the global namespace.
 * @namespace
 */
var modelplus = modelplus || {};

(function () {
  "use strict";
  
  modelplus.main = modelplus.main || {};
  
  // persistence variables
  modelplus.main.persist = modelplus.main.persist || {};
  modelplus.main.persist.hold_select = null;
  modelplus.main.persist.map_river_zoom = null;
  
  /**
   *
   */
  modelplus.main.display_message_block = function(msg_html){
	var div_modal, div_modal_ctt, inner_html;
	
	div_modal_ctt = $('#modal_content_div');
	div_modal = document.getElementById(modelplus.ids.MODAL_DIV);
    div_modal.style.display = "block";
    inner_html = "<p><span id='modal_close_span' onclick='modelplus.main.hide_message_block()'>×</span></p>";
    inner_html += "<p>" + msg_html + "</p>";
    div_modal_ctt.html(inner_html);
	
    // register 'ESC' as closing key
    modelplus.keyCodes[modelplus.ABOUT_CLOSE_BUTTON] = function(){
      modelplus.main.hide_message_block();
    };
  }

  /**
   *
   */
  modelplus.main.hide_message_block = function(){
    $("#"+modelplus.ids.MODAL_DIV).hide();
  }
  
  /**
   *
   */
  modelplus.main.get_selected_in_div = function(div_id){
    var cur_div, cur_idx_a, cur_div, cur_all_a, cur_a;
	
    cur_div = $("#" + div_id);
    cur_all_a = cur_div.find("a");
    for(cur_idx_a in cur_all_a){
      cur_a = cur_all_a[cur_idx_a];
      try{
        if (cur_a.classList.contains("npact")){
          return(cur_a.id); }
      } catch (err) { continue; }
    }
    return(null);
  }
  
  /**
   *
   */
  modelplus.main.get_displayed_representation = function(){
    var considered_divs, cur_considered_div;
    var cur_idx_div, cur_menu_id;
	
    considered_divs = [modelplus.ids.MENU_MODEL_MAIN_SELEC_DIV,
                       modelplus.ids.MENU_MODEL_COMP_SELEC_DIV];
	
    for(cur_idx_div in considered_divs){
      cur_menu_id = considered_divs[cur_idx_div];
      if(cur_menu_id != null){
        return(cur_menu_id);
    }}
	
	return(null);
  }
  
  /**
   *
   */
  modelplus.main.get_displayed_evaluation = function(){
    var div_id;
	div_id = modelplus.ids.MENU_MODEL_EVAL_SELEC_DIV;
    return(modelplus.main.get_selected_in_div(div_id));
  }
  
  /**
   *
   */
  modelplus.main.get_clicked_about_label = function(about_obj){
    var the_label, the_parent, the_a;
    the_parent = about_obj.parent();
    the_a = the_parent.children('a');
    the_label = the_a.html();
    return(the_label);
  }
  
})();
