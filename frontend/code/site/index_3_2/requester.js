/**************************************************************************************/
/**************************************** DEFS ****************************************/
/**************************************************************************************/

var modelplus = modelplus || {};

(function () {
  "use strict";
  
  modelplus.requester = modelplus.requester || {};

  // constants
  modelplus.requester.constants = modelplus.requester.constants || {};
  modelplus.requester.constants.SELECT_HILLSLOPE = "[select a Hillslope profile]";
  modelplus.requester.constants.SELECT_DATE = "[select an appropriate date]";
  modelplus.requester.constants.HOUR_IN_MILISECONDS = 60 * 60 * 1000;
  modelplus.requester.constants.FIELDID_RUNSET_ID = "runset_id";
  
  // debug - DEL ME
  console.log("IS DEPLOY: " + modelplus.url.is_deploy + ", IS SAND: " + modelplus.url.is_sandbox);
  
})();

GLB_vars_requester = function(){};
GLB_vars_requester.prototype.field_calendar_id = "datetime_mid";
GLB_vars_requester.prototype.models_definition_id = "models_def";
GLB_vars_requester.prototype.models_def_prefix_id = "model_def_";
GLB_vars_requester.prototype.run_radio_group_id = "what_run";
GLB_vars_requester.prototype.field_help_id = "field_help";
GLB_vars_requester.prototype.models_count = 1
GLB_vars_requester.prototype.aval_hlms = [];
GLB_vars_requester.prototype.aval_precip = [];
GLB_vars_requester.prototype.aval_reservoirs_link_id = [];

/**************************************************************************************/
/**************************************** FUNCS ***************************************/
/**************************************************************************************/

  modelplus.requester.util = modelplus.requester.util || {};
  
  /**
   * Get the acronyms of all selected items in a div.
   * RETURN: Array of strings
   */
  modelplus.requester.util.get_checked_acronyms = function(parent_div_id){
    "use strict";

    var cur_all_checkbox, cur_all_checked, cur_checkbox_idx, cur_checkbox;
	
	cur_all_checkbox = $("#"+parent_div_id+" :input");
    cur_all_checked = Array();
    for(cur_checkbox_idx in cur_all_checkbox){
      cur_checkbox = cur_all_checkbox[cur_checkbox_idx];
      if(cur_checkbox.checked){
        cur_all_checked.push(cur_checkbox.id.split("_").pop());
      }
    }
	return(cur_all_checked);
  }

  /**
   *
   */
  modelplus.requester.util.get_selected_hlmodel_id = function(modeldef_num){
    "use strict";
    try{
      return(parseInt($("#hillslope_model_"+modeldef_num+" option:selected").val()));
    } catch(err) {
      return(null);
    }
  }
  
  /**
   *
   */
  modelplus.requester.util.get_selected_whatrun = function(){
    "use strict";
    return($("input[name='what_run']:checked").val());
  }

  /**
   *
   * RETURN: Integer - time difference in miliseconds
   */
  modelplus.requester.get_iniend_deltatime = function(what_run){
    "use strict";
	
	var delta_time;
	
	// define delta time in hours, then convert it into miliseconds
	switch(what_run){
      case "20dseq_onlygen": 
	  case "20dseq_loginless": 
      case "10p10f_loginless":
        delta_time = 10 * 24; break;
      case "gencall04days":
        delta_time = 4 * 24; break;
	  case "06hseq_loginless":
	    delta_time = 3; break;
	    break;
	  case "06p06f_loginless":
	    delta_time = 6; break;
	  default:
	    delta_time = 0; break;
    }
    delta_time *= modelplus.requester.constants.HOUR_IN_MILISECONDS;
    return(delta_time);
  }
  
  /**
   *
   * RETURN: Array of dates with size 2
   */
  modelplus.requester.get_iniend_timestamps = function(what_run){
    "use strict";
	
	var delta_time, str_date_value, ini_date, end_date;
	var mid_year, mid_month, mid_day, mid_date;
	
	// calculate delta time
	delta_time = modelplus.requester.get_iniend_deltatime(what_run);
	if(delta_time == 0){
		return(null);}
	
	// process selected date field
	str_date_value = $("#"+GLB_vars_requester.prototype.field_calendar_id).val();
	if (str_date_value.length != 10){
		set_radios_disabled_attr(true);
		// $("#datetime_ini").val("");
		// $("#datetime_end").val("");
		return(null);
	}
	mid_year = str_date_value.substring(6,10);
	mid_month = str_date_value.substring(0,2);
	mid_day = str_date_value.substring(3,5);
	mid_date = new Date(mid_year, mid_month, mid_day, 0,0,0,0);
	
	// prepare date objects and fill them
	ini_date = new Date(mid_year, mid_month, mid_day, 0,0,0,0);
	end_date = new Date(mid_year, mid_month, mid_day, 0,0,0,0);
	ini_date.setTime(mid_date.getTime() - delta_time);
	end_date.setTime(mid_date.getTime() + delta_time);
	
	return([ini_date, end_date]);
  }
  
  /**
   *
   * RETURN :
   */
  modelplus.requester.get_auto_runset_id = function(callback_function){
    "use strict";
    
	var get_url;
	get_url = modelplus.url.proxy + modelplus.url.api;
	get_url += "sc_runsets";
	get_url += "%i%do=get_new_runset_id";
	
    $.get(get_url, 
      function(data){
        var parsed_data, max_num_str, max_num_int, max_num_cnt;
		const PREFIX = "rset";
        parsed_data = JSON.parse(data);
		console.log("a");
		parsed_data = parsed_data["runset_id"];
		console.log("b");
		max_num_str = parsed_data.replace(PREFIX, "");
		max_num_cnt = max_num_str.length;
		console.log("c");
		max_num_int = parseInt(max_num_str) + 1;
		console.log("m");
		max_num_str = max_num_int.toString();
		console.log("n");
		console.log("q");
		console.log("Adding until " + max_num_str.length + " < " + max_num_cnt + ".");
		while(max_num_str.length < max_num_cnt){
			max_num_str = "0" + max_num_str;
		}
		console.log("z");
        callback_function(PREFIX + max_num_str);
	  }
	);

    return(null);
  }
  
  /**
   *
   * RETURN :
   */
  modelplus.requester.fill_auto_runset_id = function(){
    "use strict";
	
    modelplus.requester.get_auto_runset_id(function(data){
      var runset_id_obj;
      runset_id_obj = $("#" + modelplus.requester.constants.FIELDID_RUNSET_ID);
      runset_id_obj.val(data);
    });

    return;
  }
  
  /**
   *
   * TODO - bring content from 'show_help' function into this one
   * RETURN :
   */
  modelplus.requester.show_help = function(field_id){
    "use strict";
    show_help(field_id);
  }
  
  /**
   * Refresh model comparison
   * RETURN :
   */
  modelplus.requester.update_model_comparison_ref = function(max_models){
    "use strict";
    var count_model_1, cur_mdl_id_1, count_model_2, cur_mdl_id_2;
    var div_comparisons;

    div_comparisons = $("#comparisons_def");
	div_comparisons.empty();
	
    // check each model information
    for (count_model_1 = 1; count_model_1 <= max_models-1; count_model_1++){
      cur_mdl_id_1 = $("#model_def_id_"+count_model_1).val();
      for (count_model_2 = 1; count_model_2 <= max_models-1; count_model_2++){
        cur_mdl_id_2 = $("#model_def_id_"+count_model_2).val();
        if ((typeof cur_mdl_id_1 === "undefined") ||
            (typeof cur_mdl_id_2 === "undefined") ||
		    (cur_mdl_id_1 == cur_mdl_id_2)){
          continue;
        }
        // div_comparisons.append(cur_mdl_id_1 + "_" + cur_mdl_id_2);
		div_comparisons.append(modelplus.requester.create_model_comparison_line(count_model_1, count_model_2));
        div_comparisons.append("<br />");
      }
    }
  }

  /**
   *
   * FUNCTION :
   */
  modelplus.requester.update_model_combination_ref = function(max_models){
    "use strict";
    var ws_api_url;
    ws_api_url = modelplus.url.proxy + modelplus.url.api + 'sc_representationscomp';

    // call AJAX
    $.ajax({
      url: ws_api_url,
      success: function(data) {
        var inner_html;
        inner_html = modelplus.requester.create_modelcomb_html(JSON.parse(data), max_models);
        $('#modelcombinations_def').html(inner_html);
      }
    });
  }
  
  /**
   *
   * FUNCTION :
   */
  modelplus.requester.create_modelcomb_html = function(api_response, max_models){
    "use static";
    var return_html, cur_idx1, cur_defval, cur_title, cur_model_id, role_id, role_name;
	var cur_reprcomp;

    // basic check
    if ((!api_response) || (api_response.length == 0)){
      return("Empty");
    }

    return_html = "";
    for(cur_idx1 in api_response){
      cur_reprcomp = api_response[cur_idx1]["acronym"];
      return_html += "<div class='simple_line'>";
      return_html += "<div class='simple_line_left_half'>";
      return_html += api_response[cur_idx1]["title"];
      return_html += ":&nbsp;</div>";
	  return_html += "<div class='simple_line_right_half'>";
      for(cur_idx2 = 1; cur_idx2 < max_models; cur_idx2++){
        cur_model_id = $("#model_def_id_"+cur_idx2).val();
		role_id = api_response[cur_idx1]["roles_mdl"][0]["acronym"];
        if (typeof cur_model_id === "undefined"){
          continue; }
        return_html += "<input type='checkbox' id='modelcomb_"+ cur_reprcomp + "_" +role_id+"_" +cur_model_id+ "' />";
        return_html += cur_model_id + "<br />"
      }
      return_html += "</div>";
	  return_html += "</div>";
    }
    return(return_html);
  }

  /**
   *
   * RETURN :
   */
  modelplus.requester.create_model_comparison_line = function(mdl_num_1, mdl_num_2){
    "use strict";
    var line_content, mdl_id_1, mdl_id_2;
	
	mdl_id_1 = $("#model_def_id_"+mdl_num_1).val();
	mdl_id_2 = $("#model_def_id_"+mdl_num_2).val();

    line_content = "<div class='simple_line'>";
    line_content += "<div class='simple_line_left'>";
    line_content += mdl_id_1 + " x " + mdl_id_2;
    line_content += "</div>";
    line_content += "<div class='simple_line_right'>";
    line_content += modelplus.requester.create_model_comparison_comp(mdl_num_1, mdl_num_2);
    line_content += "</div>";
    line_content += "</div>";

    return(line_content);
  }

  /**
   *
   * RETURN :
   */
  modelplus.requester.create_model_comparison_comp = function(mdl_num_1, mdl_num_2){
    "use strict";
    var all_repr_1, all_repr_2, com_repr, line_content, mdl_1_id, mdl_2_id;

    all_repr_1 = [];
    all_repr_2 = [];
	mdl_1_id = $("#model_def_id_"+mdl_num_1).val();
	mdl_2_id = $("#model_def_id_"+mdl_num_2).val();

    // 
	line_content = "";
    $('#models_def').find("*").each(function(){
      var cur_mdl_num, the_regex;
      var cur_id = $(this).attr('id');
      if (typeof cur_id === "undefined") return;
      if( cur_id.match(new RegExp("^reprs" + mdl_num_1 + "_.+$","g")) ) {
        all_repr_1.push(modelplus.requester.get_repr_id_from_repr_obj_id(cur_id));
      } else if ( cur_id.match(new RegExp("^reprs" + mdl_num_2 + "_.+$","g")) ) {
        all_repr_2.push(modelplus.requester.get_repr_id_from_repr_obj_id(cur_id));
      }
    });

    // 
    com_repr = $(all_repr_1).filter(all_repr_2);
    $(com_repr).each(function(){
      line_content += "<input type='checkbox' id='comp_"+mdl_1_id+"_"+mdl_2_id+"_"+this+"' />";
      line_content += "<span>" + $("#reprs"+mdl_num_1+"_"+this+"_name").html() + "</span>";
      line_content += "<br />";
    });
    return(line_content);
  }
  
  /**
   *
   * RETURN :
   */
  modelplus.requester.get_model_num_from_repr_obj_id = function(repr_obj_id){
    "use strict";
    var clean_val;
    clean_val = repr_obj_id.split("_")[0];
    clean_val = clean_val.replace("reprs", "");
    return(clean_val);
  }
  
  /**
   *
   * RETURN :
   */
  modelplus.requester.get_repr_id_from_repr_obj_id = function(repr_obj_id){
    "use strict";
    var clean_val;
    return(repr_obj_id.split("_")[1]);
  }

