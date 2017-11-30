var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  const state_num = 6;
  var sm = modelplus.requester.state_machine;
  var ids = modelplus.requester.constant.id;
  
  // define get form functions
  (function () {
   sm.get_form_info_functions = sm.get_form_info_functions || {};
   sm.get_form_info_functions[state_num] = function(){
    
    // interface function 1
    var lock_fields = function(){
	  return ( new Promise( function(resolve, reject){
        resolve(true);
      }));
    }

    // interface function 2
    var check_fields = function(){
      return ( new Promise( function(resolve, reject){
        resolve(true);
      }));
    }

    // interface function 3
    var solve = function(data){
      var solved = true;  // TODO - do it properly
	  
	  // count comparisons
      for(var key in sm.post_dict){
        if (!(/^comparisons_/.test(key))) continue;
        delete sm.post_dict[key];
      }
	  
	  // iterate over divs
	  $("input:checked[id^=common_representation_]").each(function() {
		var splitted = $(this).attr('id').split("_");
		var post_id = "comparisons_" + splitted[2] + "_" + splitted[3];
		
		if (sm.post_dict[post_id] === "undefined"){
          sm.post_dict[post_id] = splitted[4];
		} else {
          sm.post_dict[post_id] += "," + splitted[4];
		}
      });
      
      return ( new Promise( function(resolve, reject){
        resolve(solved);
      }));
    }

    // interface function 4
    var unlock_fields = function(go_next){
      
      sm.next_step_button();
      if(go_next) modelplus.requester.state_machine.next_step_go();
    }
    
    return(lock_fields()
      .then(check_fields)
	  .then(solve)
      .then(unlock_fields));
   }
  })();
  
  // define get form functions
  (function () {
    sm.update_form_functions = sm.update_form_functions || {};
	
    sm.update_form_functions[state_num] = function(){
	  $("#"+ids.SET_MODELS_REPR_COMBINED_DIV).hide();
	  hide_comparisons_list_span();
      $("#"+ids.SET_MODELS_COMPOS_DIV).hide();
	  $("#"+ids.SET_MODELS_COMPAR_H2).show();
	  build_comparisons_options();
	  $("#"+ids.SET_MODELS_COMPAR_NAMES).show();
      
      modelplus.requester.form.highlight_div(ids.SET_MODELS_COMPAR_DIV);
    }
  })();
  
  // --------------------------------------------------------- EXT ----------------------------------------------------------- //
  
  //
  function hide_comparisons_list_span(){
    $("#"+ids.SET_MODELS_COMPAR_NAMES).html("");
    $("#"+ids.SET_MODELS_COMPAR_LABEL).hide();
  }
  
  //
  function toggle_comparisons(){
    var sm = modelplus.requester.state_machine;
    var splitted_id = $(this).attr('id').split("_");
	var mdl_id_2 = splitted_id.pop();
	var mdl_id_1 = splitted_id.pop();
    var inner_div_id = "comparison_inner_" + mdl_id_1 + "_" + mdl_id_2;
	if($("#" + inner_div_id).html() == ""){
      $("#" + inner_div_id).html("Loading...");
      var mdl_hlm_1 = sm.get_hlm_model(mdl_id_1);
	  var mdl_hlm_2 = sm.get_hlm_model(mdl_id_2);
	  modelplus.api.get_common_representations_for_hlms(mdl_hlm_1, mdl_hlm_2)
	    .then(function(data){
		  fill_representations_div(inner_div_id, mdl_id_1, mdl_id_2, data);
		});
	}
	if($("#" + inner_div_id).css('display')=='none'){
      $("#" + inner_div_id).css('display', 'block');
	  $(this).html("[-]");
	} else {
      $("#" + inner_div_id).css('display', 'none');
	  $(this).html("[+]");
	}
  }
  
  // 
  function fill_representations_div(div_id, mdl_1, mdl_2, json_data){
    var cur_key, cur_obj, cur_label, cur_check, cur_check_id, cur_repr, cur_label, cur_title;
	var div_dom = $("#"+div_id);
	div_dom.empty();
	for(cur_key in json_data){
      cur_obj = json_data[cur_key];
	  cur_repr = cur_obj.acronym;
	  cur_title = cur_obj.title;
      cur_check_id = "common_representation_" + mdl_1 + "_" + mdl_2 + "_" + cur_repr;
	  cur_check = $("<input type='checkbox' id='"+cur_check_id+"' />");
	  cur_label = $("<label for='"+cur_check_id+"'>"+cur_title+"</label>");
	  div_dom.append(cur_check);
	  div_dom.append(cur_label);
	  div_dom.append("<br />");
    }
  }
  
  //
  function build_comparisons_options(){
    var return_html;
	var mdl_idx_1, mdl_idx_2, mdl_title_1, mdl_title_2, cur_div, show_a;
	var mdl_id_1, mdl_id_2, cur_inner_div, cur_inner_div_id;
	var mdl_count = modelplus.requester.model_count;
	
    if(sm.get_num_models() <= 1){
      return_html = "Insufficient number of models. No comparisons possible.";
      $("#"+ids.SET_MODELS_COMPAR_NAMES).html(return_html);
	  return;
	}
	
	// add each pair
    for(mdl_idx_1 = 1; mdl_idx_1 <= mdl_count; mdl_idx_1++){
      for(mdl_idx_2 = 1; mdl_idx_2 <= mdl_count; mdl_idx_2++){
        if (mdl_idx_1 == mdl_idx_2) continue;
		if (sm.post_dict["model_title_"+mdl_idx_1] == "undefined") continue;
		if (sm.post_dict["model_title_"+mdl_idx_2] == "undefined") continue;
		cur_div = $("<div>");
		cur_div.addClass("comparison_def");
		mdl_title_1 = sm.post_dict["model_title_"+mdl_idx_1];
		mdl_title_2 = sm.post_dict["model_title_"+mdl_idx_2];
		cur_div.html(mdl_title_1 + " x " + mdl_title_2);
		
		// add plus button
		mdl_id_1 = sm.post_dict["model_id_"+mdl_idx_1];
		mdl_id_2 = sm.post_dict["model_id_"+mdl_idx_2];
		show_a = $("<a id='toggle_comp_"+mdl_id_1+"_"+mdl_id_2+"' >[+]</a>");
		show_a.click(toggle_comparisons);
        cur_div.append(show_a);
		
		// add inner div
		cur_inner_div_id = "comparison_inner_" + mdl_id_1 + "_" + mdl_id_2;
		cur_inner_div = $("<div>");
		cur_inner_div.attr("id", cur_inner_div_id);
		cur_inner_div.css('display', 'none');
		cur_div.append(cur_inner_div);
		
		$("#"+ids.SET_MODELS_COMPAR_NAMES).append(cur_div);
      }
    }
  }
  
  
  
  

})();