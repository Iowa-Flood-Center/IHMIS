/**
 * Set of functions for loading stuffs.
 * Some functions depend on the following global variables:
 * - GLB_...
 */
 
/**
 * Acronyms:
 * - sbox: select box
 */

/***************************************************** NEW FUNCS *****************************************************/

(function () {
  "use strict";
  var mpd = modelplus.dom;

  /***------------------------------------------------- DOM FUNCS -------------------------------------------------***/
  
  /**
   * Reads web service related to the initial data to be retrieved into global variables
   * func_to_run - Function to be executed after loading data
   * RETURN - None. Changes are performed in GLB_vars prototype
   */
  modelplus.dom.load_init_data = function(func_to_run){
    modelplus.api.get_runset_results()
      .then(function(data){
        GLB_vars.prototype.sc_runsets = data;
        if ((typeof func_to_run !== 'undefined') && (func_to_run != null)){
          func_to_run();
        }
	  });
  }
  
  /**
   * Function called to display options for mono model or dual model comparison.
   * @param menu_1_id_clicked
   * @return None
   */
  mpd.on_menu_1_click = function(menu_1_id_clicked){
    // identifies clicked radio button and searches for corresponding content box to display it, hiding others.

    var count, cur_element_id;
    for(count = 0; count < GLB_menu_label_id_1.length; count++){
      cur_element_id = "#" + modelplus.ids.MENU_CONTENTS[count];
      if (GLB_menu_label_id_1[count] == menu_1_id_clicked){
        if ($("#" + menu_1_id_clicked).hasClass("npact")){
          $(cur_element_id).css("visibility", "visible");
          $(cur_element_id).css("display", "block");
        } else {
          $(cur_element_id).css("visibility", "hidden");
          $(cur_element_id).css("display", "none");
        }
      } else {
        $("#" + GLB_menu_label_id_1[count]).removeClass("npact");
        $(cur_element_id).css("visibility", "hidden");
        $(cur_element_id).css("display", "none");
      }
    }
  }

  /**
   *
   * TODO - adapt to the new flexible version of the code
   */
  mpd.reclick_item = function(){	
	// this function is called when model 1 is changed.
	// basically it searched for the selected element and calls its "click" function once again
	
	var radio_ids = ['np'+opt_mono_r_flin, 'np'+opt_mono_r_prec, 'np'+opt_mono_r_soim, 'np'+opt_mono_r_sois, 'np'+opt_mono_r_quni, 'np'+opt_mono_f_qsel, 'np'+opt_mono_r_runo, 'np'+opt_mono_r_pree, 'np'+opt_mono_r_prac,
					 'np'+opt_comp_r_flin, 'np'+opt_comp_r_prec, 'np'+opt_comp_r_soim, 'np'+opt_comp_r_sois, 'np'+opt_comp_r_quni, 'np'+opt_comp_f_qrel, 'np'+opt_comp_r_runo, 'np'+opt_comp_r_pree, 'np'+opt_comp_r_prac];
	
	var current_date = null;
	
	// store current rain date if possible
	if (rain !== undefined){
		current_date = rain.arr_val;
	}
	
	// re click the information type
	for (count_id = 0; count_id < radio_ids.length; count_id++){
		if ($("#" + radio_ids[count_id]).hasClass("npact")){
			$("#" + radio_ids[count_id]).removeClass("npact"),
			// alert("#" + radio_ids[count_id] + " is selected.");
			$("#" + radio_ids[count_id]).click();
			break;
		}
	}
	
	// store current rain date if possible
	if (current_date != null){
		rain.arr_val = current_date;
		timeline_anim();
		rain.slide();
	}
  }

  /**
   *
   * RETURN - None. Display message in the interface.
   */
  mpd.load_runset_desc = function(){
	var select_value;
	var web_service_add;
	
	select_value = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
	
	// display blocks
	div_modal.style.display = "block";
	inner_html = "<p><span id='modal_close_span' onclick='modelplus.main.hide_message_block()'>×</span></p>";
	inner_html += "<p>" + msg_string + "</p>";
	div_modal_ctt.html(inner_html);
  }

  /**
   *
   * RETURN - None. Display message in the interface.
   */
  mpd.load_model_desc = function(){
	var sc_model_id, sc_runset_id, web_service_add, msg_string;
	
	sc_runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
	sc_model_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
	
	modelplus.api.get_model_result(sc_runset_id, sc_model_id)
	  .then(function(data){
		if(data.length > 0){
			msg_string = "<strong>Title:</strong> " + data[0].title + "<br />";
			msg_string += "<strong>Description:</strong> " + data[0].description + "<br />";
		} else if (data.error !== 'undefined') {
			msg_string = "<strong>Error:</strong> " + data.error;
		} else {
			msg_string = "<strong>Error:</strong> No description available.";
		}
		
		// display block
		modelplus.main.display_message_block(msg_string);
	});
  }

  /**
   * TODO - replace by modelplus.main.display_message_block
   * msg_html - Message to be displayed in HTML format.
   * RETURN - None. Display message in the interface.
   */
  mpd.display_message_block = function(msg_html){
    var div_modal = document.getElementById('modal_div');
    var div_modal_ctt = $('#modal_content_div');
    var inner_html;

    div_modal.style.display = "block";
    inner_html = "<p><span id='modal_close_span' onclick='modelplus.main.hide_message_block()'>×</span></p>";
    inner_html += "<p>" + msg_html + "</p>";
    div_modal_ctt.html(inner_html);
    
    modelplus.keyCodes[modelplus.MODAL_HYDROGRAPH_CLOSE_BUTTON] = function(){
      modelplus.main.hide_message_block();
    };
  }

  /**
   *
   * msg_html - Message to be displayed in HTML format.
   * RETURN - None. Display message in the interface.
   */
  mpd.display_hidrograph_block = function(msg_html){
    var div_modal = document.getElementById('modal_hidrograph_div');
    var div_modal_ctt = $('#modal_content_hidrograph_div');
    var inner_html;
	
    div_modal.style.display = "block";
    inner_html = "<p><span id='modal_close_span' onclick='modelplus.dom.close_model_hidrograph_desc()'>×</span></p>";
    inner_html += "<p>" + msg_html + "</p>";
    div_modal_ctt.html(inner_html);
	
    GLB_keypress.prototype.keys[27] = function(){
      modelplus.dom.close_model_hidrograph_desc();
    };
  }

  /**
   *
   * RETURN - None. Changes are performed in the interface.
   */
  mpd.close_model_hidrograph_desc = function(){
    $("#modal_hidrograph_div").hide();
    delete GLB_keypress.prototype.keys[27];
  }

  /**
   *
   * RETURN - None. Changes are performed in the interface.
   */
  mpd.load_parameter_about = function(parameter_acronym, about_obj){
	var html_content;
	switch(parameter_acronym){
		case 'quni_usgs':
			html_content = "<strong>USGS Discharge Map</strong><br />";
			html_content += "Real time updated water discharge in each USGS flow gage.<br />";
			html_content += "For more information: <a href='http://waterwatch.usgs.gov/index.php?id=real&sid=w__kml' target='_blank'>access the website.</a> ";
			modelplus.main.display_message_block(html_content);
			break;
		default:
			// check if a select box exists for given menu_id
			var sel_input_id, representation_id, html_content, replaced_text;
			var json_representation, json_evaluation, json_obj;
			
			sel_input_id = "#np" + parameter_acronym + "_sel";
			if($(sel_input_id).length){
				representation_id = $(sel_input_id).val();
				json_representation = get_json_representation(representation_id);
				if (json_representation != null){
					if (json_representation.description != undefined){
						html_content = "<strong>"+json_representation.call_radio+"</strong><br />";
						html_content += json_representation.description;
						modelplus.main.display_message_block(html_content);
					} else {
						html_content = "<strong>"+json_representation.id+"</strong><br />";
						html_content += "No description available.";
						modelplus.main.display_message_block(html_content);
					}
				} else {
					// TODO - search for tools
					alert(representation_id + " is not a representation.");
				}
			} else {
				// 
				json_representation = get_json_representation(parameter_acronym);
				json_evaluation = get_json_evaluation(parameter_acronym);
				json_obj = null;
				if (json_representation != null){
					json_obj = json_representation;
				} else if(json_evaluation != null) {
					json_obj = json_evaluation;
				}

				if (json_obj == null) {
					html_content = "<strong>"+modelplus.main.get_clicked_about_label(about_obj)+"</strong><br />";
					html_content += "No description available.";
					modelplus.main.display_message_block(html_content);
				} else if (json_obj.description != undefined){
					var replaced_text, html_content;
					html_content = "<strong>"+modelplus.main.get_clicked_about_label(about_obj)+"</strong><br />";
					replaced_text = json_obj.description.replace(GLB_const.prototype.scrunsetid_tag, 
																 $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val());
					replaced_text = replaced_text.replace(GLB_const.prototype.scmodelid_tag, 
														  $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val());
					replaced_text = replaced_text.replace(GLB_const.prototype.screferenceid_tag, 
														  ""); // TODO - make this work
					replaced_text = replaced_text.replace(GLB_const.prototype.urlviewerbase_tag, 
														  modelplus.url.base_frontend_webservices);
					html_content += replaced_text;
					modelplus.main.display_message_block(html_content);
				} else {
					html_content = "<strong>"+json_obj.id+"</strong><br />";
					html_content += "No description available.";
					modelplus.main.display_message_block(html_content);
				}
			}
			break;
	}
  }

  /**
   *
   *
   */
  mpd.delete_current_parameter_title = function(){
    var div_comps_id = "#" + modelplus.ids.LEGEND_BOTTOM_MODELS_DIV;
    $(div_comps_id).remove;
  }

  /**
   * 
   * TODO - Make it be called
   * TODO - Make it flexible for the meta files
   */
  mpd.update_current_parameter_title = function(repr_id){
	var map_title = null;
	var sub_type = null;
	var div_comps_id = "#" + modelplus.ids.LEGEND_BOTTOM_MODELS_DIV;
	var div_comps_mdl1_id = "#" + modelplus.ids.LEGEND_BOTTOM_MODEL1_DIV;
	var div_comps_mdl2_id = "#" + modelplus.ids.LEGEND_BOTTOM_MODEL2_DIV;
	var div_comps_obj, div_comps_mdl1_obj, div_comps_mdl2_obj, leg_div_obj;
	var mdl_1_name, mdl_2_name;
	
	// add title
	modelplus.dom.update_legend_title(GLB_vars.prototype.get_legend_title(repr_id));
	
	// 
	div_comps_obj = $(div_comps_id);
	
	if(!is_menu_id_comparison_repr(repr_id)){
		
		// hide legend comparison model titles if they exist
		if (div_comps_obj.length > 0) {
			div_comps_obj.hide();
		}
		
		// move legend image bellow
		leg_div_obj = $("#" + modelplus.ids.LEGEND_BOTTOM_DIV);
		leg_div_obj.append($("#colorscalezoom"));
		
		$('#colorscalezoom').css({'margin-top':'1px'});
		
		return;
	}
	
	// get models names
	mdl_1_name = $('#' + modelplus.ids.MENU_MODEL_MAIN_SBOX).find(":selected").text();
	mdl_2_name = $('#' + modelplus.ids.MENU_MODEL_COMP_SBOX).find(":selected").text();
	
	// create comparisons title div if necessary
	div_comps_mdl1_obj = $("<div id='"+modelplus.ids.LEGEND_BOTTOM_MODEL1_DIV+"'></div>");
	div_comps_mdl2_obj = $("<div id='"+modelplus.ids.LEGEND_BOTTOM_MODEL2_DIV+"'></div>");
	if (div_comps_obj.length <= 0) {
		
		// add it to the dom
		div_comps_obj = $("<div id='"+modelplus.ids.LEGEND_BOTTOM_MODELS_DIV+"'></div>");
		
		// fill each
		div_comps_mdl1_obj.html(mdl_1_name);
		div_comps_mdl2_obj.html(mdl_2_name);
		
		// add each legend to the big div
		div_comps_obj.append(div_comps_mdl1_obj);
		div_comps_obj.append(div_comps_mdl2_obj);
		
		// add titles to the legend div
		leg_div_obj = $("#" + modelplus.ids.LEGEND_BOTTOM_DIV);
		leg_div_obj.append(div_comps_obj);
	} else {
		div_comps_obj.show();
		div_comps_mdl1_obj.html(mdl_1_name);
		div_comps_mdl2_obj.html(mdl_2_name);
	}
	
	// move legend image bellow
	leg_div_obj = $("#" + modelplus.ids.LEGEND_BOTTOM_DIV);
	leg_div_obj.append($("#colorscalezoom"));
	
	$('#colorscalezoom').css({'margin-top':'1px'});
  }

  /**
   *
   */
  mpd.create_modals = function(){
	
	// TODO - replace it
	var mdl_div = $("<div id='" + modelplus.ids.MODAL_DIV+ "'></div>");
	var mdl_ctt_div = $("<div id='modal_content_div'></div>");
	mdl_div.appendTo("body");
	mdl_ctt_div.appendTo(mdl_div);
	
	// TODO - replace it
	mdl_div = $("<div id='" + modelplus.ids.MODAL_HYDROGRAPH + "'></div>");
	mdl_ctt_div = $("<div id='" + modelplus.ids.MODAL_HYDROGRAPH_CONTENT + "'></div>");
	mdl_div.appendTo("body");
	mdl_ctt_div.appendTo(mdl_div);
	
	// use only this approach
	mdl_div = $("<div id='" + modelplus.ids.MODAL_HYDROGRAPH_IFISBASED + "'></div>");
	mdl_div.appendTo("body");
  }

  /**
   *
   *
   *
   */
  mpd.update_legend_title = function(legend_title){
	
	var div_leg_title_obj, leg_div_obj;
	
	// create object if necessary
	div_leg_title_obj = $("#" + modelplus.ids.LEGEND_BOTTOM_TITLE_DIV);
	if (div_leg_title_obj.length == 0){
		div_leg_title_obj = $("<div id='"+modelplus.ids.LEGEND_BOTTOM_TITLE_DIV+"'></div>");
		leg_div_obj = $("#" + modelplus.ids.LEGEND_BOTTOM_DIV);
		leg_div_obj.append(div_leg_title_obj);
	}
	
	div_leg_title_obj.html(legend_title);
  }
  
  /**
   * Everything that should occur when the user selects another runset.
   * RETURN - Null. Changes are performed in interface.
   */
  mpd.onchange_runset_main_sbox = function(){
    var main_runset_id, div_main_obj;
	
    main_runset_id = $('#'+modelplus.ids.MENU_RUNSET_SBOX).val();
	
    if(main_runset_id == ''){
      $("#" + modelplus.ids.MENU_RUNSET_ABOUT).hide();
      $("#" + modelplus.ids.MENU_MODEL_ABOUT).hide();
      div_main_obj = $("#" + modelplus.ids.MENU_MAIN_ALERT_DIV);
      div_main_obj.append(modelplus.labels.SELECT_MODEL);
      div_main_obj.show();
    } else {
      // $("#" + modelplus.ids.MENU_RUNSET_ABOUT).show();
      $("#" + modelplus.ids.MENU_RUNSET_ABOUT).hide();
	}
	
    // close dialogues possible (if open)
    modelplus.main.hide_message_block();
    modelplus.dom.close_model_hidrograph_desc();
	
    // hide current loaded map
    if ($("#np" + GLB_map_type).hasClass("npact")){
      reclick_id = "#np" + GLB_map_type;
      $("#np" + GLB_map_type).click();
    }
	
    modelplus.api.get_runset_result(main_runset_id)
      .then(function(json_data){
        var div_main_obj;
        var parsed_json = json_data[0];
        var glb = GLB_vars.prototype;

        // parse JSON content
        try{
          if (parsed_json == undefined) return;

          // set up variables
          glb.sc_runset = {
            "id":parsed_json.id,
            "title":parsed_json.title,
            "show_main":parsed_json.show_main,
            "timestamp_ini":parsed_json.timestamp_ini,
            "timestamp_end":parsed_json.timestamp_end
          };

        } catch(err) {
          console.log("Unable to parse '"+ json_data +"'. Error: " + err);
          return;
        }

        glb.sc_models = parsed_json.sc_model;
        glb.sc_model_combinations = parsed_json.sc_model_combination;
        glb.sc_references = parsed_json.sc_reference;
        glb.sc_representation = parsed_json.sc_representation;
        glb.sc_evaluation = parsed_json.sc_evaluation;
        glb.forecast_set = parsed_json.forecast_set;
        glb.comparison_matrix = parsed_json.comp_mtx;
        if ((typeof func_to_run !== 'undefined') && (func_to_run != null)){
          func_to_run();
        }
		glb.webmenu = parsed_json.web_menu;
			
		// set up functions
		glb.get_runset_ini = function(){
          if (glb.sc_runset.timestamp_ini !== undefined){
            return(parseInt(glb.sc_runset.timestamp_ini));
          } else {
            return(null);
          }
        }
        glb.get_runset_end = function(){
          if (glb.sc_runset.timestamp_end !== undefined)
            return(parseInt(glb.sc_runset.timestamp_end));
          else
            return(null);
        }
        glb.get_runset_timediff = function(){
          var timestamp_ini, timestamp_end;
          timestamp_ini = glb.get_runset_ini();
          timestamp_end = glb.get_runset_end();
          if((timestamp_ini != null) && (timestamp_end != null)){
            return(timestamp_end - timestamp_ini);
          } else {
            console.log("Someone is null: " + timestamp_ini + " or " + timestamp_end);
            return(null);
          }
        }

        // basic check
        if (Object.keys(glb.webmenu).length == 0){
          if ($('#'+modelplus.ids.MENU_RUNSET_SBOX).val() !== ""){
            alert("Missing meta files for menu.");
          }
        }

        modelplus.dom.populate_model_main_sbox();

        //
        if (this.runset_id == ''){
          div_main_obj = $("#" + modelplus.ids.MENU_MAIN_ALERT_DIV);
          div_main_obj.append(modelplus.labels.SELECT_RUNSET);
          div_main_obj.show();
        }
      });
  }
  
  /**
   * Fill main model select box with the content in 'GLB_vars.prototype.sc_models' variable.
   * RETURN - Null. Changes are performed in interface.
   */
  mpd.populate_model_main_sbox = function(){
    var cur_obj, cur_txt, gbl, mpi, mpd;
    gbl = GLB_vars.prototype;
    mpi = modelplus.ids;
    mpd = modelplus.dom;

    // clean previous content
    $('#'+mpi.MENU_MODEL_MAIN_SBOX).find('option').remove().end();

    // populate it with empty option
    cur_obj = $('#'+mpi.MENU_MODEL_MAIN_SBOX);
    cur_obj.append('<option value="" selected>Select...</option>');

    // populate it with models
    for (var i = 0; i < gbl.sc_models.length; i++){
      // ignore hidden models
      if (gbl.sc_models[i].show_main == "F"){ continue; }
      if (gbl.sc_models[i].show_main == false){ continue; }

      // add option
      cur_txt = '<option value="'+gbl.sc_models[i].id+'">' + 
                  gbl.sc_models[i].title + 
                '</option>';
      cur_obj.append(cur_txt);
    }

    // populate it with model combinations
    for (var i = 0; i < gbl.sc_model_combinations.length; i++){
      cur_txt = '<option value="' + gbl.sc_model_combinations[i].id + '">' + 
                  gbl.sc_model_combinations[i].title + 
                '</option>';
      cur_obj.append(cur_txt);
    }

    // define function to be run on change
    $('#'+mpi.MENU_MODEL_MAIN_SBOX).change(mpd.onchange_model_main_sbox);
    $('#'+mpi.MENU_MODEL_COMP_SBOX).change(mpd.onchange_model_comp_sbox);
    $('#'+mpi.MENU_MODEL_MAIN_SBOX).change();
  }
  
  /**
   * Everything that should occur when the user selects another main model.
   * RETURN - Null. Changes are performed in interface.
   */
  mpd.onchange_model_main_sbox = function(){
	var the_url;
	var main_model_id, runset_id;
	var cur_splitted_comparison_id, cur_txt, cur_obj;
	var reclick_id, added_comp_models;
	
	main_model_id = $('#'+modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
	runset_id = $('#'+modelplus.ids.MENU_RUNSET_SBOX).val();
	
	reclick_id = null;
	
	// close dialogues possible (if open)
	modelplus.main.hide_message_block();
	modelplus.dom.close_model_hidrograph_desc();
	
	// hide current loaded map
	if ($("#np" + GLB_map_type).hasClass("npact")){
		reclick_id = "#np" + GLB_map_type;
		$("#np" + GLB_map_type).click();
	}
	
	
	
	modelplus.api.get_model_result(runset_id, main_model_id)
      .then(function(json_data){
		
		var cur_html, cur_select_id, cur_select_obj, cur_select_html, cur_a_id, cur_a_obj;
		var cur_parameter_id, cur_parameter_name, cur_par_index;
		var cur_menu_item, cur_menu_repr, cur_repr_array;
		var div_main_obj, div_obj, div_comp_obj, div_eval_obj, div_comb_obj, div_hydr_obj;
		var sc_model_obj;
		var count_added;
		var glb = GLB_vars.prototype;
		var glb_opt_ids = GLB_opt_ids.prototype;
		
		if (json_data instanceof Array)
			sc_model_obj = json_data[0];
		else 
			sc_model_obj = json_data;
		
		// get and clean div containers
		div_main_obj = $("#"+modelplus.ids.MENU_MAIN_ALERT_DIV);
		div_main_obj.empty();
		div_main_obj.hide();
		
		div_obj = $("#"+modelplus.ids.MENU_MODEL_MAIN_SELEC_DIV);
		div_obj.empty();
		div_comp_obj = $("#"+modelplus.ids.MENU_MODEL_COMP_SELEC_DIV);
		div_comp_obj.empty();
		div_eval_obj = $("#"+modelplus.ids.MENU_MODEL_EVAL_SELEC_DIV);
		div_eval_obj.empty();
		div_comb_obj = $("#"+modelplus.ids.MENU_MODEL_COMB_PARAM_DIV);
		div_comb_obj.empty();
		div_hydr_obj = $("#"+modelplus.ids.MENU_MODEL_HYDR_PARAM_DIV);
		div_hydr_obj.empty();
		
		// basic check
		if ((typeof(sc_model_obj) !== 'undefined') && (
			(sc_model_obj.sc_representation_set != undefined) || (sc_model_obj.sc_evaluation_set != undefined) ||
			(sc_model_obj.sc_represcomb_set != undefined))){
			
			$("#" + modelplus.ids.MENU_MODEL_ABOUT).show();
					
			// build single model sub menu
			count_added = 0;
			// iterate over each 'single_model' element of 'web_menu' object
			for(var i = 0; i < glb.webmenu.single_model.length; i++){
					
				cur_menu_item = glb.webmenu.single_model[i];
				if(cur_menu_item.representation != undefined){
					// alert("Will try to show single '" + cur_menu_item["id"] + "'.");
				} else if(cur_menu_item.representations != undefined){

					cur_repr_array = new Array();
					for(var j = 0; j < cur_menu_item.representations.length; j++){
						cur_menu_repr = cur_menu_item.representations[j];
						// see if current sc_menu element (var cur_menu_repr) is in the models meta file description (var sc_model_obj)
						if((typeof(sc_model_obj.sc_representation_set) !== 'undefined') && 
								(sc_model_obj.sc_representation_set.indexOf(cur_menu_repr) != -1)){
							cur_repr_array.push(cur_menu_repr);
						}
					}
					if (cur_repr_array.length <= 0){
						// alert("ignoring " + cur_menu_item["id"]);
					} else if (cur_repr_array.lenght == 1){
						// alert("radio for " + cur_menu_item["id"]);
					} else {
						// alert("select for " + cur_menu_item["id"] + " ("+cur_repr_array.lenght+", "+cur_repr_array+")");
							
						cur_html = '<div style="display:inline-block; width:100%">';
							
						// build link
						cur_a_id = 'np'+cur_menu_item["id"];
						cur_html += '<a href="#" id="'+cur_a_id+'" class="tabrain" style="width:90px">';
						cur_html += cur_menu_item["call_select"];
						cur_html += '</a >';
							
						// build select box
							
						cur_select_id = 'np'+cur_menu_item["id"]+'_sel';
						cur_html += "<select class='sbox' id='"+cur_select_id+"' onchange='modelplus.dom.onchange_representation_select_option(\""+cur_a_id+"\")'>";
						for(var j=0; j < cur_repr_array.length; j++){
							cur_html += "<option value='"+cur_repr_array[j]+"'>";
							cur_html += GLB_vars.prototype.get_representation_call_select(cur_repr_array[j]);
							cur_html += "</option>";
						}
						cur_html += "</select>";
						
						cur_html += '<img src="' + modelplus.viewer.image_folder + 'question_mark3.png" class="qicon" onclick="modelplus.dom.load_parameter_about(' + cur_menu_item["id"] + ', $(this))" />';
							
						// cur_html += '<input type="hidden" id="npmono'+i+'_sel" value="'+cur_parameter_id+'" />';
						cur_html += '</div>';
						
						div_obj.append(cur_html);
						count_added++;
					}
				} else {
					alert("Unable to determine '" + cur_menu_item["id"] + "'.");
				}
			}
			// add no-available message
			if(count_added == 0){
				div_obj.append(modelplus.labels.NO_REPRESENTATION + "!");
				$("#" + modelplus.ids.MENU_MODEL_MAIN_RADIO_DIV).hide();
				div_obj.hide();
			} else {
				$("#" + modelplus.ids.MENU_MODEL_MAIN_RADIO_DIV).show();
				if($("#" + 'np' + glb_opt_ids.mono_group).hasClass("npact")){
					div_obj.show();
				} else {
					div_obj.hide();
				}
			}
			
			// build comparison sub menu
			// TODO - count it properly
			if(count_added == 0){
				$("#" + modelplus.ids.MENU_MODEL_COMP_RADIO_DIV).hide();
				div_comp_obj.hide();
			} else {
				$("#" + modelplus.ids.MENU_MODEL_COMP_RADIO_DIV).show();
				if($("#" + 'np' + glb_opt_ids.comp_group).hasClass("npact")){
					div_comp_obj.show();
				} else {
					div_comp_obj.hide();
				}
			}
			
			// build evaluation sub menu
			count_added = 0;
			
			var cur_raw_eval_id, cur_eval_ref, cur_reference_json, cur_ref_title;
			
			for(var i = 0; i < glb.webmenu.evaluation.length; i++){
				cur_menu_item = glb.webmenu.evaluation[i];
				if((cur_menu_item.evaluation != undefined) && (typeof(sc_model_obj.sc_evaluation_set) !== 'undefined')){
					
					for(var j=0; j < sc_model_obj.sc_evaluation_set.length; j++){
						
						// separates evaluation_id from reference
						cur_raw_eval_id = sc_model_obj.sc_evaluation_set[j].split("_")[0];
						cur_eval_ref = sc_model_obj.sc_evaluation_set[j].split("_")[1];
						
						if (cur_raw_eval_id == cur_menu_item.evaluation){
							// alert(cur_raw_eval_id + " == " + cur_menu_item.evaluation);
							
							// search evaluation raw (without related reference)
							cur_html = '<div style="display:inline-block; width:100%">';
							
							// define reference acronym
							cur_reference_json = get_json_reference(cur_eval_ref);
							if (typeof(cur_reference_json["title_acronym"]) !== 'undefined'){
								cur_ref_title = cur_reference_json["title_acronym"];
							} else {
								cur_ref_title = cur_reference_json["title"];
							}
								
							// build link
							cur_a_id = 'np'+cur_menu_item.id + "_" + cur_eval_ref;
							cur_html += '<a href="#" id="'+cur_a_id+'" class="tabrain" style="width:220px">';
							cur_html += cur_menu_item.call_radio + " (" + cur_ref_title + ")";
							cur_html += '</a >';
							cur_html += '<img src="' + modelplus.viewer.image_folder + 'question_mark3.png" class="qicon" onclick="modelplus.dom.load_parameter_about(\'' + cur_menu_item.id + '\', $(this))" />';
							cur_html += '</div>';
							
							div_eval_obj.append(cur_html);
							count_added++;
						} else {
							// alert(cur_raw_eval_id + " != " + cur_menu_item.evaluation + " (" + sc_model_obj.sc_evaluation[j] + ")");
						}
					}

				} else if(cur_menu_item.evaluations != undefined){
					// alert("Will try to show multiple for " + cur_menu_item.id);
				} else {
					// alert("Hey");
				}
				 
			}
			// add no-available message
			if(count_added == 0){
				div_eval_obj.append(modelplus.labels.NO_EVALUATIONS);
				$("#" + modelplus.ids.MENU_MODEL_EVAL_RADIO_DIV).hide();
				div_eval_obj.hide();
			} else {
				$("#" + modelplus.ids.MENU_MODEL_EVAL_RADIO_DIV).show();
				if($("#" + 'np' + glb_opt_ids.eval_group).hasClass("npact")){
					div_eval_obj.show();
				} else {
					div_eval_obj.hide();
				}
			}
			
			// building hydrograph menu
			if (glb.webmenu.hydrograph !== undefined){
				var num_radios_added = 0;
				
				for(var i = 0; i < glb.webmenu.hydrograph.length; i++){
					
					// build guiding dictionary
					var all_hydrog_options = {};
					cur_menu_item = glb.webmenu.hydrograph[i];
					if(cur_menu_item.evaluation != undefined){
						if (typeof(sc_model_obj.sc_evaluation_mdl) !== 'undefined'){
							var eval_options = {};
							for (var i = 0; i < sc_model_obj.sc_evaluation_mdl.length; i++) {
								var the_splitted = sc_model_obj.sc_evaluation_mdl[i].split("_");
								
								// check if it is it
								if(the_splitted[0] != cur_menu_item.evaluation){ continue; }
								console.log("Looking for '"+the_splitted[0]+"' in: " + JSON.stringify(cur_menu_item.evaluation));
								
								// add to dictionary
								if(!(the_splitted[0] in all_hydrog_options)){
									all_hydrog_options[the_splitted[0]] = []; 
								}
								// alert("Pushing "+ the_splitted[1] + "_" + the_splitted[2] +" to " + all_hydrog_options[the_splitted[0]]);
								all_hydrog_options[the_splitted[0]].push(the_splitted[1] + "_" + the_splitted[2]);
							}
						} else {
							
						}
					} else {
						console.log("cur_menu_item["+i+"] has: " + JSON.stringify(cur_menu_item));
					}
				
					// basic check - at least one found
					if (all_hydrog_options.length == 0){
						continue;
					}
				
					for (var cur_eval_id in all_hydrog_options) {
						
						// build link
						cur_a_id = 'np'+cur_menu_item.id;
						cur_html = '<a href="#" id="'+cur_a_id+'" class="tabrain" style="width:105px; margin-right:0px;">';
						cur_html += cur_menu_item.call_modref_radio;
						cur_html += '</a >';
						
						// build select box
						cur_select_id = cur_a_id + "_sel";
						cur_html += "<select class='sbox' id='"+cur_select_id+"' onchange='modelplus.dom.onchange_representation_select_option(\""+cur_a_id+"\")' style='margin-left:0px; margin-right:0px;'>";
						for(var j=0; j < all_hydrog_options[cur_eval_id].length; j++) {
							cur_splitted = all_hydrog_options[cur_eval_id][j].split("_");
							cur_ref_json_obj = get_json_reference(cur_splitted[0]);
							cur_mdl_json_obj = get_json_model(cur_splitted[1]);
							cur_ref_acronym = cur_ref_json_obj["title_acronym"];
							cur_mdl_acronym = cur_mdl_json_obj["title_acronym"];
							
							cur_html += '<option value="'+all_hydrog_options[cur_eval_id][j]+'">';
							cur_html += cur_mdl_acronym + "/" + cur_ref_acronym;
							cur_html += '</option>';
						}
						cur_html += '</select>';
						
						// build link
						cur_html += '<img src="' + modelplus.viewer.image_folder + 'question_mark3.png" class="qicon" onclick="modelplus.dom.load_parameter_about(\'' + cur_menu_item.id + '\', $(this))" />';
						cur_html += '</div>';
						
						// add to HTML
						div_hydr_obj.append(cur_html);
						num_radios_added += 1;
					}
				}
				
				// 
				if(num_radios_added == 0){
					$("#" + modelplus.ids.MENU_MODEL_HYDR_RADIO_DIV).hide();
					$("#" + modelplus.ids.MENU_MODEL_HYDR_PARAM_DIV).hide();				
				} else {
					$("#" + modelplus.ids.MENU_MODEL_HYDR_RADIO_DIV).show();
					if($("#" + 'np' + glb_opt_ids.hydr_group).hasClass("npact")){
						$("#" + modelplus.ids.MENU_MODEL_HYDR_PARAM_DIV).hide();
					} else {
						$("#" + modelplus.ids.MENU_MODEL_HYDR_PARAM_DIV).hide();
					}
				}
			} else {
				console.log("GLB_vars.prototype.webmenu.hydrograph is undefined.");
			}
			
			// 
			modelplus.dom.build_menu_combination(glb.webmenu, 
			                                     sc_model_obj,
												 div_comb_obj);
			div_comb_obj.hide();
			
			// 
			if(reclick_id != null){
				$(reclick_id).click();
			}
			
			$("#" + modelplus.ids.MENU_MODEL_ABOUT).show();
			
		} else if ((sc_model_obj !== undefined) && (sc_model_obj.ERROR !== 'undefined')) {
		
			if (this.runset_id == ''){
				div_main_obj.append(modelplus.labels.SELECT_RUNSET);
			} else {
				$("#" + modelplus.ids.MENU_MODEL_ABOUT).hide();
				div_main_obj.append(modelplus.labels.SELECT_MODEL);
			}
			div_main_obj.show();
			
			$("#" + modelplus.ids.MENU_MODEL_MAIN_RADIO_DIV).hide();
			div_obj.hide();
			$("#" + modelplus.ids.MENU_MODEL_COMP_RADIO_DIV).hide();
			div_comp_obj.hide();
			$("#" + modelplus.ids.MENU_MODEL_EVAL_RADIO_DIV).hide();
			div_eval_obj.hide();
			$("#" + modelplus.ids.MENU_MODEL_COMB_RADIO_DIV).hide();
			div_comb_obj.hide();
			$("#" + modelplus.ids.MENU_MODEL_HYDR_RADIO_DIV).hide();
			$("#" + modelplus.ids.MENU_MODEL_HYDR_PARAM_DIV).hide();
			
		} else {
			
			div_main_obj.hide();
			
			$("#" + modelplus.ids.MENU_MODEL_MAIN_RADIO_DIV).hide();
			div_obj.hide();
			$("#" + modelplus.ids.MENU_MODEL_COMP_RADIO_DIV).hide();
			div_comp_obj.hide();
			$("#" + modelplus.ids.MENU_MODEL_EVAL_RADIO_DIV).hide();
			div_eval_obj.hide();
			$("#" + modelplus.ids.MENU_MODEL_COMB_RADIO_DIV).hide();
			div_comb_obj.hide();
			$("#" + modelplus.ids.MENU_MODEL_HYDR_RADIO_DIV).hide();
			$("#" + modelplus.ids.MENU_MODEL_HYDR_PARAM_DIV).hide();
			
			console.log("Hiding 'about model' button.");
			$("#" + modelplus.ids.MENU_MODEL_ABOUT).hide();
		}
		
	  });
	
	
	cur_obj = $('#'+modelplus.ids.MENU_MODEL_COMP_SBOX);
	
	// clean comparison model select box and add 'empty' model
	cur_obj.find('option').remove().end();
	cur_txt = '<option value="" selected>Select...</option>';
	cur_obj.append(cur_txt);
	
	// list all comparisons of this model and updates comparison model select box
	added_comp_models = 0;
	for (var i = 0; i < GLB_vars.prototype.comparison_matrix.length; i++){
		cur_splitted_comparison_id = GLB_vars.prototype.comparison_matrix[i].id.split("_");
		
		if (cur_splitted_comparison_id.length != 2){ continue; }  // base check
		
		if (cur_splitted_comparison_id[0] == main_model_id){
			cur_txt = '<option value="'+cur_splitted_comparison_id[1]+'">' + 
						modelplus.dom.get_model_name(cur_splitted_comparison_id[1]) + 
					'</option>';
			cur_obj.append(cur_txt);
			added_comp_models = added_comp_models + 1;
		}
	}
	
	// if no comparison was added, hide such options
	if(added_comp_models == 0){
		$("#" + modelplus.ids.MENU_MODEL_MAIN_RADIO_DIV).hide();
		$("#" + modelplus.ids.MENU_MODEL_COMPMST_SELEC_DIV).hide();
	} else {
		$("#" + modelplus.ids.MENU_MODEL_MAIN_RADIO_DIV).show();
		if($("#" + 'np' + GLB_opt_ids.prototype.comp_group).hasClass("npact")){
			$("#" + modelplus.ids.MENU_MODEL_COMPMST_SELEC_DIV).show();
		} else {
			$("#" + modelplus.ids.MENU_MODEL_COMPMST_SELEC_DIV).hide();
		}
	}
	
	// define function to be run on change of comparison select box
	$('#'+modelplus.ids.MENU_MODEL_COMP_SBOX).change();
	
	// show or hide realtime tools
	var usgs_map_id, usgs_map_div_obj;
	usgs_map_id = "div"+opt_tool_us_map;
	usgs_map_div_obj = $("#"+usgs_map_id);
	if ((runset_id == "")||(runset_id == "realtime")){
		usgs_map_div_obj.show();
	} else {
		usgs_map_div_obj.hide();
	}
  }
  
  /**
   * AAA
   * webmenu = 
   */
  mpd.build_menu_combination = function(webmenu, 
                                                  sc_model_obj, 
												  div_comb_obj){
    var menu_reprcomb_id, i, cur_represcomb, cur_menu_item;
    var cur_html, cur_a_id, count_reprcomb, st;

    // basic check
	if ((webmenu.combination == undefined) || 
	    (sc_model_obj.sc_represcomb_set == undefined)){
      $("#" + modelplus.ids.MENU_MODEL_COMB_RADIO_DIV).hide();
      return;
    }
	
	count_reprcomb = 0;
    for(i = 0; i < webmenu.combination.length; i++){
      cur_menu_item = webmenu.combination[i];
      if(cur_menu_item.reprcomb != undefined){
        menu_reprcomb_id = cur_menu_item.reprcomb;
        for(cur_represcomb in sc_model_obj.sc_represcomb_set){

          if (menu_reprcomb_id == cur_represcomb){
							
            // search evaluation raw (without related reference)
            cur_html = '<div style="display:inline-block; width:100%">';

            // build link
            cur_a_id = 'np'+cur_menu_item.id;
            cur_html += '<a href="#" id="'+cur_a_id+'" class="tabrain" style="width:220px">';
            cur_html += cur_menu_item.call_radio;
            cur_html += '</a >';
            cur_html += '<img src="' + modelplus.viewer.image_folder + 'question_mark3.png" class="qicon" onclick="modelplus.dom.load_parameter_about(\'' + cur_menu_item.id + '\', $(this))" />';
            cur_html += '</div>';
								
            // add to menu and count
            div_comb_obj.append(cur_html);
								
            // add search field if necessary
			st = cur_menu_item.search_tool;
            if((st != undefined) && (st.type != undefined)){
              mpd.build_menu_combination_search(div_comb_obj, 
                                                st.type, 
                                                cur_menu_item.id);
            }

            // count it
            count_reprcomb = count_reprcomb + 1;
          }
        }
       } else {
        console.log("No 'reprcomb' in " + JSON.stringify(cur_menu_item));
      }
    }

    // show/hide
    if (count_reprcomb > 0){
      $("#" + modelplus.ids.MENU_MODEL_COMB_RADIO_DIV).show();
    } else {
      $("#" + modelplus.ids.MENU_MODEL_COMB_RADIO_DIV).hide();
    }
  }
  
  /**
   *
   * div_comb_obj: 
   * search_type:
   * RETURN - 
   */
  mpd.build_menu_combination_search = function(div_comb_obj, search_type, id){
    var div_obj, txt_obj, but_obj;

    // basic check
    if(search_type == "none") return;

    if (search_type == "on_click"){
		
      // create text
      txt_obj = document.createElement("input");
	  txt_obj.setAttribute("type", "text");
	  txt_obj.setAttribute("class", "ihmis_search_short");
	  txt_obj.setAttribute("placeholder", "Search...");
	  
	  // create button
	  but_obj = document.createElement("input");
	  but_obj.setAttribute("type", "button");
	  but_obj.setAttribute("class", "ihmis_search");
	  but_obj.setAttribute("value", "Search");
	  but_obj.onclick = function() {
        var search_val = this.parentNode.firstChild.value;
        custom_search(search_val);
      };
	  
	  // create hidden containing div
	  div_obj = document.createElement("div");
	  div_obj.setAttribute("id", id+"_search");
	  div_obj.append(txt_obj);
	  div_obj.append(but_obj);
	  div_obj.style.display = "none";
	  
    } else if (search_type == "on_type"){
      // create text
      txt_obj = document.createElement("input");
	  txt_obj.setAttribute("type", "text");
	  txt_obj.setAttribute("class", "ihmis_search_large");
	  txt_obj.setAttribute("placeholder", "Search...");
	  txt_obj.oninput = function() {
        var search_val = this.parentNode.firstChild.value;
        custom_search(search_val);
      };
	  
	  // create hidden containing div
	  div_obj = document.createElement("div");
	  div_obj.setAttribute("id", id+"_search");
	  div_obj.append(txt_obj);
	  div_obj.style.display = "none";
    }

	div_comb_obj.append(div_obj);
  }
  
  /**
   * Function to be executed when comparison select box is changed.
   * RETURN - null. Changes are performed in interface.
   */
  mpd.onchange_model_comp_sbox = function(){
	var main_model_id, comp_model_id;
	var div_obj, all_params_id, cur_html;
	var cur_par_index;
	var count_added;
	var glb = GLB_vars.prototype;
	
	// getting html objects references
	main_model_id = $('#'+modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
	comp_model_id = $('#'+modelplus.ids.MENU_MODEL_COMP_SBOX).val();
	div_obj = $('#'+modelplus.ids.MENU_MODEL_COMP_SELEC_DIV);
	
	// close dialogues possible (if open)
	modelplus.main.hide_message_block();
	modelplus.dom.close_model_hidrograph_desc();
	
	// clean div content and abort if necessary
	div_obj.empty();
	if (comp_model_id == ''){return;}
	
	// fill it with parameters of comparison matrix
	all_representations_id = glb.get_comparison_parameters_id(main_model_id, comp_model_id);
	
	// iterate over each 'single_model' element of 'web_menu' object
	count_added = 0;
	for(var i = 0; i < glb.webmenu.comparison_model.length; i++){
					
		cur_menu_item = glb.webmenu.comparison_model[i];
		// alert("Comparison mdl: " + cur_menu_item);
		
		if(cur_menu_item.representation != undefined){
			// alert("Will try to show single '" + cur_menu_item["id"] + "'.");
		} else if(cur_menu_item.representations != undefined){
			// alert("Will try to show select '" + cur_menu_item["id"] + "'.");
			cur_repr_array = new Array();
			for(var j = 0; j < cur_menu_item.representations.length; j++){
				cur_menu_repr = cur_menu_item.representations[j];
				// see if current sc_menu element (var cur_menu_repr) is in the models meta file description (var sc_model_obj)
				if(all_representations_id.indexOf(cur_menu_repr) != -1){
					cur_repr_array.push(cur_menu_repr);
				}
			}
			
			// if there is something to be presented in that select box, present it
			if (cur_repr_array.length <= 0){
				// alert("ignoring " + cur_menu_item["id"]);
			} else if (cur_repr_array.lenght == 1){
				// alert("radio for " + cur_menu_item["id"]);
			} else {
				// alert("select for " + cur_menu_item["id"] + " ("+cur_repr_array.lenght+", "+cur_repr_array+")");
							
				cur_html = '<div style="display:inline-block; width:100%">';
						
				// build link
				cur_a_id = 'np'+cur_menu_item["id"];
				cur_html += '<a href="#" id="'+cur_a_id+'" class="tabrain" style="width:90px">';
				cur_html += cur_menu_item["call_select"];
				cur_html += '</a >';
							
				// build select box
							
				cur_select_id = 'np'+cur_menu_item["id"]+'_sel';
				cur_html += "<select class='sbox' id='"+cur_select_id+"' onchange='modelplus.dom.onchange_representation_select_option(\""+cur_a_id+"\")'>";
				for(var j=0; j < cur_repr_array.length; j++){
					cur_html += "<option value='"+cur_repr_array[j]+"'>";
					cur_html += glb.get_representation_call_select(cur_repr_array[j]);
					cur_html += "</option>";
				}
				cur_html += "</select>";
						
				cur_html += '<img src="' + modelplus.viewer.image_folder + 'question_mark3.png" class="qicon" onclick="modelplus.dom.load_parameter_about(' + cur_menu_item["id"] + ', $(this))" />';
							
				// cur_html += '<input type="hidden" id="npmono'+i+'_sel" value="'+cur_parameter_id+'" />';
				cur_html += '</div>';
						
				div_obj.append(cur_html);
				count_added++;
			}
		} else {
			alert("Unable to determine '" + cur_menu_item["id"] + "'.");
		}		
	
	}
	
	// add no-available message
	if(count_added == 0){
		div_obj.append(modelplus.labels.NO_REPRESENTATION + "|");
	} else {
		div_obj.show();
	}
	
	// debug
	/*
	alert("There are " + all_params_id.length + " comparisons.");
	for(var i=0; i < all_params_id.length; i++){
		alert("Comp. parameter: " + all_params_id[i] + ".");
	}
	*/

	/*
	GLB_menugroup_ids.prototype.clean_flags(GLB_menugroup_ids.prototype.varscomp_flags);
	for(var i = 0; i < all_params_id.length; i++){
		GLB_menugroup_ids.prototype.set_flag(all_params_id[i],
											 GLB_menugroup_ids.prototype.varscomp_flags,
											 GLB_menugroup_ids.prototype.vars_map);
	}
	
	for(var i=0; i < GLB_menugroup_ids.prototype.varscomp_flags.length; i++){
		if (count_true(GLB_menugroup_ids.prototype.varscomp_flags[i]) > 1){
			cur_html = '<div style="display:inline-block; width:100%">';
			cur_html += '<a href="#" id="npcomp'+i+'" class="tabrain" style="width:120px">'+GLB_menugroup_ids.prototype.vars_label[i]+'</a>';
			cur_html += "<select class='sbox'>";
			for(var j=0; j < GLB_menugroup_ids.prototype.varscomp_flags[i].length; j++){
				if (GLB_menugroup_ids.prototype.varscomp_flags[i][j]){
					cur_html = cur_html + "<option>"+GLB_menugroup_ids.prototype.vars_map[i][j]+"</option>";
				}
			}
			cur_html = cur_html + "</select></div>";
			div_obj.html(div_obj.html() + cur_html);
		} else if (count_true(GLB_menugroup_ids.prototype.varscomp_flags[i]) == 1){
			cur_par_index = index_true(GLB_menugroup_ids.prototype.varscomp_flags[i]);
			cur_parameter_name = GLB_vars.prototype.get_parameter_name(GLB_menugroup_ids.prototype.vars_map[i][cur_par_index]);
			cur_html = '<div style="display:inline-block; width:100%">';
			cur_html += '<a href="#" id="npcomp'+i+'" class="tabrain" style="width:120px">'+cur_parameter_name+'</a>';
			cur_html += '</div>';
			div_obj.html(div_obj.html() + cur_html);
		}
	}
	*/
  }
  
  /**
   *
   * type: Menu id
   * RETURN - True if the type is related to an evaluation, False otherwise
   */
  modelplus.dom.uncheck_other_evaluations = function(type){
	var div_eval_obj, div_eval_children;
	var clicked_element_id, displayed;
	var cur_removed_type;
	
	clicked_element_id = "np" + type;
	
	// list all elements inside evaluation div
	div_eval_obj = $("#"+modelplus.ids.MENU_MODEL_EVAL_SELEC_DIV);
	div_eval_children = div_eval_obj.find("a");
	
	displayed = modelplus.main.get_displayed_representation();
	
	// for each listed element uncheck it if it is different from what we have now
	div_eval_children.each(function () {
		if((this.id != clicked_element_id) && ($(this).hasClass("npact"))){
			cur_removed_type = this.id.substring(2);
			hide_custom_display(cur_removed_type);
			$(this).removeClass("npact");
		}
	});
  }
  
  /**
   *
   * group_a_id -
   * RETURN -
   */
  modelplus.dom.onchange_representation_select_option = function(group_a_id){
	GLB_ifisrain_callback.prototype.was_sel_change = true;
	if($("#"+group_a_id).hasClass("npact")){
      $("#"+group_a_id).click();
      $("#"+group_a_id).click();
	}
  }
  
  /**
   * Removes from exhibition all elements from place calling hide_custom_display.
   * type - Element clicked. Expected to start with 'np'.
   * param_div_id - Id of divi with select boxes. Usually it is in "modelplus.ids.MENU_MODEL_..._PARAM_DIV"
   * RETURN - None. Changes performed in interface.
   */
  modelplus.dom.uncheck_other_custom_display = function(clicked_element_id, param_div_id){
	var div_hydr_obj, div_hydr_children, cur_removed_type;
	
	// list all elements inside param div
	div_hydr_obj = $("#" + param_div_id);
	div_hydr_children = div_hydr_obj.find("a");
	
	// for each listed element uncheck it if it is different from what we have now
	div_hydr_children.each(function () {
		if((this.id != clicked_element_id) && ($(this).hasClass("npact"))){
			cur_removed_type = this.id.substring(2);
			hide_custom_display(cur_removed_type);
			$(this).removeClass("npact");
		}
	});
  }
  
  /**
   *
   * type - 
   * RETURN - None. Changes are performed in interface.
   */
  modelplus.dom.uncheck_all_other_custom_displays = function(type){
	var clicked_element_id, param_div_idx;
	var cleaned_param_div_ids;
	
	clicked_element_id = 'np' + type;
	
	cleaned_param_div_ids = [modelplus.ids.MENU_MODEL_EVAL_SELEC_DIV,
							 modelplus.ids.MENU_MODEL_COMB_PARAM_DIV,
							 modelplus.ids.MENU_MODEL_HYDR_PARAM_DIV];
							 
	for(param_div_idx=0; param_div_idx < cleaned_param_div_ids.length; param_div_idx++){
		modelplus.dom.uncheck_other_custom_display(clicked_element_id, cleaned_param_div_ids[param_div_idx]);
	}
  }
  
  /***-------------------------------------------- DOM MAP LEGEND FUNCS -------------------------------------------***/
  
  /**
   * Display legend on top of the map.
   * display_id: 
   * innter_html: 
   * RETURN: Null.
   */
  modelplus.dom.show_legend_top = function(display_id, innter_html){

     // create div object
     var div_obj = $('<div>', {
       id:modelplus.ids.LEGEND_TOP_DIV
     });
     div_obj.html(innter_html);
     
     // create hidden object
     var div_hid = $('<input>');
     div_hid.attr({
       id: modelplus.ids.LEGEND_TOP_HID,
       type: 'hidden',
       value: display_id
     });
     div_obj.append(div_hid);
     
     // add to the body
     $("body").append(div_obj);
  }
  
  /**
   * If the TOP legend is on, hide / destroy it
   * display_id:
   * RETURN: Null.
   */
  modelplus.dom.hide_legend_top = function(display_id){
    var top_legend_obj;
    
    // basic checks
    if ($("#"+modelplus.ids.LEGEND_TOP_HID).length <= 0 )
      return;
    if ($("#"+modelplus.ids.LEGEND_TOP_HID).val() != display_id)
      return;
      
    // hide and destroy it
    top_legend_obj = $("#"+modelplus.ids.LEGEND_TOP_DIV);
    top_legend_obj.hide();
    top_legend_obj.remove();
  }
  
  
  
  /***----------------------------------------------- DOM GET FUNCS -----------------------------------------------***/
  
  var mpd = modelplus.dom;
  
  /**
   * 
   * RETURN - The name of the model if it was found, 'null' otherwise.
   */
  modelplus.dom.get_model_name = function(model_id){
    var i;
	var glb = GLB_vars.prototype;
    for (i = 0; i < glb.sc_models.length; i++){
      if (glb.sc_models[i].id == model_id){
        return(glb.sc_models[i].title);
      }
    }
    return(null);
  }
  
  /**
   *
   * model_forecast_id -
   * RETURN -
   */
  mpd.get_forecast_model_name = function(model_forecast_id){
    // TODO it
    var s_id, f_i, cur_s_o, cur_f_o;
    var glb = GLB_vars.prototype;

    // search for the state that has the searched forecast
    for(s_id in glb.forecast_set){
      cur_s_o = glb.forecast_set[s_id];
      if(cur_s_o.scenarios.hasOwnProperty(model_forecast_id)){
        cur_f_o = cur_s_o.scenarios[model_forecast_id];
        return(cur_s_o.title + ":" + cur_f_o.title);
      }
    }
	return(null);
  }
  
  /**
   *
   * sc_model_id -
   * RETURN -
   */
  modelplus.dom.get_json_model = function(sc_model_id){
	for (var i = 0; i < GLB_vars.prototype.sc_models.length; i++){
		if (GLB_vars.prototype.sc_models[i].id == sc_model_id){
			return(GLB_vars.prototype.sc_models[i]);
		}
	}
	return(null);
  }

})();
 
/******************************************************* FUNCS *******************************************************/

/**
 * GENERAL FUNCTION
 * boolean_array - 
 * RETURN - Number of 'True' values in given array
 */
function count_true(boolean_array){
	var count_t = 0;
	for(var i=0; i < boolean_array.length; i++){
		if (boolean_array[i]) {count_t = count_t + 1;}
	}
	return(count_t);
}

/**
 * GENERAL FUNCTION
 * boolean_array -
 * RETURN -
 */
function index_true(boolean_array){
	for(var i=0; i < boolean_array.length; i++){
		if (boolean_array[i]) {return(i);}
	}
	return(-1);
}

/**
 * Verify if, for a given menu id, the interface should load IFIS Rain.
 * type: Menu id
 * RETURN - True if the type is related to a ifis rain map, False otherwise
 */
function is_ifis_rain(type){
	var is_numeric;
	is_numeric = !isNaN(type);
	return(is_numeric);
}

/**
 *
 * type: Menu id
 * RETURN - True if the type is related to an evaluation, False otherwise
 */
function is_evaluation(type){
	var cur_eval_menu_item;
	var type_splitted;
	
	// first check
	if(type.indexOf('_') == -1){ return(false); }
	
	// split and get first
	type_splitted = type.split("_");
	
	// check if selected is in list of evaluations
	for(var i = 0; i < GLB_vars.prototype.webmenu.evaluation.length; i++){
		cur_eval_menu_item = GLB_vars.prototype.webmenu.evaluation[i];
		if(cur_eval_menu_item.evaluation != undefined){
			if(type_splitted[0] == cur_eval_menu_item.evaluation){
				return(true);
			}
		}
	}
	
	return(false);
}

/**
 *
 * type: Menu id
 * RETURN - True if the type is related to an evaluation with select box, False otherwise
 */
function is_hydrograph(type){
	
	// first check
	if(type.indexOf('_') != -1){ return(false); }
	
	// second check
	if (GLB_vars.prototype.webmenu.hydrograph == undefined){ 
		console.log("No entry for hydrograph in menu.");
		return(false);
	}
	
	// check if selected is in list of evaluations
	for(var i = 0; i < GLB_vars.prototype.webmenu.hydrograph.length; i++){
		cur_eval_menu_item = GLB_vars.prototype.webmenu.hydrograph[i];
		if(cur_eval_menu_item.evaluation != undefined){
			if(type == cur_eval_menu_item.evaluation){
				return(true);
			}
		}
	}
	return(false);
}

/**
 *
 * type:
 * RETURN :
 */
function is_comparison_modelcomb(type){
	"use strict";
	
	var checked_obj, grandparent_obj;
	
	// first check
	checked_obj = $("#np"+type);
	grandparent_obj = checked_obj.parent().parent();
	if(grandparent_obj.attr("id") == modelplus.ids.MENU_MODEL_COMB_PARAM_DIV){
		return(true);
	} else {
		return(false);
	}
}

/**
 *
 * type: 
 * RETURN -
 */
function is_representation_combined(type){
	var cur_reprcomb_menu_item;
	
	// is a representation combined if it is not a number and has no underline
	if ((type.indexOf('_') == -1)&&(isNaN(type))){
		return(true);
	} else {
		return(false);
	}
}

/**
 * Uses AJAX to retrieve the most recent timestamp available and build arguments for IFIS_Rain object.
 * the_id - Id of clicked element.
 * RETURN - None. Changes are performed on user interface.
 */
function load_ifis_rain(the_id, vis){
	var value_element_id, prefix, sc_runset_id;
	var image_ifisrain_folder_path, image_ifisrain_suffix;
	var sc_model1_id, sc_model2_id, sc_representation_id; 
	var ifis_rain_callback;
	var runset_time_interval;
	var legend_url;
	
	// some constants
	var gbl_cbk = GLB_ifisrain_callback.prototype;
	gbl_cbk.design_sc = 11;                                                            // TODO - make it come from meta files
	gbl_cbk.design_rt = 5;                                                             // TODO - make it come from meta files
	
	// get parameter id that is going to be shown
	/*
	value_element_id = "np"+the_id+"_sel";
	sc_representation_id = $("#"+value_element_id).val();
	*/
	sc_representation_id = screpresentationid_from_scmenuid(the_id);
	
	prefix = the_id.substring(0, 2);
	
	sc_runset_id = $('#'+modelplus.ids.MENU_RUNSET_SBOX).val();
	sc_model1_id = $('#'+modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
	
	if(($('#'+modelplus.ids.MENU_MODEL_COMP_SBOX).length) && 
	   ($('#np'+GLB_opt_ids.prototype.comp_group).hasClass("npact"))){
	    sc_model2_id = $('#'+modelplus.ids.MENU_MODEL_COMP_SBOX).val();
		if (sc_model2_id == "") { sc_model2_id = null; }
	} else {
		sc_model2_id = null;
	}
	
	// build arguments object
	gbl_cbk.call = function(last_timestamp){
		var check_before, check_after;
		
		gbl_cbk.ref_timestamp0 = last_timestamp;
		check_before = $("#np" + gbl_cbk.id).hasClass("npact");
		ifis_rain_maps(gbl_cbk.vis, gbl_cbk.type);
		check_after = $("#np" + gbl_cbk.id).hasClass("npact");
		
		if (check_before != check_after){
			$("#np" + gbl_cbk.id).addClass("npact");
		}
	}
	gbl_cbk.url1 = build_folder_path(prefix, sc_representation_id, sc_runset_id);
	gbl_cbk.url2 = sc_representation_id + '.png';
	//GLB_ifisrain_callback.prototype.legend = GLB_urls.prototype.base_image_folder + 'cscale_qindexn.png';  // TODO - make it come from meta files
	
	// get JSON object
	json_repr_obj = get_json_representation(sc_representation_id);
	
	// set up legend
	legend_id = null;
	if(is_menu_id_single_repr(the_id)){
		if ((json_repr_obj.legend_sing != undefined) && (json_repr_obj.legend_sing != null) && (json_repr_obj.legend_sing != "")){
			legend_id = json_repr_obj.legend_sing;
		} else if ((json_repr_obj.legend != undefined) && (json_repr_obj.legend != null) && (json_repr_obj.legend != "")) {
			legend_id = json_repr_obj.legend;
		}
	} else if (is_menu_id_comparison_repr(the_id)) {
		if (json_repr_obj == undefined) {
			legend_id = null;
		} else if ((json_repr_obj.legend_comp != undefined) && (json_repr_obj.legend_comp != null) && (json_repr_obj.legend_comp != "")){
			legend_id = json_repr_obj.legend_comp;
		} else if ((json_repr_obj.legend != undefined) && (json_repr_obj.legend != null) && (json_repr_obj.legend != "")) {
			legend_id = json_repr_obj.legend;
		}
	}
	if(legend_id == null){ legend_id = "nolegend"; }
	gbl_cbk.legend = modelplus.viewer.image_legend_folder + legend_id + '.png';
	
	// set up calendar type, design, 
	gbl_cbk.id = the_id;
	if (json_repr_obj.calendar_type == "daily"){
		gbl_cbk.type = 10118;
		gbl_cbk.design = null;
	} else {
		gbl_cbk.type = the_id;
		runset_time_interval = GLB_vars.prototype.get_runset_timediff();
		var eval_ini, eval_end;
		eval_ini = 9 * 24 * 60 * 60;   // 10-days min threshold
		eval_end = 11 * 24 * 60 * 60;  // 10-days max threshold

		// news
		// for hourly
		if (GLB_vars.prototype.is_model_combination(sc_model1_id)){
			gbl_cbk.design = gbl_cbk.design_sc;
			gbl_cbk.array_end = 480;
			gbl_cbk.array_init = 240;
		} else {
			// TODO - use another most appropriate condition - based on representation information
			if ((sc_runset_id == 'realtime') || 
				((runset_time_interval != null)&&(runset_time_interval >= eval_ini)&&(runset_time_interval <= eval_end)) ||
				(((sc_model1_id.indexOf('fore') !== -1) || (sc_model1_id.indexOf('past') !== -1)) && (sc_model1_id.indexOf('pastfore') == -1))){
				gbl_cbk.design = gbl_cbk.design_rt;
				gbl_cbk.array_end = 240;
				gbl_cbk.array_init = 0;
			} else {
				console.log("  FAIL [" + eval_ini + " < " + runset_time_interval + " < " + eval_end + "].");
				gbl_cbk.design = gbl_cbk.design_sc;
				gbl_cbk.array_end = 480;
				gbl_cbk.array_init = 0;
			}
		}
		
	}
	
	// set up other variables
	gbl_cbk.vis = vis;
	gbl_cbk.representation_id = sc_representation_id;
	
	// read reference timestamp and load images after returning from AJAX
	read_reference_timestamp0_map(sc_runset_id, sc_model1_id, sc_model2_id, sc_representation_id, GLB_ifisrain_callback.prototype.call);
}


/**
 *
 * sc_runset_id -
 * sc_model1_id -
 * sc_model2_id - String or null (if not a comparison)
 * sc_result_id -
 * callback_function - function(int timestamp). Function that will be executed after reading the file.
 * RETURN - None.
 */
function read_reference_timestamp0_map(sc_runset_id, sc_model1_id, sc_model2_id, sc_result_id, callback_function){
	"use strict";
	// retrieve the timestamp reference for all models
	// return : Into 'last_timestamps' global variable
	var sc_model_id, ws_url;
	
	// build model combination if needed
	if(sc_model2_id == null)
		sc_model_id = sc_model1_id;
	else
		sc_model_id = sc_model1_id + "_" + sc_model2_id;
	
	modelplus.api.get_timestamp_ref0(sc_runset_id, sc_model_id, sc_result_id)
		.then(function (data){
			callback_function(data[0]); 
	});
}

/**
 * Creates URL for image maps
 * prefix - Expected '90' for single model repr, '92' for comparison model repr (or 'eval'?)
 * parameter_acronym -
 * runset_id -
 * RETURN - String.
 */
function build_folder_path(prefix, parameter_acronym, runset_id){
	var model1_id, model2_id;
	var models_displayed;
	var cur_http;
	
	cur_http = modelplus.url.base_realtime_folder + runset_id + '/repres_displayed/';
	
	model1_id = $("#"+modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
	switch(prefix){
		case "90":
			models_displayed = cur_http + model1_id + "/";
			break;
		case "92":
			model2_id = $("#"+modelplus.ids.MENU_MODEL_COMP_SBOX).val();
			models_displayed = cur_http + model1_id + "_" + model2_id + "/";
			break;
		case "98":
			alert("clicked");
			break;
		default:
			alert("Unexpected value of prefix ('" + prefix + "')");
			return(null);
	}
	
	models_displayed = models_displayed + parameter_acronym + "/";
	
	return (models_displayed);
}

/**
 * Fill main runset select box with the content in 'GLB_vars.prototype.sc_runsets' variable.
 * RETURN - Null. Changes are performed in interface.
 */
function populate_runset_main_sbox(){
	var jquery_runset_sbox, cur_txt;
	var default_runset_id, has_default_runset;
	
	// 
	default_runset_id = 'realtime';
	jquery_runset_sbox = $('#' + modelplus.ids.MENU_RUNSET_SBOX);
	
	// clean previous content
	jquery_runset_sbox.find('option').remove().end();
	
	// populate it
	jquery_runset_sbox.append('<option value="" selected>Select...</option>');
	has_default_runset = false;
	for (var i = 0; i < GLB_vars.prototype.sc_runsets.length; i++){
		
		// ignore hidden runsets
		if(GLB_vars.prototype.sc_runsets[i].show_main == "F"){ continue; }
		
		cur_txt = 	'<option value="'+GLB_vars.prototype.sc_runsets[i].id+'">' + 
						GLB_vars.prototype.sc_runsets[i].title + 
					'</option>';
		jquery_runset_sbox.append(cur_txt);
		if (GLB_vars.prototype.sc_runsets[i].id == default_runset_id){
			has_default_runset = true;
		}
	}
	
	// define function to be run on change
	jquery_runset_sbox.change(modelplus.dom.onchange_runset_main_sbox);
	
	// select 'realtime' as default, if it exists in the list
	if (has_default_runset){
		jquery_runset_sbox.val('realtime');
		jquery_runset_sbox.change();
	}
}


/**
 * Check if a np_link is a group label.
 * RETURN - True if given argument is a group, False otherwise.
 */
function is_np_link_group_label(np_link_type){
	var group_labels_ids, i;
	
	group_labels_ids = [GLB_opt_ids.prototype.mono_group, 
						GLB_opt_ids.prototype.comp_group, 
						GLB_opt_ids.prototype.eval_group, 
						GLB_opt_ids.prototype.comb_group,
						GLB_opt_ids.prototype.tool_group,
						GLB_opt_ids.prototype.hydr_group];
	
	for(i in group_labels_ids){
		if(group_labels_ids[i] == np_link_type){
			return(true);
		}
	}
	
	return(false);
}


// TODO - delte it
GLB_vars.prototype.get_model_name = modelplus.dom.get_model_name;

/*
 *
 * RETURN - 
 */
GLB_vars.prototype.get_representation_call_select = function(representation_id){
	for (var i = 0; i < GLB_vars.prototype.sc_representation.length; i++){
		if (GLB_vars.prototype.sc_representation[i].id == representation_id){
			if (GLB_vars.prototype.sc_representation[i].call_select != undefined){
				return(GLB_vars.prototype.sc_representation[i].call_select);
			} else {
				return(null);
			}
		}
	}
	return(null);
}

/**
 *
 * RETURN - The IDs of all parameters
 */
GLB_vars.prototype.get_comparison_parameters_id = function(model1_id, model2_id){
	var comparison_id, comp_i;
	var comparison_params_id;
	
	comparison_id = model1_id + "_" + model2_id;
	comp_i = -1;
	
	// search for comparison index
	for (var i = 0; i < GLB_vars.prototype.comparison_matrix.length; i++){
		if (GLB_vars.prototype.comparison_matrix[i].id == comparison_id){
			comp_i = i;
			break;
		}
	}
	
	// if not found, break the loop
	if (comp_i == -1){
		alert("Not found comparison " + comparison_id); 
		return(null);
	} else {
		return(GLB_vars.prototype.comparison_matrix[i].params);
	}
}

/**
 *
 * sc_menu_id - A numeric value
 * RETURN - A string if found, null otherwise
 */
function screpresentationid_from_scmenuid(sc_menu_id){
	// TODO - make it flexible for non-select also
	value_element_id = "np"+sc_menu_id+"_sel";
	sc_representation_id = $("#"+value_element_id).val();
	return(sc_representation_id);
}

/**
 *
 * sc_reference_id -
 * RETURN -
 */
function get_json_reference(sc_reference_id){
	for (var i = 0; i < GLB_vars.prototype.sc_references.length; i++){
		if (GLB_vars.prototype.sc_references[i].id == sc_reference_id){
			return(GLB_vars.prototype.sc_references[i]);
		}
	}
	return(null);
}

/**
 *
 * sc_repr_id -
 * RETURN -
 */
function get_json_representation(sc_representation_id){
	for (var i = 0; i < GLB_vars.prototype.sc_representation.length; i++){
		if (GLB_vars.prototype.sc_representation[i].id == sc_representation_id){
			return(GLB_vars.prototype.sc_representation[i]);
		}
	}
	return(null);
}

/**
 *
 * sc_evaluation_id -
 * RETURN -
 */
function get_json_evaluation(sc_evaluation_id){
	for (var i = 0; i < GLB_vars.prototype.sc_evaluation.length; i++){
		if (GLB_vars.prototype.sc_evaluation[i].id == sc_evaluation_id){
			return(GLB_vars.prototype.sc_evaluation[i]);
		}
	}
	return(null);
}

/**
 *
 * repr_id -
 * RETURN -
 */
function is_menu_id_single_repr(repr_id){
	var prefix;
	prefix = repr_id.substring(0, 2);
	if(prefix == "90"){ return (true);} else { return (false); }
}

/**
 *
 * repr_id -
 * RETURN -
 */
function is_menu_id_comparison_repr(repr_id){
	var prefix;
	prefix = repr_id.substring(0, 2);
	if(prefix == "92"){ return (true);} else { return (false); }
}

/**
 *
 * sc_representation_id -
 * attribute_id -
 * RETURN -
 */
function get_optional_representation_attribute(sc_representation_id, attribute_id){
	var repr_obj;
	
	repr_obj = get_json_representation(sc_representation_id);
	if(repr_obj == null){return(null);}
	
	// TODO - solve this
	/* 
	if (repr_obj.representation != undefined){
		repres = GLB_vars.prototype.sc_representation[i].representation;
	} else {
		repres = null;
	}
	*/ 
}

/**
 *
 * display_id :
 * RETURN : None. Changes are performed on interface
 */
function call_custom_display(display_id){
  "use strict";
  var display_address, argument, select_id, splitted_str;
  var stylesheet_link_id = 'custom_display_css';
	
  // check if there is argument and build it
  if(display_id.indexOf('_') > -1){
    splitted_str = display_id.split("_");
    display_id = splitted_str[0];
    argument = splitted_str[1];
  } else {
    select_id = "np" + display_id + "_sel";
    if ($("#" + select_id).val() !== 'undefined'){
      argument = $("#" + select_id).val() + "'";
    } else {
      argument = null;
    }
  }
  
  // check if there is a search div
  var search_div = $("#"+display_id+"_search");
  
  // call stylesheet
  var css_address = modelplus.url.custom_display_css_folder + display_id + ".css";
  $('link[id='+stylesheet_link_id+']').remove();
  var css_tag = '<link rel="stylesheet" type="text/css" id="'+stylesheet_link_id+'" href="'+css_address+'">';
  $('head').append(css_tag);

  // call display
  display_address = modelplus.url.custom_display_js_folder + display_id + ".js";
  if (typeof custom_display !== 'undefined'){
    // delete custom_display;
    custom_display = null;
    if(search_div.length){
      search_div.hide();
	  search_div.find("input:text").each(function() {
        $(this).val('');
      });
    }
  }
  modelplus.scripts.load(display_address, function(){
    if(typeof custom_display !== 'undefined'){
      custom_display(argument);
      if(search_div.length) search_div.show();
    } else {
      alert("'custom_display' undefined for '"+display_id+"'");
    }
  });
}


/**
 *
 * display_id :
 * RETURN :
 */
function hide_custom_display(display_id){
  "use strict";
  var hidden_value, top_legend_obj, idx;
  var gbl_v = GLB_visual.prototype;
	
  modelplus.dom.hide_legend_top(display_id);
	
  // deletes all map polygons attached to the 
  if(typeof(gbl_v.polygons[display_id]) !== 'undefined'){
    if(gbl_v.polygons[display_id] instanceof Array){
      for(idx = 0; idx < gbl_v.polygons[display_id].length; idx++){
        gbl_v.polygons[display_id][idx].setMap(null);
        delete gbl_v.polygons[display_id][idx];
      }
      delete gbl_v.polygons[display_id];
    }
  } else {
    if(display_id.indexOf('_') > -1){
      hide_custom_display(display_id.split("_")[0]);
    } else {
      alert("'" + display_id + "' not in global var");
    }
  }
  
  // hides search
  var search_div = $("#"+display_id+"_search");
  if(search_div.length){
    search_div.hide();
	search_div.find("input:text").each(function() {
      $(this).val('');
    });
  }
}

/**
 * Hide or display rivers vector representation considering time of parameters displayed
 * sc_menu_id - A 'menu id'
 * RETURN - None. Changes are performed on interface
 */
function toggle_river_map(sc_menu_id){
	var sc_representation_id, repres;
	
	// if it is not selected, just show the stuff
	if ($("#np" + sc_menu_id).hasClass("npact") == false){
		iowadata.network.setMap(map);
		GLB_map_river_zoom = true;
		$("#np"+opt_tool_vec_rivers).addClass("npact");
		return;
	}
	
	// gets "representation attribute" relative to selected sc_representation
	sc_representation_id = screpresentationid_from_scmenuid(sc_menu_id);
	repres = null;
	for (var i = 0; i < GLB_vars.prototype.sc_representation.length; i++){
		if (GLB_vars.prototype.sc_representation[i].id == sc_representation_id){
			if (GLB_vars.prototype.sc_representation[i].representation != undefined){
				repres = GLB_vars.prototype.sc_representation[i].representation;
			} else {
				repres = null;
			}
		}
	}
	
	// display or hide the layer
	switch(repres){
		case "composite": 
		case "links_h5_b":
			iowadata.network.setMap(null);
			GLB_map_river_zoom = false;
			$("#np"+opt_tool_vec_rivers).removeClass("npact");
			break;
		case null:
			// if there is nothing to be said, does nothing
			if (iowadata.network.getMap() == null){
				GLB_map_river_zoom = false;
				$("#np"+opt_tool_vec_rivers).removeClass("npact");
			} else {
				GLB_map_river_zoom = true;
				$("#np"+opt_tool_vec_rivers).addClass("npact");
			}
			break;
		default:
			iowadata.network.setMap(map);
			GLB_map_river_zoom = true;
			$("#np"+opt_tool_vec_rivers).addClass("npact");
	}
	
	return;
}
