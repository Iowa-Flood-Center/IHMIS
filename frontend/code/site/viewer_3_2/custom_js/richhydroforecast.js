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
	 * model_number :
	 * total_models
	 * RETURN :
	 */
	/*
	function graph_color(model_number, total_models){
		var r_min, g_min, b_min;
		var r_num, g_num, b_num;
		var r_hex, g_hex, b_hex;
		var delta, i;
		
		delta = total_models;
		// i = delta - model_number;
		i = model_number;
		
		r_min = 5;
		g_max = 14;  g_delta = 6;
		b_min = 15;
		
		if (delta == 1){
			r_num = r_min;
			g_num = g_max - g_delta;
			b_num = b_min;
		} else {
			g_delta = ((model_number - 1)/(delta - 1)) * g_delta;
			r_num = Math.round((i/delta) * r_min);
			g_num = Math.round(g_max - g_delta);
			b_num = Math.round((i/delta) * b_min);
		}
		
		r_hex = color_num_to_hex(r_num);
		g_hex = color_num_to_hex(g_num);
		b_hex = color_num_to_hex(b_num);
		
		return("#" + r_hex + r_hex + g_hex + g_hex + b_hex + b_hex);
	}
	*/
	
	
	
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
		const DIV_ID = "modal_content_hidrograph_div_div";
		const SLIDER_ID = "modal_content_hidrograph_div_slider";
		const SPAN_ID = "modal_content_hidrograph_div_span";
				
		// set up variables						
		runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
		model_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
		link_id = this.id;

		// create popup div and add 
		modelplus.hydrograph.create_tmp();
		$('#'+modelplus.ids.MODAL_HYDROGRAPH_IFISBASED).append("<div id='"+DIV_ID+"' style='width:850px; height:460px; display:block;'></div>");
		$('#'+modelplus.ids.MODAL_HYDROGRAPH_IFISBASED).append(
		  "<div style='width:100%; display:block; padding-top:30px'>\
		     <input id='"+SLIDER_ID+"' type='range' style='width:400px; margin-left:40px' onchange='richhydroforecast01.onSlideChange()' oninput='richhydroforecast01.onSlideInput()'/> \
		     <div style='float:right; padding-right:10px'>Issue time: <span id='"+SPAN_ID+"'></div> \
		   </div> \
		   <div style='position:absolute; width:730px; display:block; margin-left:60px; bottom:0px; background-color:#ddd'> \
		     <div style='background-color:#bbb; padding-left:15px; cursor:pointer' onclick='modelplus.custom_display.config_on_click();'> \
		       <span >Model selection</span> \
			 </div> \
			 <div id='"+modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF+"' style='display:none; padding-left:25px; padding-right:22px; height:400px;'> \
			   <div style='display:table-row; height:362px'> \
                 <div id='"+modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF+"_left' style='float:left; text-align:left; padding-top:5px'></div> \
                 <div id='"+modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF+"_right' style='float:left; text-align:left'></div> \
               </div> \
			   <div style='display:table-row; text-align:right; float:right; margin-bottom:22px; cursor:pointer; bottom:0px; right:15px'> \
			     <a id='config_update_button' onclick='modelplus.custom_display.config_update()'>Update Graph</a>\
			   </div> \
			 </div> \
		   </div>");
		
		richhydroforecast01.runsetid = "realtime";           // TODO - make it variable
		richhydroforecast01.modelcomb_id = "richforecasts";  // TODO - make it variable
		richhydroforecast01.link_id = link_id;               // 
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
			console.log(JSON.stringify(modelplus.custom_display.selected_models));
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
	ws_data_url = GLB_webservices.prototype.http + "custom_ws/"+reprcomp_id+".php%i%sc_runset_id="+runset_id+"%e%sc_modelcomb_id="+modelcomb_id;
	var ws_gages_location_url = GLB_webservices.prototype.http + "ws_gages_location.php";
	
	var echart_lib_url = modelplus.url.base_frontend_webservices + "/custom_js/echarts/dist/echarts.3_7.min.js";
	var hchart_lib_url = modelplus.url.base_frontend_webservices + "/custom_js/libs/richhydroforecast01.js"
	
	// load all links available
	$.ajax({
		url: ws_data_url
	}).success(function(data){
		all_links_dict = JSON.parse(data);
		console.log("Got links: " + data);
		display_when_possible();
	});
	
	// load all locations
	$.ajax({
		url: ws_gages_location_url
	}).success(function(data){
		gages_location_dict = JSON.parse(data);
		display_when_possible();
	});
	
	// build graphic after loading library
	loadScript(echart_lib_url, function(){
		display_when_possible();
	});
	loadScript(hchart_lib_url, function(){
		display_when_possible();
	});
	
	/**
	 * Function that only works properly when global vars 'all_links_dict' and 'gages_location_dict' are not null
	 * RETURN : None.
	 */
	function display_when_possible(){
		var json_gage, cur_linkid;
		var cur_latlng, cur_icon, cur_marker;
		// var count_found=0, count_missed=0;
		
		// basic check - variables must have been set
		console.log("Is it possible to call?");
		if ((all_links_dict == null) || (gages_location_dict == null)){ return; }
		if (typeof(richhydroforecast01) === 'undefined') { return; }
		if (typeof(echarts) === 'undefined') { return; }
		
		// create reference list for icon in global var if necessary
		if(typeof(GLB_visual.prototype.polygons[reprcomp_id]) === 'undefined'){
			GLB_visual.prototype.polygons[reprcomp_id] = [];
		}
		
		// for each link available, looks for a respective gauge location
		json_gage = gages_location_dict["gauge"];
		console.log("Showing "+json_gage.length+" icons.");
		for(var idx=0; idx<json_gage.length; idx++){
			cur_linkid = json_gage[idx]["link_id"];
			
			// basic check - gage location was found
			if(typeof(all_links_dict[cur_linkid]) === 'undefined'){ 
			  console.log("Ignoring idx "+idx+".");
			  continue;
			}
			
			// define icon, marker and its action
			cur_latlng = {lat:parseFloat(json_gage[idx]["lat"]),
			              lng:parseFloat(json_gage[idx]["lng"])};
			cur_icon = {
				url: icon_address,
				origin: new google.maps.Point(0,0),
				anchor: new google.maps.Point(7,7)
			};
			cur_marker = new google.maps.Marker({
				position:cur_latlng,
				map:map,
				icon:cur_icon,
				title:json_gage[idx].desc,
				id:json_gage[idx].link_id
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
		retr_url = GLB_webservices.prototype.http + "custom_ws/"+reprcomp_id+"_readjson.php";
		retr_url += "%i%sc_runset_id="+runset_id;
		retr_url += "%e%sc_model_id="+model_id;
		retr_url += "%e%link_id="+link_id;
		retr_url += "%i%sc_models_only="+modelplus.custom_display.selected_models.join(",");
		return(retr_url);
	}
}