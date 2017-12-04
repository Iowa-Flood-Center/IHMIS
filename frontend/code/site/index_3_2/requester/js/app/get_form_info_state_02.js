var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  const state_num = 2;
  var sm = modelplus.requester.state_machine;
  var ids = modelplus.requester.constant.id;
  
  (function () {
  
   sm.get_form_info_functions = sm.get_form_info_functions || {};
  
   sm.get_form_info_functions[state_num] = function(){
    var sm = modelplus.requester.state_machine;
    var ids = modelplus.requester.constant.id;
    
    // interface function 1
    var lock_fields = function(){
	  return ( new Promise( function(resolve, reject){
        $("#"+ids.SIMULATION_TYPE_DIV).find('*').each(function(){
          $(this).prop('disabled', true);
        });
        sm.next_step_loading();
        resolve(true);
      }));
    };

    // interface function 2
    var check_fields = function(){
      return ( new Promise( function(resolve, reject){
        var selected = $("input[name='"+ids.WHATRUN_RADIO_NAME+"']:checked");
        if (selected.length === 0){
          sm.next_step_error_show("Invalid flood peak date.");
          resolve(false);
        } else {
          resolve(true);
        }
      }));
    };

    // interface function 3
    var solve = function(solved){
      if(solved) get_what_run();
      return ( new Promise( function(resolve, reject){
        resolve(solved);
      }));
    };

    // interface function 4
    var unlock_fields = function(go_next){
      $("#"+ids.SIMULATION_TYPE_DIV).find('*').each(function(){
        $(this).prop('disabled', false);
      });
      sm.next_step_button();
      if(go_next) modelplus.requester.state_machine.next_step_go();
    };
    
    return(lock_fields()
      .then(check_fields)
	  .then(solve)
	  .then(unlock_fields));
   };
   
  })();
  
  // define get form functions
  (function () {
    sm.update_form_functions = sm.update_form_functions || {};
	
    sm.update_form_functions[state_num] = function(){
      $("#"+ids.RUNSET_NAME_INPUT).hide();
      $("#"+ids.RUNSET_NAME_SPAN).html(sm.post_dict["runset_name"]);
      $("#"+ids.RUNSET_NAME_SPAN).html(sm.post_dict["runset_name"]);
      $("#"+ids.RUNSET_MID_DATE_INPUT).hide();
      show_date_mid_span();
      hide_date_iniend_span();
      modelplus.requester.form.highlight_div(ids.SIMULATION_TYPE_DIV);
      $("#"+ids.REFERENCES_INCLUDE_DIV).hide();
      $("#"+ids.SET_MODELS_DIV).hide();
      $("#"+ids.SET_MODELS_COMPAR_DIV).hide();
      $("#"+ids.SET_MODELS_COMPOS_DIV).hide();
      $("#"+ids.WHAT_DO_DIV).hide();
      $("#"+ids.CONTACT_INFO_DIV).hide();
      $("#"+ids.BUTTON_PREV_STEP).show();
      $("#"+ids.BUTTON_NEXT_STEP).show();
      $("#"+ids.BUTTON_SUBMIT).hide();
	}
  })();
  
  // --------------------------------------------------------- EXT ----------------------------------------------------------- //

  //
  function show_date_mid_span(){
    var date_obj = new Date(modelplus.requester.state_machine.post_dict["timestamp_mid"] * 1000);
    var month = date_obj.getMonth() + 1;
	var day = date_obj.getDate();
	var year = date_obj.getFullYear();
	var date_str = month + "/" + day + "/" + year;
    $("#"+modelplus.requester.constant.id.RUNSET_MID_DATE_SPAN).html(date_str);
  }
  
  //
  function get_what_run(){
    var sm = modelplus.requester.state_machine;
	var ids = modelplus.requester.constant.id;
    var what_run = $("input[name='"+ids.WHATRUN_RADIO_NAME+"']:checked").val();
	sm.post_dict["what_run"] = what_run;
	var timestamp_mid = sm.post_dict["timestamp_mid"];
    switch(what_run){
      case "what_run_20dseq":
	  case "what_run_10dp10df":
        sm.post_dict["timestamp_ini"] = timestamp_mid - (10 * 24 * 60 * 60);
        sm.post_dict["timestamp_end"] = timestamp_mid + (10 * 24 * 60 * 60);
	    break;
      case "what_run_06hseq":
        sm.post_dict["timestamp_ini"] = timestamp_mid - (3 * 24 * 60 * 60);
        sm.post_dict["timestamp_end"] = timestamp_mid + (3 * 24 * 60 * 60);
	    break;
      case "what_run_06hp06hf":
        sm.post_dict["timestamp_ini"] = timestamp_mid - (3 * 24 * 60 * 60);
        sm.post_dict["timestamp_end"] = timestamp_mid + (3 * 24 * 60 * 60);
	    break;
	}
  }
  
  //
  function hide_date_iniend_span(){
    $("#"+modelplus.requester.constant.id.RUNSET_INIEND_DATE_SPAN).html("");
  }

})();