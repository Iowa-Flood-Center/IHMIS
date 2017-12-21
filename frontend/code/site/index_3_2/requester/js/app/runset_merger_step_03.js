var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  const state_num = 3;
  var sm = modelplus.requester.state_machine;
  var g_ids = modelplus.requester.constant.id;
  var s_ids = modelplus.model_requester.constant.id;
  
  sm.get_form_info_functions = sm.get_form_info_functions || {};
  
  // define get form functions
  (function () {
   sm.get_form_info_functions[state_num] = function(){
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
    
    sm.update_form_functions[state_num] = function(){
      $("#"+s_ids.SET_MODELS_COMPAR_DIV).hide();
      modelplus.requester.form.highlight_div(s_ids.SET_MODELS_DIV);
	  display_potential_models(select_potential_models());
    }
  })();
  
  // --------------------------------------------------------- EXT ----------------------------------------------------------- //
  
  // 
  function select_potential_models(){
    var models_to = modelplus.requester.state_machine.auxi_dict["from_runset"]["sc_model"];
    var models_from = modelplus.requester.state_machine.auxi_dict["to_runset"]["sc_model"];
    var models_potential = [];
    models_from.forEach(function(model_from){
      var will_add = true;
      models_to.forEach(function(model_to){
        if(model_from.title == model_to.title){
          will_add = false; return; }
      });
      if(!will_add) return;
      models_potential.push(model_from);
    });
    return(models_potential);
  }
  
  // 
  function display_potential_models(potential_models){
    var div_dom = $("#"+s_ids.COPY_MODELS_ADDED_DIV);
	if(div_dom.html() != "") return;
    potential_models.forEach(function(cur_model){
	  div_dom.append(create_model_checkbox_dom(cur_model));
    });
  }
  
  //
  function create_model_checkbox_dom(model_obj){
    var span_dom = $("<span>");
	var input_dom = $("<input type='checkbox'>");
	var label_dom = $("<label>");
	
	var checkbox_id = "copy_model_checkbox_" + model_obj.id;
	input_dom.attr("id", checkbox_id);
	label_dom.attr("for", checkbox_id);
	label_dom.html(model_obj.title);
	
	span_dom.append(input_dom);
	span_dom.append(label_dom);
	span_dom.append($("<br />"));
	return(span_dom);
  }

})();