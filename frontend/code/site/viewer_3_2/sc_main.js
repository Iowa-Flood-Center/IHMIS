
/**************************************** WORKSPACE *****************************************/

var modelplus = modelplus || {};

(function () {
  "use strict";
  
  // define URLs
  // TODO: try to move it into modelplus.url.js
  modelplus.url = modelplus.url || {};
  
  // container for Key Codes
  modelplus.keyCodes = modelplus.keyCodes || {};
  
  modelplus.dom = modelplus.dom || {};
  
  modelplus.styles = modelplus.styles || {};
  
  // define other scripts
  modelplus.scripts = modelplus.scripts || {};
  
  // TODO - review the following dirty solution
  (function(){
    var VIEW_FOLDER = "viewer_3_2";
    var scripts = document.getElementsByTagName('script');
    var index = scripts.length - 1;
    var myScript = scripts[index];
	modelplus.scripts.ubase = myScript.src.split("/"+VIEW_FOLDER+"/")[0]+"/";
	modelplus.scripts.uview = modelplus.scripts.ubase + VIEW_FOLDER + "/";
  })();
  
  // define additional scripts to be loaded
  modelplus.scripts.queue = [modelplus.scripts.ubase + "common/scripts/modelplus.url.js",
                             modelplus.scripts.ubase + "common/scripts/modelplus.api.js",
                             modelplus.scripts.uview + "scripts/modelplus.constants.js", 
                             modelplus.scripts.uview + "scripts/modelplus.main.js",
                             modelplus.scripts.uview + "scripts/modelplus.hydrograph.js"];
  modelplus.scripts.uview_main = modelplus.scripts.uview + "modelplus.js";
})();

/*************************************** GLOBAL VARS ****************************************/

// Define global variables (in modelplus.viewer workspace)
// Should be called after external scripts are loaded
(function () {
  "use strict";
  
  modelplus.viewer = modelplus.viewer || {};
  
  modelplus.viewer.define_global_variables = function(){
    var vw = modelplus.viewer;
    vw.image_folder = modelplus.url.base_frontend_viewer + 'imgs/';
	vw.image_legend_folder = vw.image_folder + 'legends/';
	
	vw.map_objects = vw.map_objects || {};
	vw.map_objects.domain_kml = modelplus.url.base_frontend_viewer + 
	                                          "kmls/iowa_water_domain_03_large_truncated.kml";
	
    // TODO - send the following to the API - ON
	GLB_webservices.prototype.http = modelplus.url.api_old_v;
	vw.ws = modelplus.url.proxy + modelplus.url.base_frontend_webservices;
	// TODO - send the following to the API - OFF

    // define folders for custom javascripts and stylesheets
	modelplus.url.custom_display_js_folder = modelplus.url.base_frontend_viewer + 'custom_js/';
    modelplus.url.custom_display_css_folder = modelplus.url.base_frontend_viewer + 'custom_css/';
  }
})();

// 3.0 - all menu groups - TODO: send it somewhere else
function GLB_menugroup_ids(){};

// 3.0 - all menu groups - TODO: vanish with that
function GLB_webservices(){};

// 3.0 - all session variables
function GLB_vars(){};
GLB_vars.prototype.sc_runsets = null;
GLB_vars.prototype.sc_runset = null;
GLB_vars.prototype.sc_models = null;
GLB_vars.prototype.sc_model_combinations = null;
GLB_vars.prototype.sc_references = null;
GLB_vars.prototype.sc_evaluation = null;
GLB_vars.prototype.sc_representation = null;
GLB_vars.prototype.comparison_matrix = null;
GLB_vars.prototype.webmenu = null;
GLB_vars.prototype.get_legend_title = function(menu_id){
	var count_i, cur_obj, the_obj, title_str;
	var select_id, checkbox_id, select_obj, checkbox_obj;
	var div_leg_title_obj;
	
	// defining possible ids and checking what exists
	checkbox_id = "np" + menu_id;
	select_id = checkbox_id + "_sel";
	checkbox_obj = $("#" + checkbox_id);
	select_obj = $("#" + select_id);
	
	title_str = "";
	if ((checkbox_obj.length)&&(select_obj.length)){
		title_str = checkbox_obj.html() + ": " + select_obj.find(":selected").text();
	} else if ((checkbox_obj.length)&&(select_obj.length == 0)) {
		title_str = checkbox_id.html();
	} else {
		console.log("Unexpected situation: " + checkbox_id.length + " and " + select_id.length);
	}
	
	return(title_str);
}
GLB_vars.prototype.is_model_unique = function(sc_model_id){
	return $.inArray(sc_model_id, GLB_vars.prototype.sc_models);
}
GLB_vars.prototype.is_model_combination = function(sc_model_id){
	var idx;
	for(idx = 0; idx < GLB_vars.prototype.sc_model_combinations.length; idx++){
		if (GLB_vars.prototype.sc_model_combinations[idx]["id"] == sc_model_id){
			return(true);
		}
	}
	return(false);
}

