var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};
modelplus.requester.state_machine = modelplus.requester.state_machine || {};

(function () {
  "use strict";
  
  const state_num = 4;
  var sm = modelplus.requester.state_machine;
  var ids = modelplus.requester.constant.id;
  var labels = modelplus.requester.constant.labels;
  
  
  // define get form functions
  (function () {
   sm.get_form_info_functions = sm.get_form_info_functions || {};
   sm.get_form_info_functions[state_num] = function(){
    var sm = modelplus.requester.state_machine;
    var ids = modelplus.requester.constant.id;
    
    // interface function 1
    var lock_fields = function(){
      return ( new Promise( function(resolve, reject){
        $("#"+ids.SET_MODELS_ADDED_DIV).find('*').each(function(){
          $(this).prop('disabled', true);
        });
        sm.next_step_loading();
        resolve(true);
      }));
    }

    // interface function 2
    var check_fields = function(){
      return ( new Promise( function(resolve, reject){
		var count_valid_models = 0;
        var cur_mdl_index = 1;
        var will_resolve = true;
        var model_div_id = null;
        var cur_input_dom, cur_input_id, cur_input_id_pref, cur_sub_idx;
		
		// check if every model was minimally filled
        for(cur_mdl_index = 1; cur_mdl_index <= modelplus.requester.model_count; cur_mdl_index++){
          model_div_id = ids.SET_MODELS_INNER_PREF + cur_mdl_index;
          
          // check if this one was not deleted
          if($("#"+model_div_id).length <= 0) continue;
          
          // check if title is not null
          cur_input_id = "model_name_input_" + cur_mdl_index;
          if($("#"+cur_input_id).val().trim() == ""){
            sm.next_step_error_show("At least one model has empty name.");
            will_resolve = false;
            break;
          }
		  
		  // check if an HLM was selected
		  cur_input_id = "model_hlm_input_" + cur_mdl_index;
		  if($("#"+cur_input_id+" option:selected").val() == -1){
            sm.next_step_error_show("All models must have a HLM Model selected.");
            will_resolve = false;
            break;
          }
		  
          // check if there is no empty global parameter
          cur_sub_idx = 1;
		  cur_input_id_pref = "model_gblprm_"+cur_mdl_index+"_";
		  while(true){
            cur_input_id = cur_input_id_pref + cur_sub_idx;
			cur_input_dom = $("#"+cur_input_id);
			if(cur_input_dom.length <= 0) break;
			if(cur_input_dom.val().trim() == ""){
              sm.next_step_error_show("All global parameters must be provided.");
              will_resolve = false;
			  break;
            }
            cur_sub_idx += 1;
		  }
		  
		  count_valid_models += 1;
        }
		
		// check if at least one model was created correctly
        if (will_resolve && (count_valid_models == 0)){
          sm.next_step_error_show("At least one model must be defined.");
          will_resolve = false;
        }
        
        // define resolution
        resolve(will_resolve);
      }));
    }

    // interface function 3
    var solve = function(solved){
      var model_div_id, input_id;
	  var cur_sub_idx, cur_input_id_pref, cur_post_dict_id, cur_eval_div_id;
	  var cur_input_id, cur_input_dom;
	  var cur_mdl_index = 1;

      for(cur_mdl_index = 1; cur_mdl_index <= modelplus.requester.model_count; cur_mdl_index++){
        model_div_id = ids.SET_MODELS_INNER_PREF + cur_mdl_index;
        // TODO - clean all
		
		// check if this one was not deleted
        if($("#"+model_div_id).length <= 0) continue;
		
        // add items to the post dictionary object
		sm.post_dict["model_id_"+cur_mdl_index] = "mdl"+cur_mdl_index;
        sm.post_dict["model_title_"+cur_mdl_index] = $("#model_name_input_"+cur_mdl_index).val();
		sm.post_dict["model_desc_"+cur_mdl_index] = $("#model_desc_input_"+cur_mdl_index).val();
		
		input_id = "model_hlm_input_" + cur_mdl_index;
		sm.post_dict["hillslope_model_"+cur_mdl_index] = $("#"+input_id+" option:selected").val();
		
		// add forcings
		cur_sub_idx = 1;
		cur_input_id_pref = "model_forcing_"+cur_mdl_index;
		while(true){
          cur_input_id = cur_input_id_pref + "_" + cur_sub_idx + " option:selected";
		  cur_input_dom = $("#"+cur_input_id);
		  if(cur_input_dom.length <= 0) break;
		  cur_post_dict_id = "model_for_"+cur_mdl_index+"_"+cur_sub_idx;
		  sm.post_dict[cur_post_dict_id] = cur_input_dom.val().trim();
          cur_sub_idx += 1;
		}
		
		// add global parameters
		cur_sub_idx = 1;
		cur_input_id_pref = "model_gblprm_"+cur_mdl_index+"_";
		while(true){
          cur_input_id = cur_input_id_pref + cur_sub_idx;
		  cur_input_dom = $("#"+cur_input_id);
		  if(cur_input_dom.length <= 0){ break; }
		  cur_post_dict_id = "model_par_"+cur_mdl_index+"_"+cur_sub_idx;
		  sm.post_dict[cur_post_dict_id] = cur_input_dom.val().trim();
          cur_sub_idx += 1;
		}
		
		// add evaluations
		cur_sub_idx = 1;
		cur_input_id_pref = "model_evaluation_"+cur_mdl_index+"_";
		cur_post_dict_id = "model_eval_"+cur_mdl_index;
		cur_eval_div_id = ids.SET_MODELS_INNER_EVAL_DIV_PREF + cur_mdl_index;
		sm.post_dict[cur_post_dict_id] = modelplus.requester.get_checked_values(cur_eval_div_id);
		/*
		sm.post_dict[cur_post_dict_id] = [];
		while(true){
          cur_input_id = cur_input_id_pref + cur_sub_idx;
		  cur_input_dom = $("#"+cur_input_id);
		  if(cur_input_dom.length <= 0) break;
		  if(cur_input_dom.prop('checked')){
			sm.post_dict[cur_post_dict_id].push(cur_input_dom.val());
		  }
		  cur_sub_idx += 1;
		}
		*/
		
		// add representations
        cur_input_id = ids.SET_MODELS_INNER_REPR_DIV_PREF + cur_mdl_index;
		cur_post_dict_id = "model_repr_"+cur_mdl_index;
		sm.post_dict[cur_post_dict_id] = modelplus.requester.get_checked_acronyms(cur_input_id);
        sm.post_dict[cur_post_dict_id] = sm.post_dict[cur_post_dict_id].join(",");
      }
	
      // TODO - add to memory
      return ( new Promise( function(resolve, reject){
        resolve(solved);
      }));
    }

    // interface function 4
    var unlock_fields = function(go_next){
      $("#"+ids.SET_MODELS_ADDED_DIV).find('*').each(function(){
        $(this).prop('disabled', false);
      });
      sm.next_step_button();
      if(go_next) modelplus.requester.state_machine.next_step_go();
    }
    
    // nested calls
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
      hide_models_list_span();
      modelplus.requester.form.highlight_div(ids.SET_MODELS_DIV);
      $("#"+ids.SET_MODELS_REPR_COMBINED_DIV).hide();
	  $("#"+ids.SET_MODELS_REPR_COMBINED_INNER_DIV).empty();
      show_reference_list_span();
	  $("#"+ids.SET_MODELS_TITLE).show();
	  load_hlm_options()
        .then(function(available_hlms){
          $("#"+ids.SET_MODELS_ADD_DIV).show();
          $("#"+ids.SET_MODELS_ADDED_DIV).show();
		  sm.available_hlm = available_hlms;
      });
    }
  })();
  
  // --------------------------------------------------------- EXT ----------------------------------------------------------- //
   
  function show_view_menu(){
    var menu_num = $(this).attr('id').split('_').pop();
    var model_div_id = ids.SET_MODELS_INNER_PREF + menu_num;
    var model_show_a = "model_show_" + menu_num;
    var model_title_span_id = "model_name_span_" + menu_num;
    $("#"+model_div_id).find("*").each(function(){
      var this_id = $(this).attr('id');
      switch (this_id){
        case model_title_span_id:
          $(this).html("");
          $(this).hide();
          break;
        case model_show_a:
          $(this).hide();
          break;
        default:
          $(this).show();
      }
    });
  }
  
  //
  function hide_view_menu(){
    var menu_num = $(this).attr('id').split('_').pop();
    var model_div_id = ids.SET_MODELS_INNER_PREF + menu_num;
    var model_title_label_id = "model_name_label_" + menu_num;
    var model_title_span_id = "model_name_span_" + menu_num;
    var model_title_input_id = "model_name_input_" + menu_num;
    var model_show_a = "model_show_" + menu_num;
    $("#" + model_div_id).find("*").each(function(){
      var this_id = $(this).attr('id');
      switch(this_id){
        case model_title_label_id:
          break;
        case model_title_span_id:
          $(this).html($("#"+model_title_input_id).val());
          $(this).show();
          return;
        case model_show_a:
          $(this).show();
          return;
        default:
          $(this).hide();
      }
    })
  }
  
  // 
  function delete_view_menu(){
    var menu_num = $(this).attr('id').split('_').pop();
    var model_div_id = ids.SET_MODELS_INNER_PREF + menu_num;
    $("#" + model_div_id).remove(); 
  }
  
  // 
  function hide_models_list_span(){
	$("#"+ids.SET_MODELS_NAMES).html("");
    $("#"+ids.SET_MODELS_LABEL).hide();
    $("#"+ids.SET_MODELS_NAMES).hide();
  }
  
  // performs an AJAX request to get information about valid HLM models
  function load_hlm_options(){
    var ws_api_url;
    ws_api_url = modelplus.url.proxy + modelplus.url.api;
	ws_api_url += 'hl_models%i%timestamp_ini=' + sm.post_dict["timestamp_ini"];
	ws_api_url += '%e%timestamp_end=' + sm.post_dict["timestamp_end"];
    return ($.getJSON(ws_api_url));
  }
  
  // performs an AJAX request to update forcings
  function change_hlm(){
    var model_num = $(this).attr('id').split('_').pop();
	var cur_input_id = "model_hlm_input_" + model_num;
	var the_hlm_id = $("#"+cur_input_id+" option:selected").val();
	
	// if null, clean forcings, ... and evaluation divs
    if(the_hlm_id == '-1'){
      var div_id = ids.SET_MODELS_INNER_FORC_DIV_PREF + model_num;
      $("#" + div_id).html(labels.HLM_SELECTION);
      return;
    }
	
	var ws_api_url = modelplus.url.proxy + modelplus.url.api;
	var ws_url = null;
	
	// fill forcings div
	ws_url = 'forcing_types%i%from_hlmodel='+the_hlm_id;
	$.getJSON(ws_api_url + ws_url)
	  .then((all_forcings) => { load_forcings(the_hlm_id, all_forcings, model_num, 0); });

    // fill global parameters
    ws_url = 'hl_models_global_parameters%i%from_hlmodel='+the_hlm_id;
	$.getJSON(ws_api_url + ws_url)
	  .then((all_globalpars) => { load_global_parameters(all_globalpars, model_num); });
			  
    // fill evaluations
    modelplus.api.get_evaluations_for_hlm(the_hlm_id, sm.post_dict["reference_ids"])
      .then((all_evaluations) => { load_evaluations(all_evaluations, model_num); });

    // fill simple representations
    modelplus.api.get_representations_for_hlm(the_hlm_id)
      .then((all_representations) => { load_representations(all_representations, model_num) });
  }
  
  // perform AJAX requests to fill div of forcing options
  function load_forcings(hlm_id, hlm_forcings, mdl_num, forc_idx){
    var ws_api_url, forcing_title;
    var div_id = ids.SET_MODELS_INNER_FORC_DIV_PREF + mdl_num;
	if (forc_idx == 0) $("#" + div_id).empty();
    forcing_title = hlm_forcings[forc_idx].title;
    modelplus.api.get_forcing_options(hlm_forcings[forc_idx].id,
	                                  sm.post_dict["timestamp_ini"],
                                      sm.post_dict["timestamp_end"])
      .then(function(all_forc_opts){
        $("#" + div_id).append(create_forcing_select_object(forcing_title,
                                                            forc_idx + 1,
                                                            all_forc_opts, 
	                                                        mdl_num));
        if(forc_idx < (hlm_forcings.length-1)){
          load_forcings(hlm_id, hlm_forcings, mdl_num, forc_idx+1);
        }
      });
  }
  
  // create forcing option DOM select
  function create_forcing_select_object(forcing_title, forcing_idx, all_forc_opts, mdl_num){
    var label_obj, select_obj, option_obj, dom_id;
	dom_id = "model_forcing_"+mdl_num+"_"+forcing_idx;
	label_obj = $("<label>"+forcing_title+":</label>");
	select_obj = $("<select id='"+dom_id+"'>");
	option_obj = $('<option>', {
      value: -1,
      text: modelplus.requester.constant.labels.NONE
    });
	select_obj.append(option_obj);
    for(var forcing_opt_idx in all_forc_opts){
      option_obj = $('<option>', {
        value: all_forc_opts[forcing_opt_idx]['id'],
        text: all_forc_opts[forcing_opt_idx]['title']
      });
      select_obj.append(option_obj);
    }
	label_obj.append(select_obj);
	
	return(label_obj);
  }
  
  // fill div of global parameters
  function load_global_parameters(hlm_globalparms, mdl_num){
    var div_id = ids.SET_MODELS_INNER_PARM_DIV_PREF + mdl_num;
	$("#" + div_id).empty()
    for(var gblprm_idx in hlm_globalparms){
	   $("#" + div_id).append(create_globalparameter_input_object(hlm_globalparms[gblprm_idx],
	                                                              mdl_num));
	}
  }
  
  // create global parameters DOM inputs
  function create_globalparameter_input_object(glb_param_obj, mdl_num){
    var label_obj, input_obj, dom_id;
	dom_id = "model_gblprm_"+mdl_num+"_"+glb_param_obj.id;
	label_obj = $("<label>"+glb_param_obj.title+":</label>");
	input_obj = $("<input type='text' id='"+dom_id+"'>");
	input_obj.val(glb_param_obj.default_value);
	label_obj.append(input_obj);
	return(label_obj);
  }
  
  // fill div of evaluations 
  function load_evaluations(hlm_evaluations, mdl_num){
    var div_id = ids.SET_MODELS_INNER_EVAL_DIV_PREF + mdl_num;
	$("#" + div_id).empty()
    for(var eval_idx in hlm_evaluations){
	   $("#" + div_id).append(create_evaluations_input_objects(hlm_evaluations[eval_idx],
	                                                           mdl_num));
	}
  }
  
  // create evaluations DOM inputs
  function create_evaluations_input_objects(eval_obj, mdl_num){
    var div_object, input_obj, label_obj, dom_id, label_text;
	dom_id = "model_evaluation_"+mdl_num+"_"+eval_obj.id+"_"+eval_obj.id;
	div_object = $("<div>");
	input_obj = $("<input type='checkbox' id='"+dom_id+"'>");
	input_obj.val(eval_obj.acronym+"_"+eval_obj.screference_acronym);
	
	label_text = eval_obj.title + "(using "+eval_obj.screference_title+")";
	
	label_obj = $("<label for='"+dom_id+"'>"+label_text+"</label>");
	div_object.append(input_obj);
	div_object.append(label_obj);
	return(div_object);
  }
  
  //
  function load_representations(hlm_representations, mdl_num){
    var div_id = ids.SET_MODELS_INNER_REPR_DIV_PREF + mdl_num;
	$("#" + div_id).empty();
	for(var repr_idx in hlm_representations){
      $("#" + div_id).append(create_representation_input_object(hlm_representations[repr_idx],
	                                                            mdl_num));
    }
  }
  
  //
  function create_representation_input_object(repr_obj, mdl_num){
    var div_object, input_obj, label_obj, dom_id;
	dom_id = ids.SET_MODELS_SEL_REPR_PREF + mdl_num + "_" + repr_obj.acronym;
	div_object = $("<div>");
	input_obj = $("<input type='checkbox' id='"+dom_id+"'>");
	label_obj = $("<label for='"+dom_id+"'>"+repr_obj.title+"</label>");
	div_object.append(input_obj);
	div_object.append(label_obj);
	return(div_object);
  }
  
  // create select
  // TODO - use the model number argument
  function create_hlm_select_object(mdl_num){
    var input_id = "model_hlm_input_" + mdl_num;
    var model_hlm_label = $("<label>Hillslope model:</label>");
    var model_hlm_span = $("<span></span>");
    model_hlm_label.append(model_hlm_span);
    var model_hlm_input = $("<select>");
	model_hlm_input.attr("id", input_id);
	model_hlm_input.change(change_hlm);
	
	// create basic option
    cur_opt_add = $('<option>', {
      value: -1,
      text: modelplus.requester.constant.labels.HLM_SELECTION
    })
	model_hlm_input.append(cur_opt_add);
	
	// create all available options
    var cur_opt_add, avail_hlm;
    for(var avail_hlm_idx in sm.available_hlm){
      avail_hlm = sm.available_hlm[avail_hlm_idx];
      cur_opt_add = $('<option>', {
        value: avail_hlm.id,
        text: avail_hlm.title
      })
      model_hlm_input.append(cur_opt_add);
    }
    model_hlm_label.append(model_hlm_input);
    return(model_hlm_label);
  }
  
  //
  function add_new_model(){
    modelplus.requester.model_count += 1;
	var mdl_num = modelplus.requester.model_count;
    
    var model_div_id = ids.SET_MODELS_INNER_PREF + mdl_num;
    var model_div = $("<div id='"+model_div_id+"' class='model_def'>");
    
    // create title field
    var model_title_label = $("<label id='model_name_label_"+mdl_num+"'>Model title:</label>");
    var model_title_span = $("<span id='model_name_span_"+mdl_num+"' ></span>");                  // TODO - set id
    model_title_label.append(model_title_span);
    var model_title_input = $("<input id='model_name_input_"+mdl_num+"' type='text'></input>");
    model_title_label.append(model_title_input);
    model_div.append(model_title_label);
	
	// create description field
	var model_desc_label = $("<label id='model_desc_label_"+mdl_num+"'>Model description:</label>");
	var model_desc_span = $("<span id='model_desc_span_"+mdl_num+"' ></span>");                  // TODO - set id
	model_desc_label.append(model_desc_span);
	var model_desc_input = $("<input id='model_desc_input_"+mdl_num+"' type='text'></input>");
	model_desc_label.append(model_desc_input);
    model_div.append(model_desc_label);
    
    // create hillslope profile field
    model_div.append(create_hlm_select_object(mdl_num));
	
	// create forcings div
	var model_forcings_label = $("<label>Forcings:</label>");
	var model_forcings_div = $("<div>" + labels.HLM_SELECTION + "</div>");
	model_forcings_div.attr("id", ids.SET_MODELS_INNER_FORC_DIV_PREF + mdl_num);
	model_forcings_label.append(model_forcings_div);
	model_div.append(model_forcings_label);
	
	// create global parameters div
    var model_gblparms_label = $("<label>Global Parameters:</label>");
	var model_gblparms_div = $("<div>" + labels.HLM_SELECTION + "</div>");
	model_gblparms_div.attr("id", ids.SET_MODELS_INNER_PARM_DIV_PREF + mdl_num);
	model_gblparms_label.append(model_gblparms_div);
	model_div.append(model_gblparms_label);
	
	// create evaluations div
	var model_evaluats_label = $("<label>Evaluations:</label>");
	var model_evaluats_div = $("<div>" + labels.HLM_SELECTION + "</div>");
	model_evaluats_div.attr("id", ids.SET_MODELS_INNER_EVAL_DIV_PREF + mdl_num);
	model_evaluats_label.append(model_evaluats_div);
	model_div.append(model_evaluats_label);
	
	// create representations div
	var model_repres_label = $("<label>Representations:</label>");
	var model_repres_div = $("<div>" + labels.HLM_SELECTION + "</div>");
	model_repres_div.attr("id", ids.SET_MODELS_INNER_REPR_DIV_PREF + mdl_num);
	model_repres_label.append(model_repres_div);
	model_div.append(model_repres_label);
    
    // create hide buttons
    var model_hide_a = $("<a id='model_hide_"+mdl_num+"' >[-]</a>");
    model_hide_a.click(hide_view_menu);
    model_div.append(model_hide_a);
    
    // create show button
    var model_show_a = $("<a id='model_show_"+mdl_num+"' >[+]</a>");
    model_show_a.css('display', 'none');
    model_show_a.click(show_view_menu);
    model_div.append(model_show_a);
    
    // create delete button
    var model_delete_a = $("<a id='model_delete_"+mdl_num+"' >[remove]</a>");
    model_delete_a.click(delete_view_menu);
    model_div.append(model_delete_a);
    
    $("#"+ids.SET_MODELS_ADDED_DIV).append(model_div);
  }
  
  modelplus.requester.add_new_model = function(){
      add_new_model();
  }
  
  //
  function show_reference_list_span(){
    $("#" + ids.REFERENCES_INCLUDE_LIST_DIV).hide();
    $("#" + ids.REFERENCES_INCLUDE_TITLE).hide();
    $("#" + ids.REFERENCES_INCLUDE_LABEL).show();
    $("#" + ids.REFERENCES_INCLUDE_NAMES).html(JSON.stringify(sm.post_dict["reference_ids"]));  
    $("#" + ids.REFERENCES_INCLUDE_NAMES).show();
  }

})();