/**
 * Function that is triggered when someone selects a date
 */
function on_date_select(){
	"use strict";
	
	var str_date_value, mid_year, mid_month, mid_day;
	var mid_date, ini_date, end_date, delta_time, tmp_dates;
	var what_run, enable_radios;
	
	// gets selected date
	what_run = modelplus.requester.util.get_selected_whatrun();
	tmp_dates = modelplus.requester.get_iniend_timestamps(what_run);
	
	// basic check
    if (tmp_dates == null){
      $("#datetime_ini").val("");
      $("#datetime_end").val("");
      return;
    }
    ini_date = tmp_dates[0];
    end_date = tmp_dates[1];
	
	// fill up the fields
	$("#datetime_ini").val(leadingZero(ini_date.getMonth()) + "/" + leadingZero(ini_date.getDate()) + "/" + ini_date.getFullYear() +" "+
						   leadingZero(ini_date.getHours())+":00");
	$("#datetime_end").val(leadingZero(end_date.getMonth()) + "/" + leadingZero(end_date.getDate()) + "/" + end_date.getFullYear() +" "+
						   leadingZero(end_date.getHours())+":00");
	
	// enable the radio buttons
	set_radios_disabled_attr(false);

	update_available_options();
	update_references_field();
	
	// TODO - send to a function
	var re = new RegExp("^[0-9][0-9]p[0-9][0-9]f_.*$");
	if(re.test(what_run)){
		$("#modelcombinations_def").parent().hide();
		$("#model_def_modelcomb_button").click();
	} else {
		$("#modelcombinations_def").parent().show();
	}
}

/**
 *
 * is_disabled :
 * RETURN :
 */
