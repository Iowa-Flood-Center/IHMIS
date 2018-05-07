/**************************************************************************************/
/**************************************** DEFS ****************************************/
/**************************************************************************************/

GLB_vars_settings = function(){};
GLB_vars_settings.prototype.delete_url = modelplus.url.proxy + modelplus.url.base_webservice + "ws_delete_runset.php";      // TODO - move to API
GLB_vars_settings.prototype.settings_base_url = modelplus.url.base_frontend_sandbox + "index_3_2/settings/";
GLB_vars_settings.prototype.evaluations_list_url = modelplus.url.proxy + GLB_vars_settings.prototype.settings_base_url + "ws_list_evaluations_possible.php";
GLB_vars_settings.prototype.evaluations_delete_url = modelplus.url.proxy + GLB_vars_settings.prototype.settings_base_url + "ws_delete_evaluation_possible.php";

/**************************************************************************************/
/********************************* modelplus.settings *********************************/
/**************************************************************************************/

var modelplus = modelplus || {};

(function () {
  "use strict";
  
  modelplus.settings = {};
  
  // Triggered when Runset tab is clicked
  modelplus.settings.replace_runsets = function(){
  
    modelplus.api.get_runset_results()
        .then(function(json_obj){
        var cur_i, cur_obj;
        var the_html_cont, the_html_save;
        var div_content = $("#the_content");
		div_content.empty();
      
        // list runsets
        the_html_cont = json_obj.length + " runsets:<br />";
        for(cur_i = 0; cur_i < json_obj.length; cur_i++){
          cur_obj = json_obj[cur_i];
          div_content.append(create_runset_line_div(cur_obj));
          div_content.append(create_runset_edit_div(cur_obj.id));
        }
      
        // option for save current
        $("#the_info").html(create_save_menu());
      })
  }
  
  //
  function create_runset_line_div(runset_obj){
    var div_obj, cur_obj, cur_div;
	var runset_id = runset_obj.id;
	var runset_title = runset_obj.title;
    
    div_obj = $("<div class='runset_line'>");
    
	cur_div = $("<div class='runset_line_title'>");
    cur_obj = $("<span >");
    cur_obj.html(runset_title);
	cur_div.append(cur_obj);
    div_obj.append(cur_div);
    
	cur_div = $("<div class='runset_line_option'>");
    cur_obj = $("<a >");
    cur_obj.attr("onclick", "delete_runset(\""+runset_id+"\");");
    cur_obj.attr("class", "runset_line_option");
	cur_obj.html("delete");
    cur_div.append("(", cur_obj, ")");
    div_obj.append(cur_div);
	
	cur_div = $("<div class='runset_line_option'>");
    cur_obj = $("<a >");
    cur_obj.attr("onclick", "modelplus.settings.edit_runset(\""+runset_id+"\");");
	cur_obj.attr("class", "runset_line_option");
    cur_obj.html("edit");
	cur_div.append("(", cur_obj, ")");
	div_obj.append(cur_div);
    
	cur_div = $("<div class='runset_line_option'>");
    cur_obj = $("<a >");
    cur_obj.attr("onclick", "modelplus.settings.hide_runset(\""+runset_id+"\");");
	cur_obj.attr("class", "runset_line_option");
    cur_obj.html("(hide)");
	cur_div.append(cur_obj);
	if(!modelplus.util.is_runset_visible_public(runset_obj))
      cur_obj.attr("style", "display:none");
    div_obj.append(cur_div);
    
	cur_div = $("<div class='runset_line_option'>");
    cur_obj = $("<a >");
    cur_obj.attr("onclick", "modelplus.settings.show_runset(\""+runset_id+"\");");
	cur_obj.attr("class", "runset_line_option");
    cur_obj.html("(show)");
    cur_div.append(cur_obj);
	if(modelplus.util.is_runset_visible_public(runset_obj))
      cur_obj.attr("style", "display:none");
    div_obj.append(cur_div);
    
    return(div_obj);
  }
  
  //
  function create_runset_edit_div(runset_id){
    var cur_obj;
    cur_obj = $("<div >");
    cur_obj.attr("id", "edit_div_"+runset_id);
    cur_obj.css("display", "none");
    cur_obj.html("");
    return(cur_obj);
  }
  
  // opens runset edit window
  modelplus.settings.edit_runset = function(runset_id){
    var div_obj;
	div_obj = $("#edit_div_"+runset_id);
	
	// toggle if filled
	if(div_obj.html() !== ""){
		div_obj.toggle("slow");
		return;
	}
	
	// fill and show if empty
	modelplus.api.get_runset_result(runset_id)
      .then(function(data_obj){
        var cur_dom, cur_sub_div, cur_label, cur_obj, idx;
		var sc_runset = data_obj[0];
		
		cur_sub_div = $("<div >");
		cur_sub_div.attr("id", "edit_div_models_" + runset_id);
		
		// add models
		div_obj.append("Models:");
		div_obj.append("<br >");
		for(idx=0; idx < sc_runset['sc_model'].length; idx++){
			cur_obj = sc_runset['sc_model'][idx];
			cur_label = $("<label >");
			cur_dom = $("<input type='checkbox' value='"+cur_obj.id+"'>");
			cur_label.append(cur_dom);
			cur_label.append(cur_obj.title);
			cur_sub_div.append(cur_label);
			cur_sub_div.append("<br />");
		}
		
		// add submit button
		cur_dom = $("<input type='button'>");
		cur_dom.attr("value", "Delete selected models");
		cur_dom.attr("onclick", "modelplus.settings.delete_models('"+runset_id+"');");
		cur_sub_div.append(cur_dom);
		
		div_obj.append(cur_sub_div);
		
		div_obj.show("slow");
      });
  }
  
  //
  modelplus.settings.show_runset = function(runset_id){
    var url_show, confirm_r;
    confirm_r = confirm("Really want to show '"+runset_id+"' ?");
    if(confirm_r){
      modelplus.api.change_runset_result_main_visibility(runset_id, true)
		.then(function(data){
          modelplus.settings.replace_runsets();
		});
    }
  }
  
  // 
  modelplus.settings.hide_runset = function(runset_id){
    var url_hide, confirm_r;
    confirm_r = confirm("Really want to hide '"+runset_id+"' ?");
    if(confirm_r){
      modelplus.api.change_runset_result_main_visibility(runset_id, false)
		.then(function(data){
          modelplus.settings.replace_runsets();
		});
    }
  }
  
  // 
  modelplus.settings.delete_models = function(runset_id){
	var models_id;
	var search_div_id = "edit_div_models_" + runset_id;
	
	var checked_objs = $("#"+search_div_id+" input:checked");
	
	// basic check
	if(checked_objs.length <= 0){
		alert("No model selected.");
		return;
	} else if (checked_objs.length == 1) {
		checked_objs = [checked_objs];
	}
	
	var confirm_r = confirm("Really want to delete '"+checked_objs.length+"' models from '"+runset_id+"' ?");
	if(confirm_r){
	  models_id = [];
	  checked_objs.forEach(function (cur_element) {
		var model_id = cur_element.attr('value');
	    models_id.push(model_id);
		modelplus.api.delete_model_from_runset_result(runset_id, models_id)
		/*
	      .then(function(data){
	        alert(JSON.stringify(data));
	      });*/
      });
	  
	}
  }
  
  // Deletes runset from server.
  function delete_runset(runset_id){
      var url_delete, confirm_r;
      
      confirm_r = confirm("Really want to delete '"+runset_id+"' ?");
      
      if(confirm_r){
        url_delete = GLB_vars_settings.prototype.delete_url + "%i%runset_id=" + runset_id;
        $.ajax({
          url: url_delete,
          success: function(data) {
            replace_runsets();
          },
          error: function(data){
            alert("Error: " + data);
          }
        });
      }
  }
  
  /**
   *
   * RETURN :
   */
  modelplus.settings.create_runset_snapshot = function(){
	var url_dict;
  
    // get args from form
    url_dict = {
      id: $("#snap_id").val(),
      name: $("#snap_name").val(),
      about: $("#snap_about").val(),
      timestamp_ini: $("#runset_beg").val(),
      timestamp_end: $("#runset_end").val()
    };

    // basic check
    if ((url_dict.runset_id == "") || (url_dict.runset_name == "")){
      $('#saving_status').html("Both runset id and runset name must be provided.");
      return;
    } else {
      $('#saving_status').html("Saving runset...");
    }
	
	// perform API call
	modelplus.api.save_runset_snapshot(url_dict)
      .then(function(data){
        console.log(JSON.stringify(data));
        $('#saving_status').html("Runset saved!");
      });
  }
  
})();

