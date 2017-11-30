var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  const state_num = 9;
  var sm = modelplus.requester.state_machine;
  var ids = modelplus.requester.constant.id;
  
  // define get form functions
  (function () {
   sm.get_form_info_functions[state_num] = function(){
    sm.get_form_info_functions = sm.get_form_info_functions || {};
    
    // interface function 1
    var lock_fields = function(){
	  return ( new Promise( function(resolve, reject){
        $("#"+ids.CONTACT_INFO_DIV).find('*').each(function(){
          $(this).prop('disabled', true);
        });
        sm.next_step_loading();
        resolve(true);
      }));
    }

    // interface function 2
    var check_fields = function(){
      return ( new Promise( function(resolve, reject){
        var selected_obj = $("input[name='"+ids.HOWCONTACT_RADIO_NAME+"']:checked");
		var contact_email = $("#"+ids.CONTACT_EMAIL_INPUT).val().trim();
		var will_resolve = true;
        if (selected_obj.length === 0){
          sm.next_step_error_show("Need to select one contact option.");
          will_resolve = false;
        } else {
          var selected_val = selected_obj.val();
          if ((selected_val != "how_contact_none")&&(contact_email == "")) {
            sm.next_step_error_show("Need to provide a proper email address.");
            will_resolve = false;
          }
		}
		resolve(will_resolve);
      }));
    }

    // interface function 3
    var solve = function(solved){
      
      return ( new Promise( function(resolve, reject){
		if (solved){
          sm.post_dict['contact_option'] = $("input[name='"+ids.HOWCONTACT_RADIO_NAME+"']:checked").val();
	      sm.post_dict['email'] = $("#"+ids.CONTACT_EMAIL_INPUT).val().trim();
		}
        resolve(solved);
      }));
    }

    // interface function 4
    var unlock_fields = function(go_next){
      $("#"+ids.CONTACT_INFO_DIV).find('*').each(function(){
        $(this).prop('disabled', false);
      });
      sm.next_step_button();
      if(go_next){
        modelplus.requester.state_machine.next_step_go();
        $(".help_button").hide();
      }
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
      $("#"+ids.WHAT_DO_RADIOS_DIV).hide();
	  $("#"+ids.HOWCONTACT_SPAN).hide();
      modelplus.requester.form.highlight_div(ids.CONTACT_INFO_DIV);
      $("#"+ids.HOWCONTACT_RADIOS_DIV).show();
      show_what_do_span();
	  $("#"+ids.BUTTON_PREV_STEP).show();
      $("#"+ids.BUTTON_NEXT_STEP).show();
      $("#"+ids.BUTTON_SUBMIT).hide();
	}
  })();

  // --------------------------------------------------------- EXT ----------------------------------------------------------- //
  
  function show_what_do_span(){
    var what_do_val = modelplus.requester.state_machine.post_dict["what_do"];
	$("#"+modelplus.requester.constant.id.WHAT_DO_H2).hide();
    if(typeof what_do_val == "undefined"){
      $("#"+modelplus.requester.constant.id.WHAT_DO_SPAN).html("UNDEFINED");
	} else {
      $("#"+modelplus.requester.constant.id.WHAT_DO_SPAN).html(what_do_val);
	}
	$("#"+modelplus.requester.constant.id.WHAT_DO_LABEL).show();
	$("#"+modelplus.requester.constant.id.WHAT_DO_SPAN).show();
  }
  
})();