// 3.1 - key press actions
function GLB_keypress(){};
GLB_keypress.prototype.keys = {};

// 3.0 - all constants
function GLB_const(){};
GLB_const.prototype.rainBounds = new google.maps.LatLngBounds(new google.maps.LatLng(40.133331,-97.154167), new google.maps.LatLng(44.53785,-89.89942));
GLB_const.prototype.urlviewerbase_tag = "\%URL_VIEWER_BASE\%";
GLB_const.prototype.scrunsetid_tag = "\%SC_RUNSET_ID\%";
GLB_const.prototype.scmodelid_tag = "\%SC_MODEL_ID\%";
GLB_const.prototype.screferenceid_tag = "\%SC_REFERENCE_ID\%";

// 3.0 - all current visualisation variables
function GLB_visual(){};
GLB_visual.prototype.polygons = [];

// 3.0 - beautify dirty
function GLB_ifisrain_callback(){};
GLB_ifisrain_callback.prototype.mock=null;  // an K.O.P. technique for keeping this global variable alive even before using it
GLB_ifisrain_callback.prototype.url1=null;
GLB_ifisrain_callback.prototype.url2=null;
GLB_ifisrain_callback.prototype.call=null;
GLB_ifisrain_callback.prototype.was_sel_change=false;

/****************************** GLOBAL OPTIONS IDS VARIABLES ********************************/

function GLB_opt_ids(){};
GLB_opt_ids.prototype.mono_group = '85999';
GLB_opt_ids.prototype.comp_group = '90999';
GLB_opt_ids.prototype.eval_group = '95999';
GLB_opt_ids.prototype.comb_group = '97999';
GLB_opt_ids.prototype.hydr_group = '98999';
GLB_opt_ids.prototype.tool_group = '99999';

var opt_tool_w_map = '99001';      // white background map
var opt_tool_us_map = '99002';     // USGS discharges kml map
var opt_tool_vec_rivers = '99003';
var opt_tool_vec_domain = '99004';

/********************************* GLOBAL STATIC VARIABLES ***********************************/
var GLB_kml = null;
var GLB_gauges_markers = null;
var GLB_menu_label_id_1 = ['np'+GLB_opt_ids.prototype.mono_group, 
						   'np'+GLB_opt_ids.prototype.comp_group, 
						   'np'+GLB_opt_ids.prototype.tool_group, 
						   'np'+GLB_opt_ids.prototype.eval_group,
						   'np'+GLB_opt_ids.prototype.comb_group,
						   'np'+GLB_opt_ids.prototype.hydr_group];

var GLB_map_type = null;
var GLB_map_river_zoom = null;                                              // REPLACE BY modelplus.main.persist.map_river_zoom
var GLB_map_domain_zoom = false;

/*********************************** GLOBAL MAPS OBJECTS ************************************/

function GLB_map_objects(){};
GLB_map_objects.prototype.kml_object = null;

/******************************** modelplus.X.load FUNCTIONS ********************************/

