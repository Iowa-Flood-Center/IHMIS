var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  var STATE_NUM = 8;
  var sm = modelplus.requester.state_machine;
  var ids = modelplus.requester.constant.id;
  
  // define get form functions
  (function () {
    sm.get_form_info_functions[STATE_NUM] = function(){
    sm.get_form_info_functions = sm.get_form_info_functions || {};
    
    // interface function 1
    var lock_fields = function(){
	  return ( new Promise( function(resolve, reject){
        resolve(true);
      }));
    }

    // interface function 2
    var check_fields = function(){
      return ( new Promise( function(resolve, reject){
        var selected_obj = $("input[name='"+ids.WHAT_DO_RADIO_NAME+"']:checked");
		if (selected_obj.length === 0){
          sm.next_step_error_show("Need to select one action.");
          resolve(false);
		} else {
		  resolve(true);
		}
      }));
    }

    // interface function 3
    var solve = function(solved){
      // TODO - check if at least one option was defined
      return ( new Promise( function(resolve, reject){
        if(solved){
          sm.post_dict['what_do'] = $("input[name='"+ids.WHAT_DO_RADIO_NAME+"']:checked").val();
		}
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
	
    sm.update_form_functions[STATE_NUM] = function(){
      hide_what_do_span();
      modelplus.requester.form.highlight_div(ids.WHAT_DO_DIV);
      $("#"+ids.WHAT_DO_RADIOS_DIV).show();
	  $("#"+ids.WHAT_DO_LABEL).hide();
      $("#"+ids.CONTACT_INFO_DIV).hide();
      $("#"+ids.HOWCONTACT_RADIOS_DIV).hide();
      show_compositions_list_span();
	}
  })();

  // --------------------------------------------------------- EXT ----------------------------------------------------------- //
  
  // 
  function hide_what_do_span(){
    $("#"+modelplus.requester.constant.id.WHAT_DO_SPAN).hide();
	$("#"+modelplus.requester.constant.id.WHAT_DO_SPAN).hide();
	$("#"+modelplus.requester.constant.id.WHAT_DO_H2).show();
  }
  
  // 
  function show_compositions_list_span(){
    $("#"+ids.SET_MODELS_COMPOS_NAMES).html("No compositions.");  // TODO - dynamic
    $("#"+ids.SET_MODELS_COMPOS_LABEL).show();
    $("#"+ids.SET_MODELS_COMPOS_NAMES).show();
	$("#"+ids.SET_MODELS_COMPOS_H2).hide();
  }
  
})();