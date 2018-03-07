var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";

  var STATE_NUM = 5;
  var sm = modelplus.requester.state_machine;
  var ids = modelplus.requester.constant.id;
  
  // define get form functions
  (function () {
   sm.get_form_info_functions = sm.get_form_info_functions || {};
   sm.get_form_info_functions[STATE_NUM] = function(){
    
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
      var model_div_id, all_repr_comb, cur_post_dict_id, cur_tmp_vect;
      var solved = true;  // TODO - do it properly
      var cur_mdl_index = 1;
      
      for(cur_mdl_index = 1; cur_mdl_index <= modelplus.requester.model_count; cur_mdl_index++){
        model_div_id = ids.SET_MODELS_INNER_REPR_COMBINED_DIV_PREF + cur_mdl_index;

        // check if this one was not deleted
        if($("#"+model_div_id).length <= 0) continue;

        // 
        all_repr_comb = modelplus.requester.get_checked_acronyms(model_div_id).join(",");
        if(all_repr_comb.length <= 0) continue;
        
        // 
        cur_post_dict_id = "model_repr_"+cur_mdl_index;
        sm.post_dict[cur_post_dict_id] += "," + all_repr_comb;
        
        // remove repeated
        cur_tmp_vect = [];
        $.each(sm.post_dict[cur_post_dict_id].split(","), function(i, el){
          if($.inArray(el, cur_tmp_vect) === -1) cur_tmp_vect.push(el);
        });
        sm.post_dict[cur_post_dict_id] = cur_tmp_vect.join(",");
      }
      
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
      $("#"+ids.SET_MODELS_TITLE).hide();
      $("#"+ids.SET_MODELS_ADD_DIV).hide();
      $("#"+ids.SET_MODELS_ADDED_DIV).hide();
      $("#"+ids.SET_MODELS_COMPAR_DIV).hide();
      fill_models_list_span();
      $("#"+ids.SET_MODELS_LABEL).show();
      $("#"+ids.SET_MODELS_NAMES).show();
      build_combinations_options();
      modelplus.requester.form.highlight_div(ids.SET_MODELS_REPR_COMBINED_DIV);
    }
  })();
  
  // --------------------------------------------------------- EXT ----------------------------------------------------------- //
  
  // 
  function show_model_combined_options(){
    var checks_div_dom, mdl_idx, all_model_repr;
    
    // getting all representations
    mdl_idx = $(this).parent("div").attr("id").split("_").pop();
    all_model_repr = sm.post_dict["model_repr_"+mdl_idx].split(",");
    checks_div_dom = $(this).parent("div").find("div");
    
    // check if it is just a toggle
    if(checks_div_dom.html().trim() != ""){
      if(checks_div_dom.is(":visible"))
        checks_div_dom.hide();
      else
        checks_div_dom.show();
      return;
    }
    
    // load content
    modelplus.api.get_representations_from_combining(all_model_repr)
      .then(function(data){
        // basic check - empty result
        if (data.length == 0){
          checks_div_dom.html("No model combination available.");
          return;
        }
        
        // build checkboxes
        data.forEach(function(cur_repr_combined){
          var cur_repr_check_id, cur_repr_dom
          
          cur_repr_check_id = "repr_combined_"+mdl_idx+"_"+cur_repr_combined["acronym"];
          cur_repr_dom = $("<input type='checkbox' >");
          cur_repr_dom.attr("id", cur_repr_check_id);
          checks_div_dom.append(cur_repr_dom);
          cur_repr_dom = $("<label >");
          cur_repr_dom.attr("for", cur_repr_check_id);
          cur_repr_dom.html(cur_repr_combined["title"]);
          checks_div_dom.append(cur_repr_dom);
          checks_div_dom.append($("<br>"));
        });
      });
  }
  
  //
  function build_combinations_options(){
    var cur_mdl_index, cur_div_id, cur_div_dom, cur_a_dom, inner_div_dom;
    var cur_repr_check_id, cur_repr_dom, all_model_repr;
	var added_combinations;
    
    // check if not empty before touching it
    if ($("#"+ids.SET_MODELS_REPR_COMBINED_INNER_DIV).html().trim()) return;
    
	// build options
    inner_div_dom = $("#" + ids.SET_MODELS_REPR_COMBINED_INNER_DIV);
	added_combinations = 0;
    for(cur_mdl_index = 1; cur_mdl_index <= modelplus.requester.model_count; cur_mdl_index++){
      if(sm.post_dict["model_title_"+cur_mdl_index] === "undefined") continue;
      
      // create div for each model
      cur_div_id = ids.SET_MODELS_INNER_REPR_COMBINED_DIV_PREF + cur_mdl_index;
      cur_div_dom = $("<div>");
      cur_div_dom.attr("id", cur_div_id);
      cur_a_dom = $("<a ></a>");
      cur_a_dom.on("click", show_model_combined_options);
      cur_a_dom.html(sm.post_dict["model_title_"+cur_mdl_index]);
      cur_div_dom.append(cur_a_dom);
      cur_div_dom.append("<br>");
      cur_div_dom.append("<div>");
      
      // add it to inner div
      inner_div_dom.append(cur_div_dom);
	  added_combinations += 1;
    }
	
	// ops. No option? Nothing to do.
	if(added_combinations == 0){
      cur_div_dom = $("<div>");
	  cur_div_dom.html("No options available.");
	  inner_div_dom.append(cur_div_dom);
	}
  }
  
  
  
  // 
  function fill_models_list_span(){
    var cur_mdl_index, cur_a, cur_a_id;
    var titles_array = [];
    
    // build list
    for(cur_mdl_index = 1; cur_mdl_index <= modelplus.requester.model_count; cur_mdl_index++){
      if(sm.post_dict["model_title_"+cur_mdl_index] === "undefined") continue;
      
      cur_a_id = "model_a_"+cur_mdl_index;
      cur_a = "<a id='"+cur_a_id+"' onclick='modelplus.requester.show_model_details(this)'>";
      cur_a += "["+sm.post_dict["model_title_"+cur_mdl_index]+"]";
      cur_a += "</a>";
      titles_array.push(cur_a);
    }
    
    // select what to display
    if (titles_array.length > 0){
      $("#"+ids.SET_MODELS_NAMES).html(titles_array.join(", "));
    } else {
      $("#"+ids.SET_MODELS_NAMES).html("No model selected.");
    }
  }
  
})();