(function () {
  "use strict";

  modelplus.scripts = modelplus.scripts || {};
  modelplus.styles = modelplus.styles || {};

  /**
   * Load a script dynamically (copied from internet)
   * url - Imported script url
   * callback - Function o be called on callback
   * RETURN - None
   */
  modelplus.scripts.load = function(url, callback, callback_arg){

    var script = document.createElement("script")
    script.type = "text/javascript";

    if (script.readyState){  //IE
      script.onreadystatechange = function(){
        if (script.readyState == "loaded" || 
            script.readyState == "complete"){
          script.onreadystatechange = null;
          callback(callback_arg);
        }
      };
    } else {  //Others
      script.onload = function(){
        callback(callback_arg);
      };
    }

    script.src = url;
    document.getElementsByTagName("head")[0].appendChild(script);
  }

  /**
   * Load a list of scripts dynamically
   * urls - List of imported script urls
   * callback - Function to be called on final callback
   * RETURN - None
   */
  modelplus.scripts.loadQueue = function(callbackFunction){
    var cur_script;
  
    // when finished, trigger sequence
    if(modelplus.scripts.queue.length == 0){
      if(callbackFunction != null){ 
        callbackFunction()
      }
      return;
    }
  
    cur_script = modelplus.scripts.queue[0];
    modelplus.scripts.queue.shift();
    modelplus.scripts.load(cur_script,
                           modelplus.scripts.loadQueue,
                           callbackFunction);
  }
  
  /**
   * Load a .css stylesheet
   */
  modelplus.styles.load = function(filename){
    var fileref = document.createElement("link");
    fileref.setAttribute("rel", "stylesheet");
    fileref.setAttribute("type", "text/css");
    fileref.setAttribute("href", modelplus.url.base_frontend_viewer + filename);
    if (typeof fileref != "undefined")
        document.getElementsByTagName("head")[0].appendChild(fileref);
  }
  
})();