/**************************************************************************************/
/**************************************** FUNCS ****************************************/
/**************************************************************************************/


/**
 *
 * evaluation_id :
 * RETURN :
 */
function delete_evaluation(evaluation_id){
  var dest_url;
  
  confirm_r = confirm("Really want to remove '"+evaluation_id+"' ?");
  
  if(confirm_r){
    dest_url = GLB_vars_settings.prototype.evaluations_delete_url + "%i%evaluation_id=" + evaluation_id;
    alert("Performing: " + dest_url);
    $.ajax({
      url: dest_url,
      success: function(data) {
        replace_evaluations();
        alert("Success: " + data);
      },
      error: function(data){
        alert("Error: " + data);
      }
    });
  }
}

/**
 *
 * number :
 * RETURN :
 */
function two_digits(number){
    return number > 9 ? "" + number: "0" + number;
}

/**
 *
 * RETURN :
 */
function create_save_menu(){
  var the_html_save, current_timestamp, minimum_timestamp;
  
  // retrieve timestamp in seconds
  current_timestamp = Math.floor(Date.now() / 1000);
  minimum_timestamp = current_timestamp - (10 * 24 * 60 * 60);
  current_date = new Date(current_timestamp * 1000);
  minimum_date = new Date(minimum_timestamp * 1000);
  
  // retrieve hour rounded timestamp
  current_round_date = new Date(current_timestamp * 1000);
  current_round_date.setMinutes(0);
  current_round_date.setSeconds(0);
  current_round_timestamp = current_round_date.getTime()/1000;
  minimum_round_date = new Date(minimum_timestamp * 1000);
  minimum_round_date.setMinutes(0);
  minimum_round_date.setSeconds(0);
  minimum_round_timestamp = minimum_round_date.getTime()/1000;
  
  // retrieve show it to user
  current_str = two_digits(current_date.getDate()) + "/" + two_digits(current_date.getMonth()) + "/" + current_date.getFullYear();
  current_str += ", " + two_digits(current_date.getHours()) + ":" + two_digits(current_date.getMinutes());
  minimum_str = two_digits(minimum_date.getDate()) + "/" + two_digits(minimum_date.getMonth()) + "/" + minimum_date.getFullYear();
  minimum_str += ", " + two_digits(minimum_date.getHours()) + ":" + two_digits(minimum_date.getMinutes());
  
  // show form
  
  the_html_save = "Save current realtime system as runset.<br />";
  
  the_html_save += "<div><div class='save_snapshot_left'>Id:</div>";
  the_html_save += "<div class='save_snapshot_right'><input type='text' id='snap_id' /></div></div>";
  
  the_html_save += "<div><div class='save_snapshot_left'>Title:</div>";
  the_html_save += "<div class='save_snapshot_right'><input type='text' id='snap_name' /></div></div>";
  
  the_html_save += "<div><div class='save_snapshot_left'>Description:</div>";
  the_html_save += "<div class='save_snapshot_right'><textarea style='vertical-align:text-top; height:120px' id='snap_about'></textarea></div></div>";
  
  the_html_save += "<div><div class='save_snapshot_left'>Start:</div>";
  the_html_save += "<div class='save_snapshot_right'>" + minimum_str + "</div>";
  the_html_save += "<input type='hidden' id='runset_beg' value='" +  minimum_round_timestamp + "' ></div>";
  
  the_html_save += "<div><div class='save_snapshot_left'>End:</div>"
  the_html_save += "<div class='save_snapshot_right'>" + current_str + "</div>";
  the_html_save += "<input type='hidden' id='runset_end' value='" + current_round_timestamp + "' ></div>";
  
  the_html_save += "<div class='save_snapshot_center'><input type='button' value='Submit' onclick='modelplus.settings.create_runset_snapshot();' /></div>";
  
  the_html_save += "<div class='save_snapshot_center status' id='saving_status'></div>";
  
  return (the_html_save);
}

