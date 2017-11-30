
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
    const view_folder = "viewer_3_2";
    var scripts = document.getElementsByTagName('script');
    var index = scripts.length - 1;
    var myScript = scripts[index];
	modelplus.scripts.ubase = myScript.src.split("/"+view_folder+"/")[0]+"/";
	modelplus.scripts.uview = modelplus.scripts.ubase + view_folder + "/";
  })();
  
  // define additional scripts to be loaded
  modelplus.scripts.queue = [modelplus.scripts.ubase + "common/scripts/modelplus.url.js",
                             modelplus.scripts.ubase + "common/scripts/modelplus.api.js",
                             modelplus.scripts.uview + "scripts/modelplus.constants.js", 
                             modelplus.scripts.uview + "scripts/modelplus.main.js",
                             modelplus.scripts.uview + "scripts/modelplus.hydrograph.js"];
  modelplus.scripts.uview_main = modelplus.scripts.uview + "sc_modelplus_3_1.js";
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
	// TODO - all modelplus.viewer.ws_* must vanish
    vw.ws = modelplus.url.proxy + modelplus.url.base_frontend_webservices;
	vw.ws_load_runset = vw.ws + "ws_load_runset.php?runsetid=";
    vw.ws_get_metainfo_load_model = function(runset_id, model_id){
      return(vw.ws + "ws_load_model.php%i%runsetid="+runset_id+"%e%modelid="+model_id);
	}
	vw.ws_representations_ref0_timestamp = vw.ws + "ws_load_timestamp_ref0_map.php";
	vw.ws_get_representations_ref0_timestamp_url = (runset_id, model_id, representation_id)=>{
      var args, url, arg;
      url = vw.ws_representations_ref0_timestamp;
      arg =  "%i%sc_runset_id="+runset_id;
	  arg += "%e%sc_model_id="+model_id;
	  arg += "%e%sc_representation_id="+representation_id;
      return(url + arg);
    }
	// TODO - send the following to the API - OFF
  }
})();

// 3.0 - all menu groups - TODO: send it somewhere else
function GLB_menugroup_ids(){};

// 3.0 - all local URLS
function GLB_urls(){};
GLB_urls.prototype.custom_display_folder = modelplus.url.base_frontend_viewer + 'custom_js/';
modelplus.url.custom_display_css_folder = modelplus.url.base_frontend_viewer + 'custom_css/';

// 3.0 - all web services
function GLB_webservices(){};

GLB_webservices.prototype.metainfo_list_runsets = GLB_webservices.prototype.http + "ws_list_runsets.php";

GLB_webservices.prototype.metainfo_main = GLB_webservices.prototype.http + 'ws_load_metainfo_main.php?runsetid=';
GLB_webservices.prototype.metainfo_scrunset_params = GLB_webservices.prototype.http + 'ws_load_metainfo_runset_raw.php';
GLB_webservices.prototype.metainfo_scmodel_params = GLB_webservices.prototype.http + 'ws_load_metainfo_raw.php';
GLB_webservices.prototype.runsets_desc = modelplus.url.proxy + 'ws_runset_runsetdesc.php?model_id=';
GLB_webservices.prototype.get_models_desc = function(sc_runset_id, sc_model_id){
	return (GLB_webservices.prototype.http + 'ws_model_modeldesc.php%i%model_id=' + sc_model_id + '%e%runset_id=' + sc_runset_id);
}

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

/************************************* IFIS FUNCTIONS ***************************************/
function sc_init() {
	// read_reference_timestamp0();
	// read_reference_timestamp0_map();
	// 'single' starts selected
	
	console.log("sc_init()");
	
	var menu = new Array(
		'<div class="np_title np_blue" style="clear: both; width:100%">IFIS MODEL-PLUS</div>',
		'<div style="width:100%">Runset:' + 
			'<select id="'+modelplus.ids.MENU_RUNSET_SBOX+'" class="sbox" ></select>' +
			'<input id="'+modelplus.ids.MENU_RUNSET_ABOUT+'" type="button" value="About" onclick="load_runset_desc();" class="sbox" />' +
		'</div>',
		'<div style="width:100%">Model:' + 
			'<select id="'+modelplus.ids.MENU_MODEL_MAIN_SBOX+'" class="sbox" style="width:200px" ></select>' +
			'<input id="'+modelplus.ids.MENU_MODEL_ABOUT+'" type="button" value="About" onclick="load_model_desc();" class="sbox" />' +
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
					'<img src="' + modelplus.viewer.image_folder + 'question_mark3.png" class="qicon" onclick="load_parameter_about(\'quni_usgs\', $(this));" />' +
				'</div>',
			'</div>'
		);
	
	//
	$('#np_sc').html(menu.join(''));
	$('#nptsc').attr("src", '../sc/model/model.png');
	$('#nptsc').show();
	$('#logoimg').attr('src', modelplus.viewer.image_folder + 'ifis-logo-mplus.png');
	$('#logoimg').parent().closest('a').attr("href", modelplus.url.base_frontend);

	// load Iowa model domain map
	console.log("Loading: " + modelplus.viewer.map_objects.domain_kml);
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
	
	modelplus.dom.create_modals();
	
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
      load_init_data(populate_runset_main_sbox);
	  var domain_mask = $("#np" + opt_tool_vec_domain);
      if (domain_mask.length != 0){
        domain_mask.click();
      }
    });
  });
}

