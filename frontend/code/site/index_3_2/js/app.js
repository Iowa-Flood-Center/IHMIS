$(document).foundation()

var modelplus = modelplus || {};

(function () {
  "use strict";

  modelplus.requester = modelplus.requester || {};
  modelplus.utils = modelplus.utils || {};            // TODO - this should not be here

  // define Requester State Machine
  modelplus.requester.state_machine = modelplus.requester.state_machine || {};

  // define Requester State Machine attributes
  modelplus.requester.state_machine.current_state = 1;
  modelplus.requester.state_machine.post_dict = {};

  // TODO - MOVE TO UTILS
  modelplus.utils.datestr_to_timestamp = function(date_str){
    if (date_str.length != 10)
      return(null);
    var mid_year = date_str.substring(6,10);
	var mid_month = date_str.substring(0,2);
	var mid_day = date_str.substring(3,5);
	return (modelplus.utils.get_timestamp(mid_day, mid_month, mid_year));
  }
  
  // TODO - MOVE TO UTILS
  modelplus.utils.get_timestamp = function(day, month, year){
    var date_obj = new Date(Date.UTC(year, month, day, 0, 0, 0));
	date_obj.setUTCHours(date_obj.getUTCHours() + 5);
	return (date_obj.getTime() / 1000);
  }
  
  // --------------------------------------------------------- GET ----------------------------------------------------------- //
  
  // define Requester State Machine methods
  modelplus.requester.state_machine.get_form_info = function(){
    var sm = modelplus.requester.state_machine;
    var cur_state = sm.current_state;
    var all_funcs = sm.get_form_info_functions;
    var num_states = all_funcs.length;
	
	// update label
    $("#"+modelplus.requester.constant.id.LABEL_NEXT_STEP).html(cur_state + "/" + Object.keys(all_funcs).length);
	
    return ((cur_state in all_funcs) ? all_funcs[cur_state]() : false);
  }
  
  // ------------------------------------------------------------------------------------------------------------------------- //

  /**
   * Get the acronyms of all selected items in a div.
   * RETURN: Array of strings
   */
  modelplus.requester.get_checked_acronyms = function(parent_div_id){
    "use strict";

    var cur_all_checkbox, cur_all_checked, cur_checkbox_idx, cur_checkbox;
	
	cur_all_checkbox = $("#"+parent_div_id+" :input");
    cur_all_checked = Array();
    for(cur_checkbox_idx in cur_all_checkbox){
      cur_checkbox = cur_all_checkbox[cur_checkbox_idx];
      if(cur_checkbox.checked){
        cur_all_checked.push(cur_checkbox.id.split("_").pop());
      }
    }
	return(cur_all_checked);
  };
  
  // pop up with all information from a model
  modelplus.requester.show_model_details = function(a_obj){
    var sm = modelplus.requester.state_machine;
    var cur_id, cur_i, cur_value;
    var mdl_num = $(a_obj).attr("id").split('_').pop();
	var ret_html = "";
    
	// show title, id and HLM model
	ret_html += "Title: " + sm.post_dict["model_title_"+mdl_num];
	ret_html += "\n";
	ret_html += "ID: " + sm.post_dict["model_id_"+mdl_num];
	ret_html += "\n";
	ret_html += "HLM model: " + sm.post_dict["hillslope_model_"+mdl_num];
	ret_html += "\n";
	
	// show forcings
	ret_html += "Forcings: ";
	cur_i = 1;
	while(true){
      cur_id = "model_for_" + mdl_num + "_" + cur_i;
      if (!(cur_id in sm.post_dict)){ break; }
	  ret_html += sm.post_dict[cur_id] + "  ";
	  cur_i += 1;
	}
	ret_html += "\n";
	
	// show global parameters
	ret_html += "Global parameters: ";
	cur_i = 1;
	while(true){
      cur_id = "model_par_" + mdl_num + "_" + cur_i;
      if (!(cur_id in sm.post_dict)){ break; }
	  ret_html += sm.post_dict[cur_id] + "  ";
	  cur_i += 1;
	}
	ret_html += "\n";
	
	// show evaluations
	ret_html += "Evaluations: ";
	cur_id = "model_eval_" + mdl_num;
	if(sm.post_dict[cur_id].length > 0)
		ret_html += sm.post_dict[cur_id].join(", ");
	else
		ret_html += "None";
	ret_html += "\n";
	
	// show representations
	ret_html += "Representations: ";
	ret_html += "TODO";
	ret_html += "\n";
	
	alert(ret_html);
  }
  
  modelplus.requester.form = modelplus.requester.form || {};
  
  // 
  modelplus.requester.form.highlight_div = function(div_id){
    $("."+modelplus.requester.constant.classes.FILLING_FORM).each(function(){
      $(this).removeClass(modelplus.requester.constant.classes.FILLING_FORM);
	});
	if(div_id == null) return;
	
	$("#"+modelplus.requester.constant.id.LABEL_NEXT_STEP_ERROR).hide();
	var div_dom = $("#"+div_id);
	$(".help_button").hide();
	div_dom.find(".help_button").show();
	div_dom.show();
    div_dom.addClass(modelplus.requester.constant.classes.FILLING_FORM);
  }
  
  // 
  modelplus.requester.state_machine.update_form = function(){
    var ids = modelplus.requester.constant.id;
	var sm = modelplus.requester.state_machine;
    if (sm.current_state in sm.update_form_functions){
      sm.update_form_functions[sm.current_state]();
	} else {
      alert("Unexpected state: " + sm.current_state);
	  alert("Valid states: " + JSON.stringify(Object.keys(sm.update_form_functions)));
	}
  }

  //
  modelplus.requester.state_machine.update_steps_label = function(){
	var sm = modelplus.requester.state_machine;
    var cur_state = sm.current_state;
	var all_funcs = sm.get_form_info_functions;
	var steps_label = cur_state + "/" + Object.keys(all_funcs).length;
	$("#"+modelplus.requester.constant.id.LABEL_NEXT_STEP).html(steps_label);
  }
  
  //
  modelplus.requester.state_machine.prev_step = function(){
    var sm = modelplus.requester.state_machine;
    sm.current_state -= 1;
    sm.update_form();
	sm.update_steps_label();
	$("#"+ids.LABEL_NEXT_STEP_ERROR).hide();
  }

  // 
  modelplus.requester.state_machine.next_step_error_show = function(msg){
    var lab_id = modelplus.requester.constant.id.LABEL_NEXT_STEP_ERROR;
	$("#"+lab_id).html(msg);
	$("#"+lab_id).css("display", "block");
  }
  
  // 
  modelplus.requester.state_machine.next_step_error_hide = function(){
    var lab_id = modelplus.requester.constant.id.LABEL_NEXT_STEP_ERROR;
	$("#"+lab_id).html("");
	$("#"+lab_id).css("display", "none");
  }
  
  // 
  modelplus.requester.state_machine.next_step_loading = function(){
    var but_id = modelplus.requester.constant.id.BUTTON_NEXT_STEP;
	var msg = "...loading...";   // TODO - constants
    $("#"+but_id).html(msg);
	$("#"+but_id).on("click", null);
  }
  
  // 
  modelplus.requester.state_machine.next_step_button = function(){
    var but_id = modelplus.requester.constant.id.BUTTON_NEXT_STEP;
    var msg = "Next step";   // TODO - constants
    $("#"+but_id).html(msg);
    // $("#"+but_id).on("click", modelplus.requester.state_machine.submit);
  }
  
  // function called by clicking the button
  modelplus.requester.state_machine.next_step_click = function(){
    var sm = modelplus.requester.state_machine;
	sm.next_step_error_hide();
    sm.get_form_info()
	  .then(function(resolved){
        if (!resolved) return;
        modelplus.requester.state_machine.next_step_go();
	  })
  }
  
  // function called when next step is good to go
  modelplus.requester.state_machine.next_step_go = function(){
    var sm = modelplus.requester.state_machine;
    sm.next_step_error_hide();
    sm.current_state += 1;
    sm.update_form();
	sm.update_steps_label();
	$(".help_message").hide();
  }
  
  // 
  modelplus.requester.state_machine.submit = function(){
    modelplus.api.get_auto_runset_id()
      .then(function(runset_id){
        var sm = modelplus.requester.state_machine;
        var ids = modelplus.requester.constant.id;
        sm.post_dict["sandbox"] = modelplus.url.is_sandbox;
		sm.post_dict["runset_id"] = runset_id;
		sm.post_dict["num_models"] = modelplus.requester.model_count;
		sm.post_dict["asynch_ver"] = "1.3";                   // TODO - move to constants
		sm.post_dict["server_addr"] = "argon.hpc.uiowa.edu";  // TODO - move to constants
        modelplus.api.request_new_runset(sm.post_dict)
          .done(sm.submit_post)
	  });
  }
  
  // 
  modelplus.requester.state_machine.submit_post = function(submit_response){
    const fail_label = modelplus.requester.constant.labels.SUBMIT_FAILURE;
	var ids = modelplus.requester.constant.id;
    var data_dict = JSON.parse(submit_response);
    if(fail_label in data_dict){
      $("#"+ids.SUBMIT_SUCCESS_DIV).hide();
      $("#"+ids.SUBMIT_FAILURE_DIV).show();
      $("#"+ids.SUBMIT_FAILURE_MSG_DIV).html(data_dict[fail_label]);
      $("#"+ids.SUBMIT_FAILURE_DIV).show();
    } else {
      $("#"+ids.SUBMIT_SUCCESS_DIV).show();
      $("#"+ids.SUBMIT_FAILURE_DIV).hide();
	  //$("#"+ids.BUTTONS_DIV).hide();
    }
  }
  
  //
  modelplus.requester.onload = function(){
    modelplus.requester.state_machine.update_form();
    $("#" + modelplus.requester.constant.id.RUNSET_MID_DATE_INPUT).datepicker();
	modelplus.requester.load_predef_mid_date_doms();
	modelplus.requester.load_helps();
  }
  
  //
  modelplus.requester.show_help = function(){
    var help_dom = $(this).parent().parent().find(".help_message");
    var must_show = (help_dom.css("display") == "none" ? true : false);
    $(".help_message").hide();
    if(must_show) help_dom.show();
  }
  
  // ------------------------------------------------------------------ LOAD ------------------------------------------------- //
  
  // 
  modelplus.requester.load_helps = function(){
	$(".help_button").click(modelplus.requester.show_help);
  }
  
  // 
  modelplus.requester.load_predef_mid_date_doms = function(){
    var sub_htmls = [];
	
    modelplus.requester.constant.predefined_mid_dates.forEach(function(predef_date){
      var sub_html = "";
	  var dom_id = "runset_mid_date_source_" + predef_date.date_str;
	  var dom_val = predef_date.date_str;
	  var dom_lbl = predef_date.label;
	  var date_str = predef_date.date_str.substring(4,6) + '/' + predef_date.date_str.substring(6,8) + '/';
	  date_str += predef_date.date_str.substring(0,4);
	  var mid_id = modelplus.requester.constant.id.RUNSET_MID_DATE_INPUT;
      var dom_clk = "$('#"+mid_id+"').val('"+date_str+"');";
      sub_html = '<input type="radio" name="runset_mid_date_source" value="'+dom_val+'" id="'+dom_id+'" onchange="'+dom_clk+'">\
                  <label for="'+dom_id+'">'+dom_lbl+'</label>';
	  sub_htmls.push(sub_html);
    });
	$("#"+modelplus.requester.constant.id.RUNSET_MID_DATE_PREDEF_DIV).html(sub_htmls.join('<br>'));
  }
  
  // ------------------------------------------------------------------- SM -------------------------------------------------- //
  
  //
  modelplus.requester.state_machine.get_num_models = function(){
    var sm = modelplus.requester.state_machine;
	var cur_mdl_index;
	var return_num_models = 0;
	for(cur_mdl_index = 1; cur_mdl_index <= modelplus.requester.model_count; cur_mdl_index++){
      if(sm.post_dict["model_title_"+cur_mdl_index] === "undefined") continue;
      else return_num_models += 1;
    }
    return(return_num_models);
  }
  
  // 
  modelplus.requester.state_machine.get_hlm_model = function(model_id){
    var sm = modelplus.requester.state_machine;
    var cur_mdl_index;
    for(cur_mdl_index = 1; cur_mdl_index <= modelplus.requester.model_count; cur_mdl_index++){
      if(sm.post_dict["model_title_"+cur_mdl_index] === "undefined") continue;
	  if(sm.post_dict["model_id_"+cur_mdl_index] != model_id) continue;
	  return(sm.post_dict["hillslope_model_"+cur_mdl_index]);
	}
  }
  

})();
