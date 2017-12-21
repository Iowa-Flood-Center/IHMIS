/**
 * The functionally of adding a model to the interface.
 * It is pretty complex and is shared by both runset and model requester.
 * This way, it deserves a separate file to call home.
 */

/**
 * Global variables:
 * - modelplus.requester.constant.id.SET_MODELS_INNER_PREF
 * - modelplus.requester.constant.labels.HLM_SELECTION
 * - modelplus.requester.constant.id.SET_MODELS_INNER_FORC_DIV_PREF
 * - modelplus.requester.constant.id.SET_MODELS_INNER_PARM_DIV_PREF
 * - modelplus.requester.constant.id.SET_MODELS_INNER_EVAL_DIV_PREF
 * - modelplus.requester.constant.id.SET_MODELS_INNER_REPR_DIV_PREF
 * - modelplus.api.*
 */

var modelplus = modelplus || {};
modelplus.requester = modelplus.requester || {};

(function () {
  
  var sm = modelplus.requester.state_machine; // TODO - THIS SHOULD NOT BE HERE
  var ids = modelplus.requester.constant.id;
  var labels = modelplus.requester.constant.labels;
  
  /**
   * 
   * container_div_id : ID of the div that is going to receive the DOM object referent to the new model form
   * model_count : Integer describing the model count for the instance
   * available_hlms : 
   */
  modelplus.requester.add_new_model = function(container_div_id, model_count, available_hlms){
    
    // basic check
    var container_div = $("#"+container_div_id);
    if (!container_div.length){
      console.log("Div not found: '" + container_div_id + "'.");
      return;
    }
    
    // 
    var model_div_id = ids.SET_MODELS_INNER_PREF + model_count;
    var model_div = $("<div id='"+model_div_id+"' class='model_def'>");
    
    // create each field
    model_div.append(create_title_input_object(model_count));
    model_div.append(create_description_object(model_count));
    model_div.append(create_hlm_select_object(model_count, available_hlms));
    model_div.append(create_forcing_div(model_count));
    model_div.append(create_globalpars_div(model_count));
    model_div.append(create_evaluations_div(model_count));
    model_div.append(create_representations_div(model_count));
    
    // create minus
    model_div.append(create_hide_button(model_count));
    model_div.append(create_show_button(model_count));
    model_div.append(create_delete_button(model_count));
    
    // add
    container_div.append(model_div);
  }
  
  // Create input title object
  function create_title_input_object(model_count){
    var model_title_label = $("<label id='model_name_label_"+model_count+"'>Model title:</label>");
    var model_title_span = $("<span id='model_name_span_"+model_count+"' ></span>");                  // TODO - set id
    model_title_label.append(model_title_span);
    var model_title_input = $("<input id='model_name_input_"+model_count+"' type='text'></input>");
    model_title_label.append(model_title_input);
    return(model_title_label);
  }
  
  // Create input description object
  function create_description_object(model_count){
    var model_desc_label = $("<label id='model_desc_label_"+model_count+"'>Model description:</label>");
    var model_desc_span = $("<span id='model_desc_span_"+model_count+"' ></span>");                  // TODO - set id
    model_desc_label.append(model_desc_span);
    var model_desc_input = $("<input id='model_desc_input_"+model_count+"' type='text'></input>");
    model_desc_label.append(model_desc_input);
    return(model_desc_label);
  }
  
  //
  function create_hlm_select_object(model_count, available_hlms){
    var input_id = "model_hlm_input_" + model_count;
    var model_hlm_label = $("<label>Hillslope model:</label>");
    var model_hlm_span = $("<span></span>");
    model_hlm_label.append(model_hlm_span);
    var model_hlm_input = $("<select>");
    model_hlm_input.attr("id", input_id);
    model_hlm_input.change(change_hlm);
    
    // create basic option
    cur_opt_add = $('<option>', {
      value: -1,
      text: labels.HLM_SELECTION
    })
    model_hlm_input.append(cur_opt_add);
    
    // create all available options
    var cur_opt_add, avail_hlm;
    for(var avail_hlm_idx in available_hlms){
      avail_hlm = available_hlms[avail_hlm_idx];
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
  function create_forcing_div(model_count){
    var model_forcings_label = $("<label>Forcings:</label>");
    var model_forcings_div = $("<div>" + labels.HLM_SELECTION + "</div>");
    model_forcings_div.attr("id", ids.SET_MODELS_INNER_FORC_DIV_PREF + model_count);
    model_forcings_label.append(model_forcings_div);
    return(model_forcings_label);
  }
  
  // 
  function create_globalpars_div(model_count){
    var model_gblparms_label = $("<label>Global Parameters:</label>");
    var model_gblparms_div = $("<div>" + labels.HLM_SELECTION + "</div>");
    model_gblparms_div.attr("id", ids.SET_MODELS_INNER_PARM_DIV_PREF + model_count);
    model_gblparms_label.append(model_gblparms_div);
    return(model_gblparms_label);
  }
  
  // 
  function create_evaluations_div(model_count){
    var model_evaluats_label = $("<label>Evaluations:</label>");
    var model_evaluats_div = $("<div>" + labels.HLM_SELECTION + "</div>");
    model_evaluats_div.attr("id", ids.SET_MODELS_INNER_EVAL_DIV_PREF + model_count);
    model_evaluats_label.append(model_evaluats_div);
    return(model_evaluats_label);
  }
  
  // 
  function create_representations_div(model_count){
    var model_repres_label = $("<label>Representations:</label>");
    var model_repres_div = $("<div>" + labels.HLM_SELECTION + "</div>");
    model_repres_div.attr("id", ids.SET_MODELS_INNER_REPR_DIV_PREF + model_count);
    model_repres_label.append(model_repres_div);
    return(model_repres_label);
  }
  
  //
  function create_hide_button(model_count){
    var model_hide_a = $("<a id='model_hide_"+model_count+"' >[-]</a>");
    model_hide_a.click(hide_view_menu);
    return(model_hide_a);
  }
  
  // 
  function create_show_button(model_count){
    var model_show_a = $("<a id='model_show_"+model_count+"' >[+]</a>");
    model_show_a.css('display', 'none');
    model_show_a.click(show_view_menu);
    return(model_show_a);
  }
  
  // 
  function create_delete_button(model_count){
    var model_delete_a = $("<a id='model_delete_"+model_count+"' >[remove]</a>");
    model_delete_a.click(delete_view_menu);
    return(model_delete_a);
  }
  
  /////////////////////////////////// actions ////////////////////////////////////////
  
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
	modelplus.api.get_forcing_types_for_hlm(the_hlm_id)
      .then((all_forcings) => { load_forcings(the_hlm_id, all_forcings, model_num, 0); });

    // fill global parameters
	modelplus.api.get_global_parameters_for_models(the_hlm_id)
      .then((all_globalpars) => { load_global_parameters(all_globalpars, model_num); });
              
    // fill evaluations
    modelplus.api.get_evaluations_for_hlm(the_hlm_id, sm.post_dict["reference_ids"])
      .then((all_evaluations) => { load_evaluations(all_evaluations, model_num); });

    // fill simple representations
    modelplus.api.get_representations_for_hlm(the_hlm_id)
      .then((all_representations) => { load_representations(all_representations, model_num) });
  }
  
  // perform AJAX requests to fill div of forcing options
  // TODO - review that
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
  
  //
  // TODO - review that
  function load_representations(hlm_representations, mdl_num){
    var div_id = ids.SET_MODELS_INNER_REPR_DIV_PREF + mdl_num;
	$("#" + div_id).empty();
	for(var repr_idx in hlm_representations){
      $("#" + div_id).append(create_representation_input_object(hlm_representations[repr_idx],
	                                                            mdl_num));
    }
  }
  
  //
  // TODO - review that
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
  
  // create forcing option DOM select
  // TODO - review that
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
  
  //
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
  
})();