function set_radios_disabled_attr(is_disabled){
	$("#what_run_20dseq_onlygen").attr("disabled", is_disabled);
	$("#what_run_gencall04").attr("disabled", is_disabled);
	$("#what_run_gencall").attr("disabled", is_disabled);
	$("#what_run_loginless").attr("disabled", is_disabled);
	$("#what_run_06p06f_loginless").attr("disabled", is_disabled);
	$("#what_run_10p10f_loginless").attr("disabled", is_disabled);
}

/**
 * Function trigged on "Include model" button click
 * modeldef_num : 
 * RETURN :
 */
function include_model_definition(modeldef_num){
	var included_div, in_title_model_div, in_hillslope_model_div, in_precip_model_div, in_parameterset_div;
	var display_div, hr;
	var parent_div;
	
	parent_div = $("#" + GLB_vars_requester.prototype.models_definition_id);
	included_div = $("<div id='" + GLB_vars_requester.prototype.models_def_prefix_id + modeldef_num + "' ></div>");
	
	in_id_model_div = $("<div id='model_def_title_"+modeldef_num+"' class='simple_line' >" +
							"<div class='simple_line_left'>Model ID:</div>" +
							"<div class='simple_line_right'>" +
								"<div style='width:100px; display:inline-block'><input type='text' id='model_def_id_"+modeldef_num+"' style='width:90px;'></div>"+
								"<div style='width:180px; display:inline-block; text-align:right'>" +
									"(<span style='display:inline-block' onclick='$(\"#model_def_divdisplay_"+modeldef_num+"\").toggle(); " +
																				"$(\"#model_def_more_img_"+modeldef_num+"\").toggle(); " +
																				"$(\"#model_def_less_img_"+modeldef_num+"\").toggle();' >" +
										"<img src='"+GLB_lib.prototype.img_icon_url+"arrow_more.png' id='model_def_more_img_"+modeldef_num+"' style='display:block; width:10px; height:11px; cursor:pointer;' />" +
										"<img src='"+GLB_lib.prototype.img_icon_url+"arrow_less.png' id='model_def_less_img_"+modeldef_num+"' style='display:none; width:10px; height:11px; cursor:pointer;' />" +
									"</span>)&nbsp;" +
									"(<span style='display:inline-block; cursor:pointer;' onclick='$(\"#model_def_"+modeldef_num+"\").remove()'> X </span>)" +
								"</div>"+
							"</div>"+
						"</div>");
				
	display_div = $("<div id='model_def_divdisplay_"+modeldef_num+"' style='display:None'></div>");

	in_title_model_div = $("<div id='model_def_title_"+modeldef_num+"' class='simple_line'>" +
								"<div class='simple_line_left'>Title:</div>" +
								"<div class='simple_line_right'>" +
									"<input type='text' id='model_title_"+modeldef_num+"' maxlength='26' style='width:90%;'>" +
								"</div>" +
						"</div>");
						
	in_hillslope_model_div = $("<div id='model_def_hsm_"+modeldef_num+"' class='simple_line'>" +
									"<div class='simple_line_left'>Hillslope profile:</div>" +
									"<div class='simple_line_right'>" +
										create_hillslope_models_select_html(modeldef_num) +
										"&nbsp;(<a onclick='show_help(\"hillslope_model\");' class='help_show' >?</a>)&nbsp;" +
									"</div>" +
								"</div>");
	
	in_forcings_model_div = $("<div id='model_def_forcs_"+modeldef_num+"' class='simple_line'>" +
								"<div class='simple_line_left'>Forcings:</div>" + 
								"<div class='simple_line_right'>[select a Hillslope profile]</div>" + 
	                          "</div>");
							  
	in_parameterset_div = $("<div id='model_def_param_"+modeldef_num+"' class='simple_line'>" +
								"<div class='simple_line_left'>" +
									"Global&nbsp;&nbsp;<br />Parameters:" +
								"</div>" +
								"<div class='simple_line_right' id='model_def_param_right_"+modeldef_num+"'>" +
									create_globalparams_html(modeldef_num, null) + 
								"</div>" +
							"</div>");
							
	in_model_reprs_div = $("<div id='model_def_reprs_"+modeldef_num+"' class='simple_line'>"+
							"<div class='simple_line_left'>" +
								"Representations:" +
							"</div>" +
							"<div class='simple_line_right' id='model_def_reprs_right_"+modeldef_num+"'>" +
								"" +
							"</div>" +
						   "</div>");
						   
	in_modelcomb_reprs_div = $("<div id='model_def_reprscomb_"+modeldef_num+"' class='simple_line'>"+
								"<div class='simple_line_left'>" +
									"Sequence&nbsp;&nbsp;<br />Representations:" +
								"</div>" +
								"<div class='simple_line_right' id='model_def_reprscomb_right_"+modeldef_num+"'>" +
									"" +
								"</div>" +
							   "</div>");
							   
	in_evaluation_div = $("<div id='model_def_evals_"+modeldef_num+"' class='simple_line'>" +
							"<div class='simple_line_left'>" +
								"Evaluations:" +
							"</div>" +
							"<div class='simple_line_right' id='model_def_evals_right_"+modeldef_num+"'>" +
								"" +
							"</div>" +
						  "</div>");
						  
	in_desc_model_div = $("<div id='model_def_desc_"+modeldef_num+"' class='simple_line'>" +
								"<div class='simple_line_left'>" +
									"Description:" +
								"</div>" +
								"<div class='simple_line_right'>" +
									"<textarea rows='4' id='model_desc_"+modeldef_num+"' style='width:270px'></textarea>" +
								"</div>" +
						"</div>");
						
	hr = $("<hr id='model_def_hr_"+modeldef_num+"' class='model_division' />");

	in_id_model_div.appendTo(included_div);
	in_title_model_div.appendTo(display_div);
	in_hillslope_model_div.appendTo(display_div);
	in_forcings_model_div.appendTo(display_div);
	in_parameterset_div.appendTo(display_div);
	in_model_reprs_div.appendTo(display_div);
	in_modelcomb_reprs_div.appendTo(display_div);
	in_evaluation_div.appendTo(display_div);
	in_desc_model_div.appendTo(display_div);
	display_div.appendTo(included_div);
	hr.appendTo(included_div);
	
	included_div.appendTo(parent_div);
	
	GLB_vars_requester.prototype.models_count++;
}


/**
 *
 * modeldef_num :
 * RETURN :
 */
function create_hillslope_models_select_html(modeldef_num){
	var aval_hlms, ret_html, cur_j, on_change_str;
	
	aval_hlms = GLB_vars_requester.prototype.aval_hlms;
	on_change_str = "update_global_parameters_field("+modeldef_num+", null);";
	on_change_str += "update_model_representations_field("+modeldef_num+");";
	on_change_str += "update_modelcomb_representations_field("+modeldef_num+", null);";
	on_change_str += "update_forcing_field("+modeldef_num+");";
	on_change_str += "update_evaluation_fields("+modeldef_num+");";
	ret_html = "<select id='hillslope_model_"+modeldef_num+"' onchange='"+on_change_str+"' >";
	ret_html += "<option value=''>Select</option>";
	for(cur_j = 0; cur_j < aval_hlms.length; cur_j++){
		ret_html += "<option value='"+aval_hlms[cur_j]['id']+"'>";
		ret_html += aval_hlms[cur_j]['title'];
		ret_html += "</option>";
	}
	ret_html += "</select>";
	
	return(ret_html);
}