/************************************* IFIS FUNCTIONS ***************************************/
function sc_init() {
	// read_reference_timestamp0();
	// read_reference_timestamp0_map();
	// 'single' starts selected
	
	var menu = new Array(
		'<div class="np_title np_blue" style="clear: both; width:100%">IFIS MODEL-PLUS</div>',
		'<div style="width:100%">Runset:' + 
			'<select id="'+modelplus.ids.MENU_RUNSET_SBOX+'" class="sbox" ></select>' +
			'<input id="'+modelplus.ids.MENU_RUNSET_ABOUT+'" type="button" value="About" onclick="modelplus.dom.load_runset_desc();" class="sbox" />' +
		'</div>',
		'<div style="width:100%">Model:' + 
			'<select id="'+modelplus.ids.MENU_MODEL_MAIN_SBOX+'" class="sbox" style="width:200px" ></select>' +
			'<input id="'+modelplus.ids.MENU_MODEL_ABOUT+'" type="button" value="About" onclick="modelplus.dom.load_model_desc();" class="sbox" />' +
		'</div>',
		'<div id="' + modelplus.ids.MENU_MAIN_ALERT_DIV + '" style="display:none" class="npsub" ></div>',
		'<div class="np_title np_sep" id="'+modelplus.ids.MENU_MODEL_MAIN_RADIO_DIV+'" style="width:150px">' +
				'<a href="#" id="np'+GLB_opt_ids.prototype.mono_group+'" style="color:#EEEEEE">Visualization</a></div>',
			'<div id="'+modelplus.ids.MENU_MODEL_MAIN_SELEC_DIV+'" style="display:none" class="npsub" ></div>',
		'<div class="np_title np_sep" id="'+modelplus.ids.MENU_MODEL_COMP_RADIO_DIV+'" style="width:150px" >' +
				'<a href="#" id="np'+GLB_opt_ids.prototype.comp_group+'" style="color:#EEEEEE">Comparison</a></div>',
			'<div id="' + modelplus.ids.MENU_MODEL_COMPMST_SELEC_DIV + '" style="display:none" class="npsub" >',
				'Model 2:<select id="' + modelplus.ids.MENU_MODEL_COMP_SBOX + '" class="sbox"></select>',
				'<div id="' + modelplus.ids.MENU_MODEL_COMP_SELEC_DIV + '" ></div>',
			'</div>',
		'<div class="np_title np_sep" id="'+modelplus.ids.MENU_MODEL_EVAL_RADIO_DIV+'" style="width:150px" >' + 
				'<a href="#" id="np'+GLB_opt_ids.prototype.eval_group+'" style="color:#EEEEEE">Evaluation</a></div>',
			'<div id="'+modelplus.ids.MENU_MODEL_EVAL_SELEC_DIV+'" style="display:none" class="npsub" >',
			'</div>',
		'<div class="np_title np_sep" id="'+modelplus.ids.MENU_MODEL_COMB_RADIO_DIV+'" style="width:150px" >' + 
				'<a href="#" id="np'+GLB_opt_ids.prototype.comb_group+'" style="color:#EEEEEE">Comparison</a></div>',
			'<div id="'+modelplus.ids.MENU_MODEL_COMB_PARAM_DIV+'" style="display:none" class="npsub" >',
			'</div>',
		'<div class="np_title np_sep" id="'+modelplus.ids.MENU_MODEL_HYDR_RADIO_DIV+'" style="width:150px" >' + 
				'<a href="#" id="np'+GLB_opt_ids.prototype.hydr_group+'" style="color:#EEEEEE">Hydrographs</a></div>',
			'<div id="'+modelplus.ids.MENU_MODEL_HYDR_PARAM_DIV+'" style="display:none" class="npsub" >',
			'</div>',
		'<div class="np_title np_sep" style="width:150px">' + 
				'<a href="#" id="np'+GLB_opt_ids.prototype.tool_group+'" style="color:#EEEEEE">Tools</a></div>',
			'<div id="sc_set_tools" style="display:none" class="npsub" >',
				'<a href="#" id="np'+opt_tool_w_map+'" >White map layer</a>',
				'<a href="#" id="np'+opt_tool_vec_rivers+'" class="npact" >Vector rivers</a>',
				'<a href="#" id="np'+opt_tool_vec_domain+'" >Domain mask</a>',
				'<div id="div'+opt_tool_us_map+'" style="display:inline-block; width:100%">' +
					'<a href="#" id="np'+opt_tool_us_map+'" style="display:inline-block; width:200px" >USGS Discharge Map</a>' +
					'<img src="' + modelplus.viewer.image_folder + 'question_mark3.png" class="qicon" onclick="modelplus.dom.load_parameter_about(\'quni_usgs\', $(this));" />' +
				'</div>',
			'</div>'
		);
	
	//
	$('#np_sc').html(menu.join(''));
	$('#nptsc').attr("src", '../sc/model/model.png');
	$('#nptsc').css("background-color", '#CCBB00');
	$('#nptsc').hover(
		function(){
			$('#nptsc').css("background-color", '#AA9900');}, 
		function(){
			$('#nptsc').css("background-color", '#CCBB00');});
	$('#nptsc').show();
	$('#logoimg').attr('src', modelplus.viewer.image_folder + 'ihmis-logo.png');
	$('#logoimg').parent().closest('a').attr("href", modelplus.url.base_frontend);

	// load Iowa model domain map
	GLB_map_objects.prototype.kml_object = new google.maps.KmlLayer({
        url: modelplus.viewer.map_objects.domain_kml,
        map: null,
		preserveViewport:true,
		suppressInfoWindows: true,
		clickable: false
    });
	
	// set zoom_change function to show/hide features
	map.addListener('zoom_changed', function(){
		// toggle_river_map(GLB_map_type);
		if (GLB_map_river_zoom == null){
			GLB_map_river_zoom = null;  // no changes if nothing was defined
		} else if (GLB_map_river_zoom == false){
			iowadata.network.setMap(null);
		} else if (GLB_map_river_zoom == true) {
			iowadata.network.setMap(map);
		} else {
			console.log("map.addListener.zoom_change: Unexpected value("+GLB_map_river_zoom+")");
		}
		
		// toggle Iowa model domain map
		if (GLB_map_domain_zoom == false){
			// GLB_map_objects.prototype.kml_object.setMap(null);
		} else {
			// GLB_map_objects.prototype.kml_object.setMap(map);
		}
	});
	
	/**
	 * onAdd is called when the map's panes are ready and the overlay has been
     *   added to the map.
	 * It is a re-written of the function to attach it to the 'overlayLayer'
	 *   pane instead of to the imageLayer
     */
	IFISOverlay.prototype.onAdd = function() {
	  var div = document.createElement('div');
	  div.style.border = 'none';
	  div.style.borderWidth = '0px';
	  div.style.position = 'absolute';

	  // Create the img element and attach it to the div.
	  var img = document.createElement('img');
	  img.src = this.image_;
	  img.style.width = '100%';
	  img.style.height = '100%';
	  div.appendChild(img);

	  this.div_ = div;

	  // Add the element to the "overlayImage" pane.
	  var panes = this.getPanes();
	  panes.overlayLayer.appendChild(this.div_);
	};
	
	// set response for key press
	$(document).keyup(function(e) {
		if (e.keyCode in modelplus.keyCodes) { // escape key maps to keycode `27`
			console.log("Trigger function.");
			modelplus.keyCodes[e.keyCode]();
		} else if (e.keyCode == 27) {
			console.log("Esc pressed but nothing to do.");
		}
	});
}


