var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  const state_num = 1;
  var sm = modelplus.requester.state_machine;
  var ids = modelplus.requester.constant.id;
  
  // define get form functions
  (function () {
    sm.get_form_info_functions = sm.get_form_info_functions || {};
  
    sm.get_form_info_functions[state_num] = function(){
      
      // interface function 1
      var lock_fields = function(){
        return ( new Promise( function(resolve, reject){
          $("#"+ids.RUNSET_NAME_INPUT).prop('disabled', true);
          $("#"+ids.RUNSET_MID_DATE_INPUT).prop('disabled', true);
          sm.next_step_loading();
          resolve(true);
        }));
      };

      // interface function 2
      var check_fields = function(){
        return ( new Promise( function(resolve, reject){
          var url = "http://s-iihr50.iihr.uiowa.edu/andre/tests/foundation-6.4.2-complete/php/mock_5sec.php"; // TODO - replace
          if($("#"+ids.RUNSET_NAME_INPUT).val().trim() == ""){
            sm.next_step_error_show("Runset name is empty.");
            unlock_fields();
          } else if ($("#"+ids.RUNSET_MID_DATE_INPUT).val().trim() == "") {
      	sm.next_step_error_show("Flood peak date is empty.");
            unlock_fields();
        } else if (!$("#"+ids.RUNSET_MID_DATE_INPUT).val().match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/)) {
      	sm.next_step_error_show("Invalid flood peak date.");
            unlock_fields();
          } else {
			modelplus.api.get_runset_result_with_title($("#"+ids.RUNSET_NAME_INPUT).val())
			  .then(solve)
			  .then(unlock_fields);
          }
        }));
      };

      // interface function 3
      var solve = function(data){
        var solved;
		
		if(data.length > 0){
          solved = false;
		} else {
		  solved = true;
          sm.post_dict["runset_title"] = $("#"+ids.RUNSET_NAME_INPUT).val();
          var date_val = $("#"+ids.RUNSET_MID_DATE_INPUT).val();
          sm.post_dict["timestamp_mid"] = modelplus.util.datestr_to_timestamp(date_val);
        }
      
        return ( new Promise( function(resolve, reject){
          resolve(solved);
        }));
      };

      // interface function 4
      var unlock_fields = function(go_next){
        $("#"+ids.RUNSET_NAME_INPUT).prop('disabled', false);
        $("#"+ids.RUNSET_MID_DATE_INPUT).prop('disabled', false);
        sm.next_step_button();
        if(go_next){
          $("#"+ids.RUNSET_BASIC_HR).hide();
		  $("#"+ids.RUNSET_NAME_SPAN).html(sm.post_dict["runset_title"]);
		  modelplus.requester.state_machine.next_step_go();
		}
      };
    
      return(lock_fields()
        .then(check_fields));
    };
  })();
  
  // define get form functions
  (function () {
    sm.update_form_functions = sm.update_form_functions || {};
	
    sm.update_form_functions[state_num] = function(){
      $("#"+ids.RUNSET_NAME_SPAN).html("");
      $("#"+ids.RUNSET_NAME_INPUT).show();
	  $("#"+ids.RUNSET_BASIC_HR).show();
      $("#"+ids.RUNSET_NAME_DIV).find(".help_button").show();
      modelplus.requester.form.highlight_div(ids.RUNSET_NAME_DIV);
      $("#"+ids.RUNSET_MID_DATE_INPUT).show();
      hide_date_mid_span();
      $("#"+ids.SIMULATION_TYPE_DIV).hide();
      $("#"+ids.CONTACT_INFO_DIV).hide();
      $("#"+ids.BUTTON_PREV_STEP).hide();
      $("#"+ids.BUTTON_NEXT_STEP).show();
      $("#"+ids.BUTTON_SUBMIT).hide();
	}
  })();
  
  // --------------------------------------------------------- EXT ----------------------------------------------------------- //
  
  //
  function hide_date_mid_span(){
    $("#"+modelplus.requester.constant.id.RUNSET_MID_DATE_SPAN).html("");
  }

})();