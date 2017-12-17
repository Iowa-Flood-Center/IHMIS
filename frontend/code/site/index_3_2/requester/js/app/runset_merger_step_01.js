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
          $("#"+s_ids.RUNSET_FROM_INPUT).prop('disabled', true);
          $("#"+s_ids.RUNSET_TO_INPUT).prop('disabled', true);
          sm.next_step_loading();
          resolve(true);
        }));
      };

      // interface function 2
      var check_fields = function(){
        return ( new Promise( function(resolve, reject){
          var from_runset_id = $("#"+s_ids.RUNSET_FROM_INPUT+" option:selected").attr("id");
          var to_runset_id = $("#"+s_ids.RUNSET_TO_INPUT+" option:selected").attr("id");
          if((from_runset_id.trim() == "") || (to_runset_id.trim() == "")){
            sm.next_step_error_show("Must select both FROM and TO Runsets.");
            unlock_fields(false);
            resolve(false);
          } else {
			solve(from_runset_id, to_runset_id);
          }
        }));
      };

      // interface function 3
      var solve = function(from_runset_id, to_runset_id){
		sm.post_dict["from_runset_id"] = from_runset_id;
        sm.post_dict["to_runset_id"] = to_runset_id;
        return ( new Promise( function(resolve, reject){
          // TODO - make these calls parallel
          modelplus.api.get_runset_result(from_runset_id)
			.then(function(from_runsets){
			  modelplus.requester.state_machine.auxi_dict["from_runset"] = from_runsets[0];
              return(modelplus.api.get_runset_result(to_runset_id));
			})
			.then(function(to_runsets){
			  modelplus.requester.state_machine.auxi_dict["to_runset"] = to_runsets[0];
			  resolve(true);
			})
			.then(function(){unlock_fields(true)});
        }));
      };

      // interface function 4
      var unlock_fields = function(go_next){
        $("#"+s_ids.RUNSET_FROM_INPUT).prop('disabled', false);
        $("#"+s_ids.RUNSET_TO_INPUT).prop('disabled', false);
        sm.next_step_button();
        if(go_next){
          // TODO - change it
          $("#"+s_ids.FROM_RUNSET_SPAN).html(sm.auxi_dict["from_runset"].title);
          $("#"+s_ids.TO_RUNSET_SPAN).html(sm.auxi_dict["to_runset"].title);
          $("#"+s_ids.UPPER_SPANS_DIV).show();
          $("#"+s_ids.LOWER_SPANS_DIV).show();
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
      $("#"+s_ids.LOWER_SPANS_DIV).hide();
      update_runset_select_box_content();
      $("#"+s_ids.RUNSET_INFO_DIV).hide();
      $("#"+g_ids.RUNSET_NAME_SPAN).html("");
      $("#"+g_ids.RUNSET_NAME_INPUT).show();
      
      $("#"+s_ids.REFERENCES_COPY_SPAN).html("");
      $("#"+s_ids.REFERENCES_COPY_DIV).hide();
      
      $("#"+s_ids.RUNSET_CHOICE_DIV).find(".help_button").show();
      modelplus.requester.form.highlight_div(s_ids.RUNSET_CHOICE_DIV);
      $("#"+g_ids.RUNSET_MID_DATE_INPUT).show();
      hide_date_mid_span();
      $("#"+g_ids.BUTTON_SUBMIT).hide();
      $("#"+g_ids.BUTTON_PREV_STEP).hide();
      $("#"+g_ids.BUTTON_NEXT_STEP).show();
    }
  })();
  
  // --------------------------------------------------------- EXT ----------------------------------------------------------- //
  
  // load Runset select box if needed
  function update_runset_select_box_content(){

    var select_obj =  $("#"+s_ids.RUNSET_FROM_INPUT);
    if (!select_obj.length){ console.log("DOM object not found: " + s_ids.RUNSET_FROM_INPUT); }

    var select_options = $("#"+s_ids.RUNSET_FROM_INPUT + " option");
    if (select_options.length <= 1){
      if(select_options.html() != modelplus.model_requester.constant.labels.LOADING){ return; }
    } else return;
    
    modelplus.api.get_runset_results()
      .then(function(data){
        var sel_dom = $("#"+s_ids.RUNSET_FROM_INPUT);
        sel_dom.empty();
        add_opt(sel_dom, "", "Select...");
        data.forEach(function(cur_elem){
          if(cur_elem.id == modelplus.constant.realtime_runset_id) return;
          add_opt(sel_dom, cur_elem.id, cur_elem.title);
        })
        sel_dom.change(on_change_from_select);
    });
  }
  
  //
  function on_change_from_select(){
    var sel_dom = $("#"+s_ids.RUNSET_FROM_INPUT);
    
    // basic check
    if(sel_dom.length == 0){
      console.log("Input not found: " + s_ids.RUNSET_FROM_INPUT);
      return;
    }
    var selected_id = $("#"+s_ids.RUNSET_FROM_INPUT+" option:selected").attr("id");
    
    // 
    if(selected_id == ""){
      $("#"+s_ids.RUNSET_TO_DIV).hide();
    } else {
      modelplus.api.get_concurrently_runset_results(selected_id)
        .then(function(concurrently_runsets){
          var runset_to_div = $("#"+s_ids.RUNSET_TO_DIV);
          var sel_dom = $("#"+s_ids.RUNSET_TO_INPUT);
          sel_dom.empty();
          add_opt(sel_dom, "", "Select...");
          for(var cur_idx in concurrently_runsets){
            var cur_runset = concurrently_runsets[cur_idx];
            add_opt(sel_dom, cur_runset['id'], cur_runset['title']);
          }
          runset_to_div.show();
        });
    }
  }
  
  //
  function add_opt(select_dom, option_id, option_html){
    var cur_opt_dom = $("<option >");
    cur_opt_dom.attr("id", option_id);
    cur_opt_dom.html(option_html);
    select_dom.append(cur_opt_dom);
  }
  
  //
  function hide_date_mid_span(){
    $("#"+modelplus.requester.constant.id.RUNSET_MID_DATE_SPAN).html("");
  }

})();
