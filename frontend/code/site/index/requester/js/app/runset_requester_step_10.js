var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  var STATE_NUM = 10;
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
        resolve(true);
      }));
    }

    // interface function 3
    var solve = function(solved){
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
	
	sm.update_form_functions[STATE_NUM] = function(){
      show_contact_span();
      $("#"+ids.CONTACT_INFO_DIV).show();
      $("#"+ids.HOWCONTACT_RADIOS_DIV).hide();
      modelplus.requester.form.highlight_div(null);
      $("#"+ids.BUTTON_PREV_STEP).show();
      $("#"+ids.BUTTON_NEXT_STEP).hide();
      $("#"+ids.BUTTON_SUBMIT).show();
    }
  })();
  
  // --------------------------------------------------------- EXT ----------------------------------------------------------- //
  
  // 
  function show_contact_span(){
    var msg;
	$("#" + ids.HOWCONTACT_TITLE).hide();
    $("#" + ids.HOWCONTACT_LABEL).show();
	var email_add = sm.post_dict['email'];
	var span_obj = $("#"+ids.HOWCONTACT_SPAN);
    switch(sm.post_dict['contact_option']){
      case "how_contact_none":
        span_obj.html("No contact.");
	    break;
      case "how_contact_onfinish":
        span_obj.html("Email on finish for '"+sm.post_dict['email']+"'.");
        break;
      case "how_contact_all":
        span_obj.html("Emails for '"+sm.post_dict['email']+"'.");
        break;
      default:
	    console.log("Unexpected value: " + sm.post_dict['contact_option']);
    }
	span_obj.show();
  }

})();