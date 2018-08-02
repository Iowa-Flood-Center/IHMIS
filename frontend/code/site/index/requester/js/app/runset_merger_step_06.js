var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  var STATE_NUM = 6;
  var sm = modelplus.requester.state_machine;
  var g_ids = modelplus.requester.constant.id;
  var s_ids = modelplus.model_requester.constant.id;
  
  sm.get_form_info_functions = sm.get_form_info_functions || {};
  
  // define get form functions
  (function () {
   sm.get_form_info_functions[STATE_NUM] = function(){
    var ids = modelplus.requester.constant.id;
    
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
      modelplus.requester.form.highlight_div(s_ids.CONTACT_INFO_DIV);
      $("#"+g_ids.BUTTON_NEXT_STEP).show();
	  $("#"+g_ids.BUTTON_SUBMIT).hide();
    }
  })();

})();