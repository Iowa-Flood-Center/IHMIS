var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  const state_num = 1;
  var sm = modelplus.requester.state_machine;
  var g_ids = modelplus.requester.constant.id;
  var s_ids = modelplus.model_requester.constant.id;
  
  // define get form functions
  (function () {
    sm.get_form_info_functions = sm.get_form_info_functions || {};
  
    sm.get_form_info_functions[state_num] = function(){
      
      // interface function 1
      var lock_fields = function(){
        return ( new Promise( function(resolve, reject){
          $("#"+s_ids.RUNSET_NAME_INPUT).prop('disabled', true);
          $("#"+g_ids.RUNSET_MID_DATE_INPUT).prop('disabled', true);
          sm.next_step_loading();
          resolve(true);
        }));
      };

      // interface function 2
      var check_fields = function(){
        return ( new Promise( function(resolve, reject){
          var runset_id = $("#"+g_ids.RUNSET_NAME_INPUT+" option:selected").attr("id");
          if(runset_id.trim() == ""){
            sm.next_step_error_show("Must select a Runset.");
            unlock_fields();
			resolve(false);
          } else {
            solve(runset_id)
              .then(unlock_fields);
			resolve(false);
          }
        }));
      };

      // interface function 3
      var solve = function(runset_id){
        var solved = true;  // TODO - do it properly
        if(solved){
          sm.post_dict["runset_id"] = runset_id;
        }
      
        return ( new Promise( function(resolve, reject){
          resolve(solved);
        }));
      };

      // interface function 4
      var unlock_fields = function(go_next){
        $("#"+g_ids.RUNSET_NAME_INPUT).prop('disabled', false);
        $("#"+g_ids.RUNSET_MID_DATE_INPUT).prop('disabled', false);
        sm.next_step_button();
        if(go_next){
          $("#"+g_ids.RUNSET_BASIC_HR).hide();
          $("#"+g_ids.RUNSET_NAME_SPAN).html(sm.post_dict["runset_title"]);
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
      update_runset_select_box_content();
      $("#"+s_ids.RUNSET_INFO_DIV).hide();
      $("#"+g_ids.RUNSET_NAME_SPAN).html("");
      $("#"+g_ids.RUNSET_NAME_INPUT).show();
      $("#"+g_ids.RUNSET_BASIC_HR).show();
      $("#"+s_ids.RUNSET_CHOICE_DIV).find(".help_button").show();
      modelplus.requester.form.highlight_div(s_ids.RUNSET_CHOICE_DIV);
      $("#"+g_ids.RUNSET_MID_DATE_INPUT).show();
      hide_date_mid_span();
      $("#"+g_ids.SIMULATION_TYPE_DIV).hide();
      $("#"+g_ids.CONTACT_INFO_DIV).hide();
      $("#"+g_ids.BUTTON_PREV_STEP).hide();
      $("#"+g_ids.BUTTON_NEXT_STEP).show();
      $("#"+g_ids.BUTTON_SUBMIT).hide();
    }
  })();
  
  // --------------------------------------------------------- EXT ----------------------------------------------------------- //
  
  // load Runset select box if needed
  function update_runset_select_box_content(){
    var select_options = $("#"+s_ids.RUNSET_CHOICE_INPUT + " option");
    if (select_options.length <= 1){
      if(select_options.html() != modelplus.model_requester.constant.labels.LOADING){ return; }
    } else return;
    
    modelplus.api.get_runset_results()
      .then(function(data){
        var sel_dom = $("#"+s_ids.RUNSET_CHOICE_INPUT);
        sel_dom.empty();
        data.forEach(function(cur_elem){
          if(cur_elem.id == modelplus.constant.realtime_runset_id) return;
          var cur_dom = $("<option >");
          cur_dom.html(cur_elem.title);
          cur_dom.attr("id", cur_elem.id);
          sel_dom.append(cur_dom);
        })
    });
  }
  
  //
  function hide_date_mid_span(){
    $("#"+modelplus.requester.constant.id.RUNSET_MID_DATE_SPAN).html("");
  }

})();
