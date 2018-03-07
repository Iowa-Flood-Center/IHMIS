var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  var STATE_NUM = 2;
  var sm = modelplus.requester.state_machine;
  var g_ids = modelplus.requester.constant.id;
  var s_ids = modelplus.model_requester.constant.id;
  
  (function () {
  
   sm.get_form_info_functions = sm.get_form_info_functions || {};
  
   sm.get_form_info_functions[STATE_NUM] = function(){
    
    // interface function 1
    var lock_fields = function(){
      return ( new Promise( function(resolve, reject){
        
        $("#"+s_ids.REFERENCES_COPY_DIV).find('*').each(function(){
          $(this).prop('disabled', true);
        });
        sm.next_step_loading();
        resolve(true);
      }));
    };

    // interface function 2
    var check_fields = function(){
      return ( new Promise( function(resolve, reject){
        // TODO - do it properly
        /*
        var selected = $("input[name='"+g_ids.WHATRUN_RADIO_NAME+"']:checked");
        if (selected.length === 0){
          sm.next_step_error_show("Invalid flood peak date.");
          resolve(false);
        } else {
          resolve(true);
        }
        */
        resolve(true);
      }));
    };

    // interface function 3
    var solve = function(solved){
      // TODO - add to post_dict
      return ( new Promise( function(resolve, reject){
        resolve(solved);
      }));
    };

    // interface function 4
    var unlock_fields = function(go_next){
      $("#"+s_ids.REFERENCES_COPY_DIV).find('*').each(function(){
        $(this).prop('disabled', false);
      });
      sm.next_step_button();
      if(go_next){
        $("#"+s_ids.REFERENCES_COPY_SPAN).html("None");  // TODO it
        modelplus.requester.state_machine.next_step_go();
      }
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
    
    sm.update_form_functions[STATE_NUM] = function(){

      modelplus.api.get_runset_result(sm.post_dict["from_runset_id"])
        .then(build_references_options);

      $("#"+s_ids.RUNSET_CHOICE_DIV).hide();
      $("#"+s_ids.COPY_MODELS_ADDED_DIV).empty();
      modelplus.requester.form.highlight_div(s_ids.REFERENCES_COPY_DIV);
      $("#"+s_ids.SET_MODELS_DIV).hide();
      
      $("#"+s_ids.REFERENCES_COPY_DIV).show();
      
      $("#"+g_ids.BUTTON_PREV_STEP).show();
    }
  })();
  
  // --------------------------------------------------------- EXT ----------------------------------------------------------- //
  
  //
  modelplus.model_requester.add_new_model = function(){
    modelplus.requester.model_count += 1;
    modelplus.requester.add_new_model(s_ids.SET_MODELS_ADDED_DIV, 
                                      modelplus.requester.model_count,
                                      sm.available_hlm);
  }
  
  //
  modelplus.model_requester.get_available_hlm = function(){
    modelplus.api.get_hlm_options(sm.post_dict["timestamp_ini"], sm.post_dict["timestamp_end"])
      .then(function (aval_hlm){
        sm.available_hlm = aval_hlm;
        $("#"+s_ids.SET_MODELS_ADD_DIV).show();
      });
  }
 
  //
  function build_references_options(){
    console.log("TODO: build_references_options");
  }

})();
