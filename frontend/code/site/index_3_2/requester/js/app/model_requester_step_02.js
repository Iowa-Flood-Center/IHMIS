var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  const state_num = 2;
  var sm = modelplus.requester.state_machine;
  var g_ids = modelplus.requester.constant.id;
  var s_ids = modelplus.model_requester.constant.id;
  
  (function () {
  
   sm.get_form_info_functions = sm.get_form_info_functions || {};
  
   sm.get_form_info_functions[state_num] = function(){
    
    // interface function 1
    var lock_fields = function(){
      return ( new Promise( function(resolve, reject){
        $("#"+g_ids.SIMULATION_TYPE_DIV).find('*').each(function(){
          $(this).prop('disabled', true);
        });
        sm.next_step_loading();
        resolve(true);
      }));
    };

    // interface function 2
    var check_fields = function(){
      return ( new Promise( function(resolve, reject){
        var selected = $("input[name='"+g_ids.WHATRUN_RADIO_NAME+"']:checked");
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
      $("#"+g_ids.SIMULATION_TYPE_DIV).find('*').each(function(){
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

      modelplus.api.get_runset_result(sm.post_dict["runset_id"])
        .then(display_runset_info)
        .then(modelplus.model_requester.get_available_hlm);

      $("#"+s_ids.RUNSET_CHOICE_DIV).hide();
      show_date_mid_span();
      hide_date_iniend_span();
      modelplus.requester.form.highlight_div(s_ids.SET_MODELS_DIV);
      $("#"+s_ids.SET_MODELS_DIV).show();
      $("#"+g_ids.CONTACT_INFO_DIV).hide();
      $("#"+g_ids.BUTTON_PREV_STEP).show();
      $("#"+g_ids.BUTTON_NEXT_STEP).show();
      $("#"+g_ids.BUTTON_SUBMIT).hide();
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
  function display_runset_info(runset_info){
    sm.post_dict["timestamp_ini"] = runset_info[0].timestamp_ini;  // TODO - store somewhere else
    sm.post_dict["timestamp_end"] = runset_info[0].timestamp_end;  // TODO - store somewhere else
    sm.post_dict["reference_ids"] = runset_info[0].sc_reference;   // TODO - store somewhere else
    $("#"+s_ids.RUNSET_INFO_LABEL_SPAN).html(" " + runset_info[0].title);
    $("#"+s_ids.RUNSET_INFO_INTER_SPAN).html(" " + runset_info[0].timestamp_ini + " to " + runset_info[0].timestamp_end);
    $("#"+s_ids.RUNSET_INFO_MODEL_SPAN).html(" " + runset_info[0].sc_model.length + " model(s).");
    $("#"+s_ids.RUNSET_INFO_REFER_SPAN).html(" " + runset_info[0].sc_reference.length + " reference(s).");
    $("#"+s_ids.RUNSET_INFO_DIV).show();
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
    var what_run = $("input[name='"+g_ids.WHATRUN_RADIO_NAME+"']:checked").val();
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