function sc_np_links(type, vis) {
	
	if (is_np_link_group_label(type)){
		on_menu_1_click('np'+type);
		return;
	}
	
	// close dialogues possible (if open)
	modelplus.main.hide_message_block();
	close_model_hidrograph_desc();
	
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
			var display_address = GLB_urls.prototype.custom_display_folder + "disclausgssih.js";
			if ($("#np" + type).hasClass("npact")){
				delete custom_display;
				loadScript(display_address, function(){
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
				
				// if it is evaluation, clean others
				// if (is_evaluation(type)){
				//	uncheck_other_evaluations(type);
				//}
				
				uncheck_other_evaluations(type);
				
				// if it is representation combined, clean others
				if (is_representation_combined(type)){
					// alert("Show representation combined");
				}
				
				// if it is hydrograph, clean others
				if((is_hydrograph(type))||(is_comparison_modelcomb(type))){
					console.log("Unchecking all '"+type+"'.");
					uncheck_all_other_custom_displays(type);
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
	
	delete_current_parameter_title();
	
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
	
	update_current_parameter_title(GLB_ifisrain_callback.prototype.type);
	
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


/**
 * Function called to display options for mono model or dual model comparison.
 * @param menu_1_id_clicked
 * @return None
 */
function on_menu_1_click(menu_1_id_clicked){
	// identifies clicked radio button and searches for corresponding content box to display it, hiding others.
	
	// 
	for(count = 0; count < GLB_menu_label_id_1.length; count++){
		var cur_element_id = "#" + modelplus.ids.MENU_CONTENTS[count];
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

function on_model_1_select(){
	update_model2_list();
	reclick_item();
}

function on_model_2_select(){
	reclick_item();
}

/**
 *
 * TODO - adapt to the new flexible version of the code
 */
function reclick_item(){
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

function display_submenu(submenu, parent_object){
	// the element 'submenu' is going to be displayed to the left side of 'parent_object'
	
	$(parent_object).mouseover(function() {
		// .position() uses position relative to the offset parent, 
		var pos = $(this).position();

		// .outerWidth() takes into account border and padding.
		var width = $(submenu).outerWidth();

		$(parent_object).css({
			overflowX: 'visible'
		});

		//show the menu directly over the placeholder
		$(submenu).css({
			position: "absolute",
			top: pos.top + "px",
			left: (pos.left - width) + "px"
		}).show();
	});
}

function force_two_digits(the_number){
	if(the_number<10) { the_number='0'+the_number; }
	return(the_number);
}

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

/*
function read_reference_timestamp0(){
	// uses AJAX function to read files containing reference timestamp value for realtime value of zero
	// (last timestamp retrived from database)
	
	// TODO 
	$.ajax({
		url: GLB_timestamp0
	}).success(function(data) {
		last_timestamp = data;
	});
}
*/

/**
 *
 * RETURN - None. Display message in the interface.
 */
function load_runset_desc(){
	var select_value;
	var web_service_add;
	
	select_value = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
	// web_service_add = GLB_runsets_desc_url + select_value;
	
	// alert("..." + " +++ " + GLB_webservices.prototype.runsets_desc);
	
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
function load_model_desc(){
	var sc_model_id, sc_runset_id, web_service_add;
	
	sc_model_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
	sc_runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
	web_service_add = GLB_webservices.prototype.get_models_desc(sc_runset_id, sc_model_id);
	
	$.ajax({
		url: web_service_add
	}).success(function(data) {
		var msg_string, inner_html;
		
		// parse data and build message
		json_obj = JSON.parse(data);
		if(typeof(json_obj.sc_model) !== 'undefined'){
			msg_string = "<strong>Title:</strong> " + json_obj.sc_model.title + "<br />";
			msg_string += "<strong>Description:</strong> " + json_obj.sc_model.description + "<br />";
			/*
			msg_string += "<strong>Parameters:</strong> " + json_obj.parameters + "<br />";
			msg_string += "<strong>Time interval:</strong> " + json_obj.time_interval + "<br />";
			msg_string += "<strong>Data format:</strong> " + json_obj.data_format;
			*/
		} else if (json_obj.error !== 'undefined') {
			msg_string = "<strong>Error:</strong> " + json_obj.error;
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
function display_message_block(msg_html){
	var div_modal = document.getElementById('modal_div');
	var div_modal_ctt = $('#modal_content_div');
	var inner_html;
	
	div_modal.style.display = "block";
	inner_html = "<p><span id='modal_close_span' onclick='modelplus.main.hide_message_block()'>×</span></p>";
	inner_html += "<p>" + msg_html + "</p>";
	div_modal_ctt.html(inner_html);
}

/**
 *
 * msg_html - Message to be displayed in HTML format.
 * RETURN - None. Display message in the interface.
 */
function display_hidrograph_block(msg_html){
	var div_modal = document.getElementById('modal_hidrograph_div');
	var div_modal_ctt = $('#modal_content_hidrograph_div');
	var inner_html;
	
	div_modal.style.display = "block";
	inner_html = "<p><span id='modal_close_span' onclick='close_model_hidrograph_desc()'>×</span></p>";
	inner_html += "<p>" + msg_html + "</p>";
	div_modal_ctt.html(inner_html);
	
	console.log("Add function for button '27'.");
	GLB_keypress.prototype.keys[27] = function(){
		alert("ESC button pressed.");
		close_model_hidrograph_desc();
	};
}

/**
 *
 * RETURN - None. Changes are performed in the interface.
 */
function close_model_hidrograph_desc(){
	$("#modal_hidrograph_div").hide();
	delete GLB_keypress.prototype.keys[27];
}

/**
 *
 * RETURN - None. Changes are performed in the interface.
 */
function load_parameter_about(parameter_acronym, about_obj){
	var html_content;
	switch(parameter_acronym){
		case 'quni_usgs':
			html_content = "<strong>USGS Discharge Map</strong><br />Real time updated water discharge in each USGS flow gage.<br />For more information: <a href='http://waterwatch.usgs.gov/index.php?id=real&sid=w__kml' target='_blank'>access the website.</a> ";
			modelplus.main.display_message_block(html_content);
			// alert("USGS Discharge Map: real time updated water discharge in each USGS flow gage. For more information: http://waterwatch.usgs.gov/index.php?id=real&sid=w__kml");
			break;
		default:
			// check if a select box exists for given menu_id
			var sel_input_id;
			var representation_id;
			var html_content;
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
function delete_current_parameter_title(){
	var div_comps_id = "#" + modelplus.ids.LEGEND_BOTTOM_MODELS_DIV;
	var div_comps_obj;
	
	div_comps_obj = $(div_comps_id);
	
	div_comps_obj.remove();
}

/**
 * 
 * TODO - Make it be called
 * TODO - Make it flexible for the meta files
 */
function update_current_parameter_title(repr_id){
	var map_title = null;
	var sub_type = null;
	var div_comps_id = "#" + modelplus.ids.LEGEND_BOTTOM_MODELS_DIV;
	var div_comps_mdl1_id = "#" + modelplus.ids.LEGEND_BOTTOM_MODEL1_DIV;
	var div_comps_mdl2_id = "#" + modelplus.ids.LEGEND_BOTTOM_MODEL2_DIV;
	var div_comps_obj, div_comps_mdl1_obj, div_comps_mdl2_obj, leg_div_obj;
	var mdl_1_name, mdl_2_name;
	
	// add title
	update_legend_title(GLB_vars.prototype.get_legend_title(repr_id));
	
	// 
	div_comps_obj = $(div_comps_id);
	
	if(!is_menu_id_comparison_repr(repr_id)){
		
		// hide legend comparison model titles if they exist
		if (div_comps_obj.length > 0) {
			console.log("Hidding...");
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
 *
 *
 */
function update_legend_title(legend_title){
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

/* ************************************ ONLY FUNCTION HERE ************************************** */

/**
 * Gets the two-digit format of a number (e.g.: 3 -> "03").
 * a_number: A number.
 * RETURN - String.
 */
function twoDigits(a_number){
	return a_number > 9 ? "" + a_number: "0" + a_number;
}

/**
 *
 */
modelplus.dom.create_modals = function(){
	"use strict";
	
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
 */
modelplus.styles.load = function(filename){
	"use strict";
    
    var fileref = document.createElement("link");
    fileref.setAttribute("rel", "stylesheet");
    fileref.setAttribute("type", "text/css");
    fileref.setAttribute("href", modelplus.url.base_frontend_viewer + filename);
    if (typeof fileref != "undefined")
        document.getElementsByTagName("head")[0].appendChild(fileref);
}

/**
 * Load a script dynamically (copied from internet)
 * url - Imported script url
 * callback - Function o be called on callback
 * RETURN - None
 */
function loadScript(url, callback, callback_arg){

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

// TODO - remove global function
modelplus.scripts.load = loadScript;  // TODO - remove global function

/**
 * Load a list of scripts dynamically
 * urls - List of imported script urls
 * callback - Function to be called on final callback
 * RETURN - None
 */
modelplus.scripts.loadQueue = function(callbackFunction){
  "use strict";
  
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
  console.log("Loading: " + cur_script);
  modelplus.scripts.load(cur_script,
                         modelplus.scripts.loadQueue,
						 callbackFunction);
}