/**
 *
 * modeldef_num :
 * RETURN :
 */
function create_reservoirs_check_form(modeldef_num){
	var aval_reserv_link_ids, disabled_attr;
	
	aval_reserv_link_ids = GLB_vars_requester.prototype.aval_reservoirs_link_id;
	if(aval_reserv_link_ids.length == 0){
		disabled_attr = "disabled";
	} else {
		disabled_attr = "";
	}
	ret_html = "<input type='checkbox' id='reservoir_include_"+modeldef_num+"' "+disabled_attr+" />";
	
	return(ret_html);
}


/**
 *
 * modeldef_num - 
 * api_response - Array returned by API request
 * RETURN: String
 */
function create_globalparams_html(modeldef_num, api_response){
	var return_html, cur_id, cur_defval, cur_title;
	
	// basic check
	if ((!api_response) || (api_response.length == 0)){
		return(modelplus.requester.constants.SELECT_HILLSLOPE);
	}
	
	return_html = "";
	for(cur_idx in api_response){
		// return_html += api_response[cur_idx]['title'] + "<br />"
		cur_id = api_response[cur_idx]['id'];
		cur_defval = api_response[cur_idx]['default_value'];
		cur_title = api_response[cur_idx]['title'];
		return_html += "<span class='param_name_span' id='model_parlbl_"+modeldef_num+"_"+cur_id+"'>"+cur_title+":</span>";
		return_html += "<input type='text' id='model_par_"+modeldef_num+"_"+cur_id+"' class='param_name_input' value='"+cur_defval+"' />";
		return_html += "<br />";
	}
	
	return(return_html);
}


/**
 *
 * modeldef_num - 
 * api_response - Array returned by API request
 * RETURN: None. Changes are performed in the interface.
 */
function create_forcings_html(modeldef_num, api_response){
	"use strict";
	var cur_idx, cur_html, cur_id, cur_title, cur_url;
	var ini_timestamp, end_timestamp, forces_div, cur_div_id;
	var force_idx;
	
	ini_timestamp = new Date($("#datetime_ini").val()).getTime()/1000;
	end_timestamp = new Date($("#datetime_end").val()).getTime()/1000;
	forces_div = $('#model_def_forcs_'+modeldef_num);
	forces_div.empty();
	
	for(cur_idx in api_response){
		// get arguments
		cur_id = api_response[cur_idx]['id'];
		cur_title = api_response[cur_idx]['title'];
		cur_div_id = "model_for_"+modeldef_num+"_"+(1+parseInt(cur_idx));
		
		// build html
		cur_html = "<div class='simple_line'>";
		cur_html += "<div class='simple_line_left'>"+cur_title+":</div>";
		cur_html += "<div class='simple_line_right'>";
		cur_html += "<div id='"+cur_div_id+"'>Loading...</div>";
		cur_html += "</div>";
		cur_html += "</div>";
		forces_div.append($(cur_html));
		
		// call ajax for filling the new div
		cur_url = modelplus.url.proxy + modelplus.url.api + "forcing_sources";
		cur_url += "%i%from_type=" + api_response[cur_idx]['id'];
		cur_url += "%e%timestamp_ini=" + ini_timestamp;
		cur_url += "%e%timestamp_end=" + end_timestamp;
		force_idx = 1 + parseInt(cur_idx);
		$.ajax({
			url:cur_url,
			forc_title:cur_title.toLowerCase(),
			mdldef_num:modeldef_num,
			force_idx:force_idx,
			success: function(json_txt){
				var div_id, json_obj, html_content, sel_id, cur_idx;
				var cur_opt_val;
				json_obj = JSON.parse(json_txt);
				sel_id = "forcing_source_"+this.mdldef_num+"_"+this.force_idx;
				html_content = "<select id='"+sel_id+"'>";
				html_content += "<option value=''>Select...</option>";
				html_content += "<option value='0'>No "+this.forc_title+"</option>";
				for(cur_idx in json_obj){
					html_content += "<option value='"+json_obj[cur_idx]["id"]+"'>";
					html_content += json_obj[cur_idx]["title"];
					html_content += "</option>";
				}
				html_content += "</select>";
				div_id = "model_for_"+this.mdldef_num+"_"+this.force_idx;
				$("#"+div_id).html(html_content);
			}
		});
	}
	return;
}

/**
 *
 * modeldef_num - 
 * api_response - Array returned by API request
 * RETURN: None. Changes are performed in the interface.
 */
function create_evaluations_html(modeldef_num, api_response){
	"use strict";
	var cur_idx, cur_title, html_content, cur_evalcheck_html;
	var div_id, cur_checkbox_id, cur_evalcheck_obj, div_obj;
	
	div_id = "model_def_evals_right_" + modeldef_num;
	div_obj = $("#"+div_id);
	div_obj.empty();
	
	for(cur_idx in api_response){
		cur_checkbox_id = "eval_"+modeldef_num+"_"+api_response[cur_idx]['acronym'];
		cur_title = api_response[cur_idx]['title'];
		cur_evalcheck_html = "<label>";
		cur_evalcheck_html += "<input type='checkbox' id='"+cur_checkbox_id+"' \>";
		cur_evalcheck_html += cur_title + "</label><br />";
		
		div_obj.append(cur_evalcheck_html);
	}
}

/**
 *
 * modeldef_num -
 * hlm_id - 
 * RETURN 
 */
function create_reprs_subfolder_html(modeldef_num){
	"use strict";
	var web_service_url, the_hlm_id, div_obj;
	
	// the_hlm_id = parseInt($("#hillslope_model_"+modeldef_num+" option:selected").val());
	the_hlm_id = modelplus.requester.util.get_selected_hlmodel_id(modeldef_num);
	
	// basic check
	if (isNaN(the_hlm_id)){
		div_obj = $("#model_def_reprs_right_"+modeldef_num);
		div_obj.empty();
		div_obj.append(modelplus.requester.constants.SELECT_HILLSLOPE);
		return;
	}
		
	web_service_url = modelplus.url.proxy + modelplus.url.api;
	web_service_url += 'sc_representations%i%from_hlmodel=' + the_hlm_id;
	
	$.ajax({
		url:web_service_url,
		data:'modeldef_num='+modeldef_num,
		modeldef_num: modeldef_num,
		success: function(json_obj){
			create_representations_list_dom(JSON.parse(json_obj), "model_def_reprs_right_", "reprs", this.modeldef_num);
		}
	});
}

/**
 *
 * modeldef_num -
 * hlm_id - Hillslope-Link Model number. Expect values such as 190, 254, etc.
 * RETURN
 */
