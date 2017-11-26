var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  const state_num = 3;
  var sm = modelplus.requester.state_machine;
  var ids = modelplus.requester.constant.id;
  
  // define get form functions
  (function () {
   sm.get_form_info_functions = sm.get_form_info_functions || {};
   sm.get_form_info_functions[state_num] = function(){
    var sm = modelplus.requester.state_machine;
    var ids = modelplus.requester.constant.id;
    
    // interface function 1
    var lock_fields = function(){
      $("#"+ids.REFERENCES_INCLUDE_DIV).find('*').each(function(){
        $(this).prop('disabled', true);
      });
      return ( new Promise( function(resolve, reject){
        resolve(true);
      }));
    };

    // interface function 2
    var check_fields = function(){
      return ( new Promise( function(resolve, reject){
        resolve(true);  // nothing to check
      }));
    };

    // interface function 3
    var solve = function(solved){
      if (solved){
        var selected_refs = modelplus.requester.get_checked_acronyms(ids.REFERENCES_INCLUDE_LIST_DIV);
		sm.post_dict["reference_ids"] = selected_refs;  // TODO - check if it is what is expected in the web service
      }
      
      return ( new Promise( function(resolve, reject){
        resolve(solved);
      }));
    };

    // interface function 4
    var unlock_fields = function(go_next){
      $("#"+ids.REFERENCES_INCLUDE_DIV).find('*').each(function(){
        $(this).prop('disabled', false);
      });
      sm.next_step_button();
      if(go_next) modelplus.requester.state_machine.next_step_go();
    };
    
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
      $("#"+ids.RUNSET_NAME_INPUT).hide();
      $("#"+ids.RUNSET_NAME_SPAN).html(sm.post_dict["runset_name"]);
      $("#"+ids.RUNSET_MID_DATE_INPUT).hide();
      show_date_iniend_span();
      $("#"+ids.SIMULATION_TYPE_DIV).hide();
      modelplus.requester.form.highlight_div(ids.REFERENCES_INCLUDE_DIV);
      $("#"+ids.SET_MODELS_DIV).hide();
      $("#"+ids.SET_MODELS_COMPAR_DIV).hide();
      $("#"+ids.SET_MODELS_COMPOS_DIV).hide();
      $("#"+ids.WHAT_DO_DIV).hide();
	  $("#"+ids.SET_MODELS_ADDED_DIV).empty();
      $("#"+ids.CONTACT_INFO_DIV).hide();
      $("#"+ids.BUTTON_SUBMIT).hide();
	  hide_reference_list_span();
	  
	  load_references_ws()
	    .then(build_references_menu);
		/*
	    .then(function(){
          $("#"+ids.BUTTON_PREV_STEP).show();
          $("#"+ids.BUTTON_NEXT_STEP).show();
      });*/
	
      modelplus.requester.model_count = 0;
	};
  })();
  
  // --------------------------------------------------------- EXT ----------------------------------------------------------- //
  
  //
  function show_date_iniend_span(){
    var date_ini_obj = new Date(modelplus.requester.state_machine.post_dict["timestamp_ini"] * 1000);
	var date_end_obj = new Date(modelplus.requester.state_machine.post_dict["timestamp_end"] * 1000);
	var date_ini_str = date_ini_obj.getMonth()+"/"+date_ini_obj.getDate()+"/"+date_ini_obj.getFullYear();
	var date_end_str = date_end_obj.getMonth()+"/"+date_end_obj.getDate()+"/"+date_end_obj.getFullYear();
	var date_txt = "(from "+date_ini_str+" to "+date_end_str+")";
    $("#"+modelplus.requester.constant.id.RUNSET_INIEND_DATE_SPAN).html(date_txt);
  }
  
  // call ajax
  function load_references_ws(){
    var div_obj, web_service_url;
    web_service_url = modelplus.url.proxy + modelplus.url.api;
    web_service_url += 'sc_references%i%timeset=historical';
    return ($.getJSON(web_service_url));
  };
  
  // build options
  function build_references_menu(json_obj){
    var cur_idx, div_obj, check_obj;
	var cur_screference, cur_checkbox_id, cur_reprcheck_html;
	
	// clean receiving div
	div_obj = $("#" + ids.REFERENCES_INCLUDE_LIST_DIV);
	// div_obj.empty();
    if (div_obj.html().trim() == ""){

      for(cur_idx in json_obj){
		cur_screference = json_obj[cur_idx];
		cur_checkbox_id = ids.REFERENCES_INCLUDE_ID_PREF;
		cur_checkbox_id = cur_screference["acronym"];
		cur_reprcheck_html = "<input type='checkbox' id='"+cur_checkbox_id+"' \>" +
								"<label for='"+cur_checkbox_id+"'>" + cur_screference["title"] + "</label>" +
								"<br />";
		check_obj = $(cur_reprcheck_html);
		div_obj.append(check_obj);
	  }
	}
	
	return ( new Promise( function(resolve, reject){
      resolve(true);
    }));
  }
  
  // 
  function hide_reference_list_span(){
    $("#" + ids.REFERENCES_INCLUDE_LABEL).hide();
	$("#" + ids.REFERENCES_INCLUDE_NAMES).html("");
	$("#" + ids.REFERENCES_INCLUDE_NAMES).hide();
	$("#" + ids.REFERENCES_INCLUDE_LIST_DIV).show();
	$("#" + ids.REFERENCES_INCLUDE_TITLE).show();
  }
  
})();