function sc_init_rain() {
	
}

function sc_init_community() {
  "use strict";
  modelplus.scripts.loadQueue(function(){
    modelplus.viewer.define_global_variables();
	modelplus.styles.load("styles.css");
	communityselected(0, 'State of Iowa', 43.0, -92.6,'',0,0);
    modelplus.scripts.load(modelplus.scripts.uview_main, function(){
      modelplus.dom.load_init_data(populate_runset_main_sbox);
	  var domain_mask = $("#np" + opt_tool_vec_domain);
      if (domain_mask.length != 0)
        domain_mask.click();
      modelplus.dom.create_modals();
    });
  });
}

function sc_np_links(type, vis) {
	
	if (is_np_link_group_label(type)){
		modelplus.dom.on_menu_1_click('np'+type);
		return;
	}
	
	// close dialogues possible (if open)
	modelplus.main.hide_message_block();
	modelplus.dom.close_model_hidrograph_desc();
	
	switch (type) {
		// external IFIS tools
		case '10112': case '10113': case '10115': case '10116': case '10117': case '10118': 
			ifis_rain_maps(vis, type); 
			break;
		
		// display/hide white background
		case opt_tool_w_map:
			// keeps in 3.0
			if ($("#np" + type).hasClass("npact")){
				var styles = [
					{
						featureType: "all",
						elementType: "all",
						stylers: [
							{hue: "#ffffff"},
							{saturation: -100},
							{lightness: 100},
							{visibility: "on"}
						]
					}
				]
				var styledMap = new google.maps.StyledMapType(styles,
												{name: "White Map"});
				map.mapTypes.set('map_style', styledMap);
				map.setMapTypeId('map_style');
			} else {
				map.setMapTypeId(google.maps.MapTypeId.TERRAIN);
			}

			break;
		
		// display/hide vector river network
		case opt_tool_vec_rivers:
			if ($("#np" + type).hasClass("npact")){
				GLB_map_river_zoom = true;
				iowadata.network.setMap(map);
			} else {
				GLB_map_river_zoom = false;
				iowadata.network.setMap(null);
				console.log("Cleaned gmarkers");
			}
			break;
		
		// display/hide domain map
		case opt_tool_vec_domain:
			if ($("#np" + type).hasClass("npact")){
				GLB_map_objects.prototype.kml_object.setMap(map);
				iowadata.box.setMap(null);
				GLB_map_domain_zoom = true;
			} else {
				GLB_map_objects.prototype.kml_object.setMap(null);
				iowadata.box.setMap(map);
				GLB_map_domain_zoom = false;
			}
			break;
			
		// display/hide usgs discharge kml
		case opt_tool_us_map:
			// keeps in 3.0 - TODO : modularize this
			var display_address = modelplus.url.custom_display_js_folder + "disclausgssih.js";
			if ($("#np" + type).hasClass("npact")){
				delete custom_display;
				modelplus.scripts.load(display_address, function(){
					if(typeof custom_display !== 'undefined'){
						custom_display();
					} else {
						alert("'custom_display' undefined for 'disclausgssih'");
					}
				});
				
			} else {
				hide_custom_display("disclausgssih");
				$('#'+modelplus.ids.LEGEND_TOP_DIV).remove();
				delete $('#'+modelplus.ids.LEGEND_TOP_DIV);
			}
			break;
		
		default:
			
			var maps_divs = $(map).find('div');
			
			GLB_map_type = type;
			
			if(is_ifis_rain(type)){
				modelplus.main.persist.hold_select = modelplus.main.get_displayed_evaluation();
				load_ifis_rain(type, vis);
				toggle_river_map(type);
			} else {
				
				modelplus.dom.uncheck_other_evaluations(type);
				
				// if it is hydrograph, clean others
				if((is_hydrograph(type))||(is_comparison_modelcomb(type))){
					console.log("Unchecking all '"+type+"'.");
					modelplus.dom.uncheck_all_other_custom_displays(type);
				}
				
				// manage custom display
				if ($("#np" + type).hasClass("npact")){
					call_custom_display(type);
				} else {
					hide_custom_display(type);
				}
			}
			break;
	};
}