function create_reprscomb_subfolder_html(modeldef_num, hlm_id){
	var web_service_url;
	
	if(hlm_id === null){
		the_hlm_id = parseInt($("#hillslope_model_"+modeldef_num+" option:selected").text());
	} else {
		the_hlm_id = hlm_id;
	}
	
	// basic check
	if (isNaN(the_hlm_id)){
		div_obj = $("#model_def_reprscomb_right_"+modeldef_num);
		div_obj.empty();
		div_obj.append(modelplus.requester.constants.SELECT_HILLSLOPE);
		return;
	}
	
	web_service_url = modelplus.url.proxy + modelplus.url.api;
	web_service_url += 'sc_representations%i%from_hlmodel='+the_hlm_id;
	
	$.ajax({
		url:web_service_url,
		data:'modeldef_num='+modeldef_num,
		modeldef_num: modeldef_num,
		success: function(json_obj){
			create_representations_list_dom(json_obj, "model_def_reprscomb_right_", "reprscomb", this.modeldef_num);
		}
	});
}

/**
 *
 * modeldef_num
 * RETURN:
 */
function create_references_subfolder_html(){
	"use strict";
	
	var div_obj, web_service_url;
	
	web_service_url = modelplus.url.proxy + modelplus.url.api;
	web_service_url += 'sc_references%i%timeset=historical';
	
	$.ajax({
		url:web_service_url,
		success: function(json_obj){
			create_references_list_dom(JSON.parse(json_obj));
		}
	});
	
	/*
	div_obj = $("#model_def_refs_right_"+modeldef_num);
	div_obj.empty();
	div_obj.append("[select a Hillslope profile for "+modeldef_num+"]");
	*/
	return;
}

/**
 *
 * api_json_response - 
 * field_prefix - 
 * modeldef_num - 
 * RETURN: Null. Changes are performed in the interface
 */
function create_representations_list_dom(api_json_response, div_id_prefix, checkbox_id_prefix, modeldef_num){
	"use strict";
	
	var json_obj, div_obj, return_html, cur_idx;
	var cur_checkbox_id, cur_reprcheck_html, cur_screpresentation;
			
	div_obj = $("#"+div_id_prefix+modeldef_num);
	div_obj.empty();
	json_obj = api_json_response;
	for(cur_idx in json_obj){
		cur_screpresentation = json_obj[cur_idx];
		cur_checkbox_id = checkbox_id_prefix+modeldef_num+"_"+cur_screpresentation["acronym"];
		cur_reprcheck_html = "<input type='checkbox' id='"+cur_checkbox_id+"' \>";
		cur_reprcheck_html += "<span id='"+cur_checkbox_id+"_name'>" + cur_screpresentation["title"] + "</span>";
		cur_reprcheck_html += "<br \>";
		div_obj.append(cur_reprcheck_html);
	}
}

/**
 *
 *
 *
 * RETURN:
 */
function create_references_list_dom(api_json_response){
	"use strict";
	
	var json_obj, cur_idx, selected_date, div_obj, check_obj;
	var cur_screference, cur_checkbox_id, cur_reprcheck_html;
	
	// get hl_model id and build ws URL
	selected_date = new Date($("#datetime_mid").val());
	
	if (selected_date == null){
		reset_references_field();
		return;
	}
	
	//
	div_obj = $("#model_def_refs_right");
	div_obj.empty();
	json_obj = api_json_response;
	for(cur_idx in json_obj){
		cur_screference = json_obj[cur_idx];
		cur_checkbox_id = "model_def_refs_"+cur_screference["acronym"];
		cur_reprcheck_html = "<label>" +
								"<input type='checkbox' id='"+cur_checkbox_id+"' \>" +
								cur_screference["title"] +
							  "</label><br />";
		check_obj = $(cur_reprcheck_html);
		check_obj.change(function () {
			update_evaluation_fields();
		});
		div_obj.append(check_obj);
	}
}


/**
 *
 * modeldef_num -
 * hlm_id - Hillslope-Link Model number. Expect values such as 190, 254, etc.
 * RETURN: None. Changes are performed in the interface
 */
function update_global_parameters_field(modeldef_num){
	"use strict";
	var ws_api_url, source_dom, the_hlm_id, inner_html;
	
	// get hl_model id and build ws URL
	source_dom = "#hillslope_model_"+modeldef_num+" option:selected";
	the_hlm_id = parseInt($(source_dom).val());
	
	if (isNaN(the_hlm_id)){
		reset_global_parameters_field(modeldef_num)
		return;
	}
	
	// 
	ws_api_url = modelplus.url.proxy + modelplus.url.api;
	ws_api_url += 'hl_models_global_parameters%i%from_hlmodel=';
	ws_api_url += the_hlm_id;
	
	// call AJAX
	$.ajax({
		url: ws_api_url,
		success: function(data) {
			var inner_html;
			inner_html = create_globalparams_html(modeldef_num, JSON.parse(data));
			$('#model_def_param_right_'+modeldef_num).html(inner_html);
		}
	});
}

/**
 *
 * RETURN -
 */
function update_global_parameters_fields(){
	"use strict";
	var cur_model_def_num, cur_model_def_div, cur_div_id;
	for(cur_model_def_num = 1; true; cur_model_def_num++){
		cur_div_id = "#model_def_param_right_" + cur_model_def_num;
		cur_model_def_div = $("#model_def_param_right_" + cur_model_def_num);
		if(!cur_model_def_div.length){ break; }
		update_global_parameters_field(cur_model_def_num);}
}

/**
 *
 * modeldef_num -
 * RETURN - Nothing. Changes are performed in the interface
 */
function reset_global_parameters_field(modeldef_num){
	"use strict";
	var cur_div_id;
	
	cur_div_id = "#model_def_param_right_"+modeldef_num;
	// TODO - this should be somehow a constant
	$(cur_div_id).empty();
	$(cur_div_id).html(modelplus.requester.constants.SELECT_HILLSLOPE);
}

/**
 *
 * modeldef_num -
 * RETURN -
 */
function reset_references_field(){
	"use strict";
	
	var cur_div_id;
	cur_div_id = "#model_def_refs_right_"+modeldef_num;
	$(cur_div_id).empty();
	$(cur_div_id).html(modelplus.requester.constants.SELECT_DATE);
}

/**
 *
 * modeldef_num -
 * RETURN -
 */
function reset_evaluation_fields(modeldef_num){
	"use strict";
	var cur_div_id;
	
	cur_div_id = "#model_def_evals_right_"+modeldef_num;
	$(cur_div_id).empty();
	$(cur_div_id).html(modelplus.requester.constants.SELECT_HILLSLOPE);
}

/**
 * Updates the forcing fields of all model defs
 * RETURN: None. Changes are performed in the interface
 */
function update_forcing_fields(){
	"use strict";
	var cur_model_def_num, cur_model_def_div, cur_div_id;
	for(cur_model_def_num = 1; true; cur_model_def_num++){
		cur_div_id = "#model_def_hsm_" + cur_model_def_num;
		cur_model_def_div = $("#model_def_hsm_" + cur_model_def_num);
		if(!cur_model_def_div.length){ break; }
		update_forcing_field(cur_model_def_num);}
}

/**
 * Updates the forcing fields of a specific model def
 * modeldef_num -
 * RETURN: None. Changes are performed in the interface
 */
