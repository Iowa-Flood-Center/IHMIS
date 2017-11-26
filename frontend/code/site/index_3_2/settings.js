/**************************************************************************************/
/**************************************** DEFS ****************************************/
/**************************************************************************************/

GLB_vars_settings = function(){};
GLB_vars_settings.prototype.runsets_url = modelplus.url.proxy + modelplus.url.base_webservice + "ws_list_runsets.php";      // TODO - move to API
GLB_vars_settings.prototype.delete_url = modelplus.url.proxy + modelplus.url.base_webservice + "ws_delete_runset.php";      // TODO - move to API
GLB_vars_settings.prototype.showhide_url = modelplus.url.proxy + modelplus.url.base_webservice + "ws_showhide_runset.php";  // TODO - move to API
GLB_vars_settings.prototype.settings_base_url = modelplus.url.base_frontend_sandbox + "index_3_1/settings/";
GLB_vars_settings.prototype.evaluations_list_url = modelplus.url.proxy + GLB_vars_settings.prototype.settings_base_url + "ws_list_evaluations_possible.php";
GLB_vars_settings.prototype.evaluations_delete_url = modelplus.url.proxy + GLB_vars_settings.prototype.settings_base_url + "ws_delete_evaluation_possible.php";

/**************************************************************************************/
/**************************************** FUNCS ****************************************/
/**************************************************************************************/

/**
 * Deletes runset from server.
 * runset_id :
 * RETURN :
 */
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
 * runset_id :
 * RETURN :
 */
function hide_runset(runset_id){
	var url_hide, confirm_r;
	
	confirm_r = confirm("Really want to hide '"+runset_id+"' ?");
	
	if(confirm_r){
		url_hide = GLB_vars_settings.prototype.showhide_url + "%i%runset_id=" + runset_id + "%e%show_main=0";
		$.ajax({
			url: url_hide,
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
 * runset_id :
 * RETURN :
 */
function show_runset(runset_id){
	var url_show, confirm_r;
	
	confirm_r = confirm("Really want to show '"+runset_id+"' ?");
	
	if(confirm_r){
		url_show = GLB_vars_settings.prototype.showhide_url + "%i%runset_id=" + runset_id + "%e%show_main=1";
		$.ajax({
			url: url_show,
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
function create_system_snapshot(){
	var runset_id, runset_name, runset_about, runset_beg, runset_end;
	var ws_url, ws_page;
	
	// get args from form
	runset_id = $("#snap_id").val();
	runset_name = $("#snap_name").val();
	runset_about = $("#snap_about").val();
	runset_beg = $("#runset_beg").val();
	runset_end = $("#runset_end").val();
	
	// basic check
	if ((runset_id == "") || (runset_name == "")){
		alert("Both runset id and runset name must be provided.");
		return;
	}
	
	// build url
	ws_page = "ws_create_snapshot.php";
	ws_page += "?runsetid="+runset_id;
	ws_page += "&runsetname="+runset_name;
	ws_page += "&runsetabout="+runset_about;
	ws_page += "&runsetstart="+runset_beg;
	ws_page += "&runsetend="+runset_end;
	ws_url = GLB_vars_settings.prototype.settings_base_url + ws_page;
	
	console.log("Accessing '" + ws_url + "'.");
	
	// work with result
	$.ajax({
		url: ws_url,
		success: function(data) {
			json_obj = JSON.parse(data);
			if (json_obj["Saved"] !== undefined){
				alert("Saved snapshot.");
				$("#snap_id").val = "";
				$("#snap_name").val = "";
			}else if (json_obj["error"] !== undefined) {
				alert("ERROR: " + json_obj["error"]);
			} else {
				alert("Got:" + JSON.stringify(json_obj));
			}
		}
	});
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
	
	the_html_save += "<div style='text-align:center; width:325px'><input type='button' value='Submit' onclick='create_system_snapshot();' /></div>";
	
	return (the_html_save);
}

/**
 *
 * RETURN :
 */
function replace_runsets(){
	
	$.ajax({
		url: GLB_vars_settings.prototype.runsets_url,
		success: function(data) {
			var cur_i, cur_obj;
			var the_html_cont, the_html_save;
			
			// list runsets
			json_obj = JSON.parse(data);
			the_html_cont = json_obj.length + " runsets:<br />";
			for(cur_i = 0; cur_i < json_obj.length; cur_i++){
				cur_obj = json_obj[cur_i];
				the_html_cont += "- " + cur_obj.title;
				the_html_cont += "(<a onclick='delete_runset(\""+cur_obj.id+"\");' class='link_runset'>delete</a>)";
				if ((cur_obj.show_main === undefined) || (cur_obj.show_main == "T")){
					the_html_cont += "(<a onclick='hide_runset(\""+cur_obj.id+"\");' class='link_runset'>hide</a>)";
				} else {
					the_html_cont += "(<a onclick='show_runset(\""+cur_obj.id+"\");' class='link_runset'>show</a>)";
				}
				the_html_cont += "<br />";
			}
			$("#the_content").html(the_html_cont);
			
			// option for save current
			$("#the_info").html(create_save_menu());
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