function sc_rainobj(type) {
	var design_id;
	var repr_id, repr_obj, map_type;
	
	// overlay: 'ifisoverlay'      // georeferenced, high z-index
	// overlay: 'groundoverlay',   // non-georeferenced, low z-index

    // re-select element
    if(modelplus.main.persist.hold_select != null){
		$("#"+modelplus.main.persist.hold_select).addClass(modelplus.ids.MENU_SELECT_CLASS);
		modelplus.main.persist.hold_select = null;
    }
	
	modelplus.dom.delete_current_parameter_title();
	
	// newer
	rain = new IFIS_Rain({
		type: GLB_ifisrain_callback.prototype.type,
		legend: GLB_ifisrain_callback.prototype.legend,
		name: 'forecastmap',
		overlay: 'ifisoverlay', 
		array_init: GLB_ifisrain_callback.prototype.array_init,
		array_start: 0,
		array_end: GLB_ifisrain_callback.prototype.array_end,
		array_direction: 1,
		array_value: 0,
		array_interval: 60,
		design: GLB_ifisrain_callback.prototype.design,
		url1: GLB_ifisrain_callback.prototype.url1,
		url2: GLB_ifisrain_callback.prototype.url2,
		bound: GLB_const.prototype.rainBounds,
		time: build_current_dateformat(0, new Date(GLB_ifisrain_callback.prototype.ref_timestamp0*1000))
	});
	
	modelplus.dom.update_current_parameter_title(GLB_ifisrain_callback.prototype.type);
	
	setTimeout(function() {   //calls click event after a certain time
		function myself() {
			var clock_obj;
			clock_obj = $('#frtimeline').contents().find('#clock');
			if (clock_obj.length){
				parent.rain_anim('current');
			} else {
				setTimeout(myself, 750);
			}
		}
		myself();
	}, 500);
}


/************************************* OWN FUNCTIONS ***************************************/

function build_current_dateformat(time_shift, current_date_object){
	//
	// time_shift: time shift in hours
	// return: 2015-10-13 14:15:00-05
	
	var today;
	if (typeof current_date_object !== 'undefined') {
		today = current_date_object
	} else {
		today = new Date();  // consider argument if it was given
	}
	today.setHours(today.getHours() + time_shift);
	var dd = force_two_digits(today.getDate());
	var mm = force_two_digits(today.getMonth()+1); //January is 0!
	var yyyy = today.getFullYear();
	var hr = force_two_digits(today.getHours());
	var mn = force_two_digits(today.getMinutes());
	var sc = force_two_digits(today.getSeconds());

	today = yyyy+'-'+mm+'-'+dd+' '+hr+':'+mn+':'+sc+'-05';
	return(today);
}

/* ************************************ ONLY FUNCTION HERE ************************************** */

/**
 * Gets the two-digit format of a number (e.g.: 3 -> "03").
 * a_number: A number.
 * RETURN - String.
 */
function twoDigits(a_number){
  return a_number > 9 ? "" + a_number: "0" + a_number;
}

function force_two_digits(the_number){
	if(the_number<10) { the_number='0'+the_number; }
	return(the_number);
}