function update_forcing_field(modeldef_num){
	"use strict";
	var source_dom, the_hlm_id, ws_api_url;
	
	// get hl_model id
	source_dom = "#hillslope_model_"+modeldef_num+" option:selected";
	the_hlm_id = parseInt($(source_dom).val());
	
	// if no model selected, reset fields
	if(isNaN(the_hlm_id)){
		reset_forcing_fields(modeldef_num);
		return;
	}
	
	// call AJAX
	ws_api_url = modelplus.url.proxy + modelplus.url.api;
	ws_api_url += 'forcing_types%i%from_hlmodel='+the_hlm_id;
	$.ajax({
		url: ws_api_url,
		success: function(data) {
			create_forcings_html(modeldef_num, JSON.parse(data));
		}
	});
}

/**
 *
 * modeldef_num -
 * RETURN - Nothing. Changes are performed in the interface
 */
function reset_forcing_fields(modeldef_num){
	"use strict";
	var cur_div_id, cur_div_html;
	
	cur_div_id = "#model_def_forcs_"+modeldef_num;
	// TODO - this should be somehow a constant
	cur_div_html = "<div class='simple_line_left'>Forcings:</div>" + 
				   "<div class='simple_line_right'>[select a Hillslope profile]</div>";
	$(cur_div_id).empty();
	$(cur_div_id).html(cur_div_html);
}

/** 
 *
 */
function update_evaluation_fields(){
	"use strict";
	
	var cur_model_def_num, cur_model_def_div, cur_div_id;
	for(cur_model_def_num = 1; true; cur_model_def_num++){
		cur_div_id = "#model_def_hsm_" + cur_model_def_num;
		cur_model_def_div = $("#model_def_hsm_" + cur_model_def_num);
		if(!cur_model_def_div.length){
			break; }
		update_evaluation_field(cur_model_def_num);}
}

/**
 *
 * modeldef_num -
 */
function update_evaluation_field(modeldef_num){
	"use strict";
	
	var source_dom, the_hlm_id, ws_api_url, the_refs;
	
	// get hl_model id and references id
	the_hlm_id = modelplus.requester.util.get_selected_hlmodel_id(modeldef_num);
	the_refs = modelplus.requester.util.get_checked_acronyms("model_def_refs_right");
	
	// if no model or refs selected, reset fields
	if((isNaN(the_hlm_id)) || (the_refs.length == 0)){
		reset_evaluation_fields(modeldef_num);
		return;
	}
	
	// call AJAX
	ws_api_url = modelplus.url.proxy + modelplus.url.api +
	              'sc_evaluations%i%for_hlmodel=' + the_hlm_id +
				  '%e%from_references=' + the_refs.join(",");
	$.ajax({
		url: ws_api_url,
		success: function(data) {
			create_evaluations_html(modeldef_num, JSON.parse(data));
		}
	});
}

/**
 *
 * modeldef_num -
 * hlm_id -
 * RETURN
 */
function update_model_representations_field(modeldef_num){
	create_reprs_subfolder_html(modeldef_num);
}

/**
 *
 * modeldef_num -
 * RETURN
 */
function update_modelcomb_representations_field(modeldef_num, hlm_id){
	create_reprscomb_subfolder_html(modeldef_num, hlm_id);
}

/**
 *
 */
function update_references_field(){
	create_references_subfolder_html();
}

/**
 *
 * number: 
 * RETURN - String of length 2
 */
function leadingZero(number){
	return (number < 10) ? ("0" + number) : number;
}


/**
 * Update available precipitations, hillslope models and reservoirs data
 * RETURN : None. Changes are performed in the interface.
 */
function update_available_options(){
	var ini_timestamp, end_timestamp, ws_api_url;
	
	// build url
	ini_timestamp = new Date($("#datetime_ini").val()).getTime()/1000;
	end_timestamp = new Date($("#datetime_end").val()).getTime()/1000;
	
	// call AJAX for hillslope-link available profiles
	ws_api_url = modelplus.url.proxy + modelplus.url.api;
	ws_api_url += 'hl_models%i%timestamp_ini=' + ini_timestamp;
	ws_api_url += '%e%timestamp_end=' + end_timestamp;
	$.ajax({
		url: ws_api_url,
		success: function(data) {
			update_available_hillslope_models(JSON.parse(data));
			update_forcing_fields();
			update_global_parameters_fields();
		}, 
		error: function(xhr, status, error){
			console.log('AJAX error. Got "' + xhr.responseText.trim() + '"');
		}
	});
}


/**
 *
 * aval_hlms :
 * RETURN : None. Change is performed in GLB_vars_requester.prototype.aval_hlms var and interface
 */
function update_available_hillslope_models(aval_hlms){
	var cur_i, cur_j, cur_select_id, cur_select_obj, cur_prev_val, cur_s;
	
	// update global file
	GLB_vars_requester.prototype.aval_hlms = aval_hlms;
	
	// update rainproduct select box
	for(cur_i = 1; cur_i <= GLB_vars_requester.prototype.models_count; cur_i++){
		cur_select_id = "#hillslope_model_" + cur_i;
		if(typeof $(cur_select_id).val() === "undefined"){
			continue;
		}
		cur_select_obj = $(cur_select_id);
		cur_prev_val = cur_select_obj.val();
		cur_select_obj.find('option').remove();
		cur_select_obj.append($("<option value=''>Select</option>"));
		for(cur_j = 0; cur_j < aval_hlms.length; cur_j++){
			if (cur_prev_val == aval_hlms[cur_j]['id']) {cur_s = "selected";} else {cur_s = "";}
			cur_select_obj.append($("<option "+cur_s+"></option>")
								.attr("value", aval_hlms[cur_j]['id'])
								.text(aval_hlms[cur_j]['title']));
		}
	}
}


/**
 *
 * aval_link_ids : list of link ids with available reservoir data
 * RETURN : None. Change is performed in GLB_vars_requester.prototype.aval_reservoirs_link_id var and interface
 */
function update_available_reservoir_links(aval_link_ids){
	var can_select, cur_checkbox_id;
	
	// 
	GLB_vars_requester.prototype.aval_reservoirs_link_id = aval_link_ids;
	
	// define if reservoirs data is available
	if (aval_link_ids.length > 0){
		can_select = true;
	} else {
		can_select = false;
	}
	
	// update reservoirs check box
	for(cur_i = 1; cur_i <= GLB_vars_requester.prototype.models_count; cur_i++){
		cur_checkbox_id = "#reservoir_include_" + cur_i;
		if(typeof $(cur_checkbox_id).val() === "undefined"){
			console.log("Not found '"+cur_checkbox_id+"'.");
			continue;
		}
		cur_checkbox_obj = $(cur_checkbox_id);
		if(!can_select){
			cur_checkbox_obj.prop('checked', false);
			cur_checkbox_obj.attr("disabled", true);
		} else {
			cur_checkbox_obj.removeAttr("disabled");
		}
	}
}


/**
 *
 * field_id :
 * RETURN :
 */