/**
 *
 * RETURN :
 */
function replace_evaluations(){
  
  $.ajax({
    url: GLB_vars_settings.prototype.evaluations_list_url,
    success: function(data) {
      var cur_i, json_obj, the_html, cur_eval;
      
      // build html
      the_html = "";
      json_obj = JSON.parse(data);
      json_obj = json_obj.evaluation_matrix_options;
      the_html = json_obj.length + " evaluations:<br />";
      for(cur_i = 0; cur_i < json_obj.length; cur_i++){
        cur_eval = json_obj[cur_i];
        the_html += "- " + cur_eval;
        the_html += "(<a onclick='delete_evaluation(\""+cur_eval+"\");' class='delete_runset'>remove</a>)";
        the_html += "<br />";
      }
      
      // 
      the_html += "&nbsp;<br />";
      the_html += "+ <input type='' /> <input type='text' />";
      the_html += "(<a onclick='alert(\"Functionality under construction.\");' class='delete_runset'>add new</a>)";
      the_html += "<br />";
      
      // print data
      $("#the_content").html(the_html);
      $("#the_info").html("");
    },
    error: function(data) {
      the_html = "Error for " + GLB_vars_settings.prototype.runsets_url;
      
      $("#the_content").html(the_html);
      $("#the_info").html("");
    },
    always: function(data) {
      the_html = "trelale";
      
      $("#the_content").html(the_html);
      $("#the_info").html("");
    }
  });
}