modelplus.custom_display = modelplus.custom_display || {};

function custom_display(){
	"use strict"
	var modelcomb_id, runset_id, represcomb_id;
	var all_links_dict, gages_location_dict;
	var root_url, ws_data_url;
	
	// holder variable
	modelplus.custom_display.selected_models = null;
	
	/**
	 *
	 * color_value :
	 * RETURN :
	 */
	function color_num_to_hex(color_value){
		if((color_value >= 0)&&(color_value <= 9)){
			return(color_value.toString());
		} else if (color_value == 10) {
			return('a');
		} else if (color_value == 11) {
			return('b');
		} else if (color_value == 12) {
			return('c');
		} else if (color_value == 13) {
			return('d');
		} else if (color_value == 14) {
			return('e');
		} else if (color_value == 15) {
			return('f');
		} else {
			return('0');
		}
	}
	
	/**
	 *
	 */
	modelplus.custom_display.config_on_click = function(){
		$('#'+ modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF).slideToggle("slow");
		
	}
	
	/**
	 *
	 */
	modelplus.custom_display.config_update = function(){
		var parent_div_id = modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF + "_right";
		
		modelplus.custom_display.selected_models = modelplus.custom_display.selected_models || [];
		
		// 1 - update the global variable
		while(modelplus.custom_display.selected_models.length > 0) { 
			modelplus.custom_display.selected_models.pop(); }
		$('#'+parent_div_id+' input:checked').each(function() {
			modelplus.custom_display.selected_models.push($(this).attr('value'));});
		richhydroforecast01.only_models = modelplus.custom_display.selected_models;
		
		// 2 - apply to current graph
		richhydroforecast01.onSlideChange();
		
		$('#'+ modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF).slideToggle("slow");
	}
	
	/**
	 *
	 */
	modelplus.custom_display.expand_forecasts_selection = function(btn, state_model_id){
		var build_div_id, parent_div_id;
		
		parent_div_id = modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF + "_left";
		$('#'+parent_div_id+' a').each(function() {
			$(this).css("background-color", "");
		});
		
		btn.style.backgroundColor = "#999";
		
		build_div_id = modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF + "_right";
		$("#" + build_div_id).children().each(function() { $(this).hide(); })
		
		build_div_id = modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF + "_right_" + state_model_id;
		$("#" + build_div_id).show();
	}
	
	/**
	 *
	 */
	function icon_on_click(){
		var runset_id, model_id, link_id, chart_lib_url, forecastset_url;
		var DIV_ID = "modal_content_hidrograph_div_div";
		var SLIDER_ID = "modal_content_hidrograph_div_slider";
		var SPANDIV_CLASS = "span_div";
		var SPAN_ID = "modal_content_hidrograph_div_span";
		var glb = GLB_vars.prototype;
				
		// set up variables						
		runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
		model_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
		link_id = this.id;

		// create popup div and add 
		modelplus.hydrograph.create_tmp();
		$('#'+modelplus.ids.MODAL_HYDROGRAPH_IFISBASED).append("<div id='"+DIV_ID+"'></div>");
		$('#'+modelplus.ids.MODAL_HYDROGRAPH_IFISBASED).append(
		  "<div class='navigation_div'>\
		     <input id='"+SLIDER_ID+"' type='range' onchange='richhydroforecast01.onSlideChange()' oninput='richhydroforecast01.onSlideInput()'/> \
		     <div class='span_div'>Issue time: <span id='"+SPAN_ID+"'></div> \
		   </div> \
		   <div class='panel_div'> \
		     <div class='header' onclick='modelplus.custom_display.config_on_click();'> \
		       <span >Model selection</span> \
			 </div> \
			 <div id='"+modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF+"' > \
			   <div class='body'> \
                 <div id='"+modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF+"_left' class='left'></div> \
                 <div id='"+modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF+"_right' class='right'></div> \
               </div> \
			   <div class='footer'> \
			     <a id='config_update_button' onclick='modelplus.custom_display.config_update()'>Update Graph</a>\
			   </div> \
			 </div> \
		   </div>");
		
		richhydroforecast01.runsetid = glb.sc_runset.id;
		richhydroforecast01.modelcomb_id = "richforecasts";  // TODO - make it variable
		richhydroforecast01.link_id = link_id;
		richhydroforecast01.only_models = null;
		
		var cb_build_hydrograph = function(data){
			richhydroforecast01.init(DIV_ID, SLIDER_ID, SPAN_ID, data);
			richhydroforecast01.buildHydroforecast();
			modelplus.hydrograph.addHeader({position:'absolute', div_id:modelplus.ids.MODAL_HYDROGRAPH_IFISBASED});
			richhydroforecast01.onSlideChange();
		};

		var cb_get_forecast_set = function(data){
			// build menu
			var target_dom_l, target_dom_r, inner_html, jdon_obj, additional_div, additional_div_id;
			jdon_obj = JSON.parse(data);
			target_dom_l = $("#"+modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF+"_left");
			target_dom_r = $("#"+modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF+"_right");
			
			// build interface
			$.each(jdon_obj, function(keyb, valb) {
				var mode_id = modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF+"_left_"+keyb;
				var default_model_id = typeof(valb["default_scenario"]) === 'undefined' ? null : valb["default_scenario"];
				
				// build left button
				var a_obj = $("<a onclick='modelplus.custom_display.expand_forecasts_selection(this, \""+keyb+"\")'>");
				a_obj.attr("id", mode_id);
				a_obj.css("cursor", "pointer");
				a_obj.css("float", "right");
				a_obj.html(valb["title"]);
				target_dom_l.append(a_obj);
				target_dom_l.append("<br />");
				
				// build right div
				additional_div_id = modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF + "_right_" + keyb;
				additional_div = $("<div id='" + additional_div_id + "' style='display:none; border-left:1px solid #999;'></div>");
				target_dom_r.append(additional_div);
				$.each(valb["scenarios"], function(key, val) {
					var checkbox_obj, checkbox_label;
					var is_checked = '';
					if ((modelplus.custom_display.selected_models == null) && (key == default_model_id)){
						is_checked = 'checked="checked"';
						if (richhydroforecast01.only_models == null)
							richhydroforecast01.only_models = [];
						richhydroforecast01.only_models.push(default_model_id);
					}
					if ((modelplus.custom_display.selected_models != null) && (modelplus.custom_display.selected_models.indexOf(key) >= 0))
						is_checked = 'checked="checked"';
					checkbox_obj = $("<input type='checkbox' value='"+key+"' "+is_checked+" />");
					checkbox_label = $("<span>" + val["title"] + "</span><br />");
					additional_div.append(checkbox_obj);
					additional_div.append(checkbox_label);
				});
			});
			
			// build hydrograph
			richhydroforecast01.ajaxCall(null, false, null, cb_build_hydrograph, modelplus.custom_display.selected_models);  // change to null
		};
		
		// 
		forecastset_url = modelplus.url.proxy + modelplus.url.api;
		forecastset_url += "sc_forecast_set";
		forecastset_url += "%i%runset_id="+runset_id;
		
		$.ajax({url: forecastset_url, 
		        success: cb_get_forecast_set});

	}
	
	runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
	modelcomb_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
	var reprcomp_id = "richhydroforecast";
	
	all_links_dict = null;
	gages_location_dict = null;
	
	// build URLs
	root_url = modelplus.url.base_frontend_webservices;
	var icon_address = root_url + "imgs/map_icons/hidrog.png";
	ws_data_url = modelplus.viewer.ws + "custom_ws/" + reprcomp_id + ".php";
	ws_data_url += "%i%sc_runset_id=" + runset_id;
	ws_data_url += "%e%sc_modelcomb_id=" + modelcomb_id;
	
	var echart_lib_url = modelplus.url.custom_display_js_folder + "/echarts/dist/echarts.3_7.min.js";
	var hchart_lib_url = modelplus.url.custom_display_js_folder + "/libs/richhydroforecast01.js"
	
	// perform web services calls
	$.when($.getJSON(ws_data_url),
	       modelplus.api.get_gages_by_type([2, 3, 4], true, true))
      .then(function(data_1, data_2){
		all_links_dict = data_1[0];
		gages_location_dict = data_2[0];
		display_when_possible();
      });
	
	// build graphic after loading library
	modelplus.scripts.load(echart_lib_url, function(){
		display_when_possible();
	});
	modelplus.scripts.load(hchart_lib_url, function(){
		display_when_possible();
	});
	
	/**
	 * Function that only works properly when global vars 'all_links_dict' and 'gages_location_dict' are not null
	 * RETURN : None.
	 */
	function display_when_possible(){
		var cur_linkid, cur_latlng, cur_icon, cur_marker;
		
		// basic check - variables must have been set
		if ((all_links_dict == null) || (gages_location_dict == null)){ return; }
		if (typeof(richhydroforecast01) === 'undefined') { return; }
		if (typeof(echarts) === 'undefined') { return; }
		
		// create reference list for icon in global var if necessary
		if(typeof(GLB_visual.prototype.polygons[reprcomp_id]) === 'undefined'){
			GLB_visual.prototype.polygons[reprcomp_id] = [];
		}
		
		// for each link available, looks for a respective gauge location
		for(var idx=0; idx<gages_location_dict.length; idx++){
			cur_linkid = gages_location_dict[idx]["link_id"];
			
			// basic check - gage location was found
			if(typeof(all_links_dict[cur_linkid]) === 'undefined')
			  continue;
			
			// define icon, marker and its action
			cur_latlng = {lat:parseFloat(gages_location_dict[idx]["lat"]),
			              lng:parseFloat(gages_location_dict[idx]["lng"])};
			cur_icon = {
				url: icon_address,
				origin: new google.maps.Point(0,0),
				anchor: new google.maps.Point(7,7)
			};
			cur_marker = new google.maps.Marker({
				position:cur_latlng,
				map:map,
				icon:cur_icon,
				title:gages_location_dict[idx].description,
				id:gages_location_dict[idx].link_id
			});
			
			google.maps.event.addListener(cur_marker, "click", icon_on_click);
			
			// add polygon to the reference list
			GLB_visual.prototype.polygons[reprcomp_id].push(cur_marker);
		}
	}
	
	/**
	 *
	 * runset_id: 
	 * model_id: 
	 * reference_id: 
	 * link_id: 
	 * timestamp: 
	 * RETURN:
	 */
	function get_rawdata_url(runset_id, model_id, reprcomp_id, link_id){
		var retr_url;
		retr_url = modelplus.viewer.ws + "custom_ws/"+reprcomp_id+"_readjson.php";
		retr_url += "%i%sc_runset_id="+runset_id;
		retr_url += "%e%sc_model_id="+model_id;
		retr_url += "%e%link_id="+link_id;
		retr_url += "%i%sc_models_only="+modelplus.custom_display.selected_models.join(",");
		return(retr_url);
	}
}