function show_help(field_id){
	var html_content, html_close;
	
	switch(field_id){
		case "runset_id":
			html_content = "<strong>Runset ID</strong><br />";
			html_content += "Short string (up to 10 characters).<br />";
			html_content += "<strong>Rules:</strong><br />";
			html_content += "- No space. No special characters.<br/>";
			html_content += "- Start with characters, not numbers.<br />";
			html_content += "- Must be unique.<br />";
			html_content += "- Not a reserved word <br />";
			html_content += "   ('runset', 'realtime', 'log')";
			break;
		case "runset_title":
			html_content = "<strong>Runset Title</strong><br />";
			html_content += "Used to present runset to user.<br />";
			html_content += "String with up to 25 characters.<br />";
			html_content += "Does not accept special character.<br />";
			html_content += "Underscores ('_') are replaced by spaces (' ').<br />";
			html_content += "Must be unique.";
			break;
		case "datetime_mid":
			html_content = "<strong>Date</strong><br />";
			html_content += "Date in which an event of interest happened.<br />";
			html_content += "Simulation will execute within some days prior and after such date.<br />";
			html_content += "Determines which rainfall data sources and hillslope models are available.";
			break;
		case "hillslope_model":
			html_content = "<strong>Hillslope profile</strong><br />";
			html_content += "Determines how the hillslope profile is going to be modeled in Asynch.<br />";
			break;
		case "precipitation_source":
			// TODO - remove it
			html_content = "<strong>Precipitation source</strong><br />";
			html_content += "Precipitation product.<br />";
			break;
		case "reservoir_consider":
			html_content = "<strong>Reservoir</strong><br />";
			html_content += "If historical data in of reservoirs release will be considered in the simulation.<br />";
			break;
		case "server":
			html_content = "<strong>Server</strong><br />";
			html_content += "HPC server on U. of Iowa.<br />";
			html_content += "Provided user must have access to it and Suo Push enabled.";
			break;
		case "hawk_id":
			html_content = "<strong>Hawk ID</strong><br />";
			html_content += "Your user hawk ID.";
			break;
		case "email":
			html_content = "<strong>E-mail</strong><br />";
			html_content += "An e-mail address to which messages related to the processes execution on HPC will be sent.<br />";
			html_content += "If left empty, no e-mails are sent.";
			break;
		case "hawk_pass":
			html_content = "<strong>Password</strong><br />";
			html_content += "Your user hawk ID password.<br />";
			html_content += "<strong>This information is not stored anywhere.</strong>";
			break;
		default:
			html_content = ".";
			break;
	}
	
	// add close button
	html_close = "<div class='help_hide'>";
	html_close +=  "[<a onclick='$(\"#"+GLB_vars_requester.prototype.field_help_id+"\").hide();'>x</a>]";
	html_close +="</div>";
	
	// 
	$("#" + GLB_vars_requester.prototype.field_help_id).html(html_close + html_content);
	$("#" + GLB_vars_requester.prototype.field_help_id).show();
}


/**
 * Function called when "submit" button is clicked
 * max_models - maximum number of models sent
 * RETURN - Null. Changes are performed in interface.
 */
function on_submit_click(max_models){
	if (!check_fields(max_models, submit_request)){
		alert("Unable to create files.");
	}
}


/**
 * Evaluate if all ids (Runset and Model_ids) are consistent
 * max_models -
 * RETURN - Boolean. True if the fields are ok, False otherwise.
 */
function check_fields(max_models, callback_function){
	var given_ids, can_create, check_url, check_url_addr, check_url_args;
	var runset_id, runset_title, what_run, hawk_id, password;
	
	// retrieve basic data from forms
	runset_id = $("#runset_id").val();
	runset_title = $("#runset_title").val().replace(" ", "_");;
	what_run = $("input[name='what_run']:checked").val();
	
	// prepare array for non-repetitive check and cumulative flag
	given_ids = new Array();
	can_create = true;
	
	// check if runset is not null and valid
	if(runset_id == ""){
		can_create = false;
		alert("Runset ID is empty.");
	} else if (/^\w+$/.test(runset_id) == false){
		can_create = false;
		alert("Runset ID has non-letters or non-numbers characters.");
	} else if (/^[0-9].+$/.test(runset_id) == true) {
		can_create = false;
		alert("Runset ID starts with a number character.");
	} else {
		given_ids.push($("#runset_id").val());
	}
	
	// basic check to for date selection
	if($("#"+GLB_vars_requester.prototype.field_calendar_id).val().trim() == ""){
		can_create = false;
		alert("A date must be selected.");
	}
	
	// check if there is any model
	if(max_models == 1){
		can_create = false;
		alert("At least one model must be specified.");
	}
	
	// check each model information
	for (count_model = 1; count_model <= max_models-1; count_model++){
		// check if model was deleted
		if(typeof $("#model_def_id_"+count_model).val() === "undefined"){
			continue;
		}
		
		// check consistency
		if (!check_model_input(count_model, given_ids)){ 
			can_create = false;
			alert("Model '" + $("#model_def_id_"+count_model).val() + "' is invalid.");
			continue;
		}
	}
	
	// submit runset informations for check non-repetitive
	check_url_addr = modelplus.url.proxy + modelplus.url.base_webservice;
	check_url_addr += "ws_evaluate_runset_id.php";
	check_url_args = "%i%runsetid="+runset_id+"%e%runset_title="+runset_title;
	check_url = check_url_addr + check_url_args;
	if (can_create){
		$.get(check_url, 
		  function(data){
			if (data.trim() == "T"){
				console.log("Calling callback.");
				callback_function(max_models);
			} else {
				alert("Cannot create ("+data.trim()+")");
				can_create = false;
			}
		}
	)};
	return(can_create);
}


/**
 *
 * model_count :
 * given_ids :
 * RETURN :
 */
function check_model_input(model_count, given_ids){
	var model_id, hillslope_model, precipitation_source;
	var the_return;
	
	the_return = true;
	model_id = $("#model_def_id_"+model_count).val();
	
	// check if model was deleted
	if(typeof model_id === "undefined"){
		return(true);
	}
	
	// check if model has invalid characters
	if (/^\w+$/.test(model_id) == false){
		alert("Model ID '"+model_id+"' has non-letters or non-numbers characters.");
		the_return = false;
	}
	
	// check if model name starts with a number
	if(/^[0-9].+$/.test(model_id) == true){
		alert("Model ID '"+model_id+"' start with a number. It must start with a letter.");
		the_return = false;
	}
	
	// check if model id is unique
	if(given_ids.indexOf(model_id) != -1){
		alert("Model ID '"+model_id+"' is not unique.");
		the_return = false;
	}
	
	given_ids.push(model_id);
	
	// check if hillslope model was selected
	hillslope_model = $("#hillslope_model_"+model_count).val();
	if(hillslope_model == ""){
		alert("Model ID '"+model_id+"' has no hillslope model.");
		the_return = false;
	}
	
	// check if a precipitation was selected
	/*
	precipitation_source = $("#precipitation_source_"+model_count).val();
	if(precipitation_source == ""){
		alert("Model ID '"+model_id+"' has no precipitation source.");
		the_return = false;
	}
	*/
	
	return(the_return);
}


/**
 *
 * max_models - 
 * RETURN
 */
