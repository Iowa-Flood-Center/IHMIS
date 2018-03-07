var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  var STATE_NUM = 7;
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
      
      $("#"+ids.SET_MODELS_COMPOS_DIV).show();
      modelplus.requester.form.highlight_div(ids.SET_MODELS_COMPOS_DIV);
	  $("#"+ids.SET_MODELS_COMPOS_NAMES).show();
	  $("#"+ids.SET_MODELS_COMPOS_NAMES).html("UNDER CONSTRUCTION");
      $("#"+ids.WHAT_DO_DIV).hide();
      show_comparisons_list_span();
	}
  })();
  
  // --------------------------------------------------------- EXT ----------------------------------------------------------- //
  
  // 
  function show_comparisons_list_span(){
    var count_comparisons = 0;
	var subcount;
	
	// count comparisons
    for(var key in sm.post_dict){
      if (!(/^comparisons_/.test(key))) continue;
	  subcount = sm.post_dict[key].split(',').length;
      count_comparisons += subcount;
    }
	
	// 
    if (count_comparisons == 0){
      $("#"+ids.SET_MODELS_COMPAR_NAMES).html("No comparisons.");
	} else {
      $("#"+ids.SET_MODELS_COMPAR_NAMES).html(count_comparisons + " comparisons.");
	}
    $("#"+ids.SET_MODELS_COMPAR_LABEL).show();
    $("#"+ids.SET_MODELS_COMPAR_NAMES).show();
	$("#"+ids.SET_MODELS_COMPAR_H2).hide();
  }

})();