function submit_request(max_models){
	"use strict";
	var cur_all_reprs_checkbox, cur_all_reprs_checked, cur_repr_checkbox, cur_repr_checkbox_idx;
	var given_ids, alert_msg, cur_desc_par, cur_par_value, cur_par_label;
	var dest_url, post_dict, desc_vec, count_model, count_added_models;
	var runset_id, runset_title, what_run, email, asynch_ver;
	var cur_all_reprcomb_checked, cur_reprcomb_checkbox;
	var cur_splitted, count_forcing, cur_forcing_name;
	var cur_par_label_id, cur_all_reprscomb_checkbox;
	var cur_count_parameters, cur_par_field_id;
	var cur_reprcomb_checkbox_idx;
	
	console.log("Executing submit_request(" + max_models + ").");
	
	// get common fields
	runset_id = $("#runset_id").val();
	runset_title = $("#runset_title").val().replace(" ", "_");
	email = $("#email").val();
	what_run = $("input[name='what_run']:checked").val();
	asynch_ver = $("#asynch_ver").val();
	
	// build POST arguments
	post_dict = {};
	desc_vec = [];
	
	// add general data
	post_dict["sandbox"] = modelplus.url.is_sandbox;
	post_dict["runset_id"] = runset_id;
	post_dict["runset_title"] = runset_title.replace(" ", "_");
	post_dict["timestamp_ini"] = new Date($("#datetime_ini").val()).getTime()/1000;
	post_dict["timestamp_end"] = new Date($("#datetime_end").val()).getTime()/1000;
	post_dict["server_addr"] = $("#server_addr").val();
	post_dict["email"] = email;
	post_dict["num_models"] = max_models-1;
	post_dict["what_run"] = what_run;
	post_dict["asynch_ver"] = asynch_ver;
	
	switch(what_run){
		case "06p06f_loginless":
		case "10p10f_loginless":
			alert("Is case lless");
			post_dict["server_addr"] = "argon.hpc.uiowa.edu";
			// post_dict["asynch_ver"] = "1.2";
			break;
		default:
			alert("Not case lless");
			post_dict["server_addr"] = $("#server_addr").val();	
			// post_dict["asynch_ver"] = asynch_ver;
			break;
	}
	
	// check and add each model information
	count_added_models = 0;
	for (count_model = 1; count_model <= post_dict["num_models"]; count_model++){
		// check if model was deleted
		if(typeof $("#model_def_id_"+count_model).val() === "undefined"){
			continue;
		}
		
		// add data
		post_dict["model_id_"+count_model] = $("#model_def_id_"+count_model).val();
		post_dict["hillslope_model_"+count_model] = $("#hillslope_model_"+count_model).val();
		// post_dict["precipitation_source_"+count_model] = $("#precipitation_source_"+count_model).val();
		// post_dict["reservoir_include_"+count_model] = $("#reservoir_include_"+count_model).is(':checked');
		// console.log("'reservoir_include_"+count_model+"': " + $("#reservoir_include_"+count_model).is(':checked') + ". ");
		post_dict["model_title_"+count_model] = $("#model_title_"+count_model).val();
		post_dict["model_desc_"+count_model] = $("#model_desc_"+count_model).val();
		cur_desc_par = "";
		
		// add forcings
		for(count_forcing = 1; true; count_forcing++){
			cur_forcing_name = "#forcing_source_"+count_model+"_"+count_forcing;
			if(!$(cur_forcing_name).length) {break;}
			post_dict["model_for_"+count_model+"_"+count_forcing] = $(cur_forcing_name).val();
		}
		
		// add parameters
		cur_count_parameters = 1;
		cur_par_field_id = "model_par_"+count_model+"_"+cur_count_parameters;
		cur_par_label_id = "model_parlbl_"+count_model+"_"+cur_count_parameters;
		while ($("#"+cur_par_field_id).length){
			cur_par_value = $("#"+cur_par_field_id).val();
			cur_par_label = $("#"+cur_par_label_id).html();
			
			post_dict[cur_par_field_id] = cur_par_value;
			
			desc_vec.push(cur_par_label.trim() + cur_par_value);
			
			// prepare for next
			cur_count_parameters = cur_count_parameters + 1;
			cur_par_field_id = "model_par_"+count_model+"_"+cur_count_parameters;
			cur_par_label_id = "model_parlbl_"+count_model+"_"+cur_count_parameters;
		}
		
		// add model representations
		cur_all_reprs_checked = modelplus.requester.util.get_checked_acronyms("model_def_reprs_right_"+count_model);
		post_dict["model_repr_"+count_model] = cur_all_reprs_checked.join(",");
		
		// add model comb. representations
		cur_all_reprscomb_checkbox = $("#model_def_reprscomb_right_"+count_model+" :input");
		cur_all_reprcomb_checked = Array();
		for(cur_reprcomb_checkbox_idx in cur_all_reprscomb_checkbox){
			cur_reprcomb_checkbox = cur_all_reprscomb_checkbox[cur_reprcomb_checkbox_idx];
			if(cur_reprcomb_checkbox.checked){
				cur_all_reprcomb_checked.push(cur_reprcomb_checkbox.id.split("_")[2]);
			}
		}
		// console.log("Joinned: "+cur_all_reprcomb_checked.join(","));
		post_dict["modelseq_repr_"+count_model] = cur_all_reprcomb_checked.join(",");
		
		post_dict["model_desc_"+count_model] += "<br />Model " + $("#hillslope_model_"+count_model).val() + " ";
		post_dict["model_desc_"+count_model] += "(" + desc_vec.join(", ") + ").";
		
		// iterates
		count_added_models = count_added_models + 1;
	}
	
	// TODO - add comparisons
	$('#comparisons_def').find("*").each(function(){
		if( cur_id.match(new RegExp("^reprs" + mdl_num_1 + "_.+$","g")) ) {
			
		}
	});
	
	//
	$('#modelcombinations_def').find("*").each(function(){
		"use strict";
		var cur_splitted, cur_id;
		cur_id = $(this).attr("id");
		if( typeof cur_id === "undefined"){ return; }
		if( cur_id.match(new RegExp("^modelcomb_.+_.+_.+$","g")) ) {
			cur_splitted = cur_id.split("_");
			console.log("Getting from " + cur_id + ".");
			if($(this).is(":checked")){
				if (typeof post_dict["modelcomb_"+cur_splitted[1]] === "undefined"){
					post_dict["modelcomb_"+cur_splitted[1]] = [];
				}
				post_dict["modelcomb_"+cur_splitted[1]].push(cur_splitted[2] + "_" + cur_splitted[3]);
			}
		}
	});
	
	console.log(JSON.stringify(post_dict));
	
	// define server-side URL
	dest_url = modelplus.url.proxy + modelplus.url.api;
	dest_url += "sc_runset_requests/new";
	
	// execute stuff if possible
	if(count_added_models > 0){
		// call web service
		$.post(dest_url, post_dict,
			function(data){
				var data_obj;
				try{
					data_obj = JSON.parse(data);
					if(data_obj['Exception'] !== undefined){
						alert("SUBMISSION FAILED: " + data_obj['Exception']);
					} else if (data_obj['dispatched'] !== undefined) {
						if (data_obj['dispatched']){
							alert("Input files sent to the HPC.");
						} else {
							alert("Input files generated, but NOT sent to the HPC.");
						}
					} else {
						alert(data);
					}
				} catch(err) {
					alert(data);
				}
			}
		);
	} else {
		alert("Cannot create tar file. It is necessary at least one model definition.");
	}
}


/**************************************************************************************/
/**************************************** LOAD ****************************************/
/**************************************************************************************/

$(function(){
	// set up callendar
	$("#" + GLB_vars_requester.prototype.field_calendar_id).datepicker();
});
