function custom_display(){
	"use strict";
	var runset_id, modelcomb_id, reprcomp_id;
	var all_links_dict, gages_location_dict;
	
	/**
	 *
	 * model_number :
	 * total_models
	 * RETURN :
	 */
	function graph_color(model_number, total_models){
		var r_min, g_max, b_min;
		var r_num, g_num, b_num;
		var r_hex, g_hex, b_hex;
		var delta, g_delta, i;
		
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
	
	reprcomp_id = "hydrographmultiplesdot";
	all_links_dict = null;
	gages_location_dict = null;
	
	// get basic info
	runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
	modelcomb_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
	
	// build urls
	var root_url = modelplus.url.base_frontend_webservices;
	var icon_root_address = root_url + "imgs/map_icons/";
	var ws_data_url = modelplus.viewer.ws + "custom_ws/"+reprcomp_id+".php%i%sc_runset_id="+runset_id+"%e%sc_modelcomb_id="+modelcomb_id;
	var ws_gages_location_url = modelplus.viewer.ws + "ws_gages_location.php%i%filedate=20170328";
	
	// load all links available
	$.ajax({
		url: ws_data_url
	}).success(function(data){
		all_links_dict = JSON.parse(data);
		if (all_links_dict == null){ console.log("hydrographmultiplesdot: got null for all links."); }
		display_when_possible();
	});
	
	// load all locations
	console.log("hydrographmultiplesdot: calling '"+ws_gages_location_url+"'.");
	$.ajax({
		url: ws_gages_location_url
	}).success(function(data){
		gages_location_dict = JSON.parse(data);
		if (all_links_dict == null){ console.log("hydrographmultiplesdot: got null for gages location."); }
		display_when_possible();
	});
	
	/**
	 * Function that only works properly when global vars 'all_links_dict' and 'gages_location_dict' are not null
	 * RETURN : None.
	 */
	function display_when_possible(){
		var cur_icon_address;
		
		// basic check - variables must have been set
		if ((all_links_dict == null) || (gages_location_dict == null)){ return; }
		
		// create reference list for icon in global var if necessary
		if(typeof(GLB_visual.prototype.polygons[reprcomp_id]) === 'undefined'){
			GLB_visual.prototype.polygons[reprcomp_id] = [];
		}
		
		// debug
		// keys = [];
		// for(var k in all_links_dict) keys.push(k);
		// console.log("Total: " + keys.length + " ("+typeof(keys[1])+"). Keys: " + keys);
		
		// load charts library
		var chart_lib_url = modelplus.url.custom_display_js_folder + "/echarts/dist/echarts.js";
		
		// for each link available, looks for a respective gauge location
		var json_gage = gages_location_dict["gauge"];
		var cur_linkid, cur_latlng, cur_icon, cur_marker;
		for(var idx=0; idx<json_gage.length; idx++){
			cur_linkid = json_gage[idx]["link_id"].toString();
			
			// basic check - gage location and alert was found
			if(typeof(all_links_dict[cur_linkid]) === 'undefined'){ 
				// console.log("hydrographmultiplesdot: Not found link id " + cur_linkid + " in alert flags.");
				continue;
			}
			
			// define icon image
			if (all_links_dict[cur_linkid] == 0){
				cur_icon_address = icon_root_address + "gauge_wtf.png";
			} else if (all_links_dict[cur_linkid] == -5){
				cur_icon_address = icon_root_address + "virtual_dot.png";
			} else if (all_links_dict[cur_linkid] == -6){
				cur_icon_address = icon_root_address + "gauge_dot.png";
			} else {
				
			}
			// console.log("hydrographmultiplesdot: For link " + cur_linkid + ", created '" + cur_icon_address + "'.");
			
			// define marker position
			cur_latlng = {lat:parseFloat(json_gage[idx]["lat"]),
			              lng:parseFloat(json_gage[idx]["lng"])};
			cur_icon = {
				url: cur_icon_address,
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
			
			// define marker on-click action
			google.maps.event.addListener(cur_marker, "click", on_icon_click);
			
			// add polygon to the reference list
			GLB_visual.prototype.polygons[reprcomp_id].push(cur_marker);
		}
		
		loadScript(chart_lib_url, function(){});
	}
	
	function on_icon_click() {
		var runset_id, model_id, link_id, json_reader_ws;
		// var modal_ctt_div_id = 'modal_content_hidrograph_div';
		
		// set up variables						
		runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
		model_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
		link_id = this.id;
		
		json_reader_ws = modelplus.viewer.ws;
		json_reader_ws += "custom_ws/"+reprcomp_id+"_readjson.php";
		json_reader_ws += "%i%sc_runset_id="+runset_id;
		json_reader_ws += "%e%sc_model_id="+model_id;
		json_reader_ws += "%e%link_id="+link_id;
		
		modelplus.hydrograph.create_tmp();
		
		console.log("hydrographmultiplesdot: Loaded '"+json_reader_ws+"'.");
		
		// configure for module loader
		require.config({
			paths: {
				echarts: modelplus.url.custom_display_js_folder + '/echarts/dist'
			}
		});
		
		// use
		require(
			[
				'echarts',
				'echarts/chart/line',    // require the specific chart type 'line'
				'echarts/chart/scatter' // require the specific chart type 'scatter'
			],
					
			function (ec) {
		
				// alert("Calling " + json_reader_ws);
				$.ajax({
					url: json_reader_ws
				}).done(function(data){
					var json_data, myChart, div_modal_ctt, inner_html, option;
					var cur_delta_glue, delta_glue_dict, glue_ref, glue_idx;
					var cur_stage_pair, cur_stage_index, cur_date;
					var title_str, legend_array, series_obj;
					var min_timestamp, max_timestamp;
					var min_y_label, max_y_label;
					var cur_past_model_id, cur_model_color;
					
					// read and parse data
					json_data = JSON.parse(data);
					
					title_str = "Station: " + json_data["common"]["desc"];
					var subtitle_str = "Drainage Area: " + json_data["common"]["area"] + " km^2";
					
					// define delta glue for past
					glue_ref = null;
					for(cur_past_model_id in json_data["past"]){
						if(cur_past_model_id.endsWith("ref")){
							glue_idx = json_data["past"][cur_past_model_id]["stage_mdl"].length - 1;
							glue_ref = json_data["past"][cur_past_model_id]["stage_mdl"][glue_idx][1];
						}
					}
					if (glue_ref != null){
						delta_glue_dict = {};
						for(cur_past_model_id in json_data["past"]){
							if(cur_past_model_id.endsWith("ref")){
								delta_glue_dict[cur_past_model_id] = 0;
							} else {
								glue_idx = json_data["past"][cur_past_model_id]["stage_mdl"].length - 1;
								cur_delta_glue = glue_ref - json_data["past"][cur_past_model_id]["stage_mdl"][glue_idx][1];
								delta_glue_dict[cur_past_model_id] = cur_delta_glue;
							}
						}
					} else {
						delta_glue_dict = null;
					}
					
					// define legend, y-min, y-max 
					series_obj = [];
					legend_array = [];
					min_y_label = -1;
					max_y_label = 0;
					min_timestamp = 0;
					max_timestamp = 0;
					var counter_mdls = 1;
					var total_mdls = Object.keys(json_data["past"]).length + Object.keys(json_data["fore"]).length;
					var max_past_timestamp = null;
					for(var k in json_data["past"]){
						
						// define glue
						if(delta_glue_dict != null){
							if(!(k in delta_glue_dict)){
								console.log("hydrographmultiplesdot: Delta glue not found for '" + k + "'.");
								cur_delta_glue = 0;
							} else {
								cur_delta_glue = delta_glue_dict[k];
							}
						} else {
							cur_delta_glue = 0;
						}
						
						// convert dates and apply glue
						for(var cur_stage_index in json_data["past"][k]["stage_mdl"]){
							cur_stage_pair = json_data["past"][k]["stage_mdl"][cur_stage_index];

							// glue if necessary
							cur_stage_pair[1] = cur_stage_pair[1] + cur_delta_glue;
							
							// evaluate y value for max/min
							if((cur_stage_pair[1] < min_y_label) || (min_y_label == -1)){
								min_y_label = cur_stage_pair[1]; }
							if ((cur_stage_pair[1] > max_y_label) || (max_y_label == 0)){
								max_y_label = cur_stage_pair[1]; }
							
							// convert timestamp to date
							cur_date = new Date(cur_stage_pair[0] * 1000);
							json_data["past"][k]["stage_mdl"][cur_stage_index][0] = cur_date;
							
							// register min/max timestamp
							if ((cur_stage_pair[0] < min_timestamp)||(min_timestamp == 0)){
								min_timestamp = cur_stage_pair[0];
							}
							if ((cur_stage_pair[0] > max_timestamp)||(max_timestamp == 0)){
								max_timestamp = cur_stage_pair[0];
							}
						}
						json_data["past"][k]["stage_mdl"][cur_stage_index][2] = 20;
						
						// register max past timestamp
						if ((max_past_timestamp == null)||(max_past_timestamp < max_timestamp)){
							max_past_timestamp = max_timestamp;
						}
						
						legend_array.push(GLB_vars.prototype.get_model_name(k));
						if(k.endsWith("ref")){
							cur_model_color = modelplus.COLOR_REFERENCE;
						} else {
							cur_model_color = graph_color(counter_mdls, total_mdls);
						}
						series_obj.push({
							name: GLB_vars.prototype.get_model_name(k),
							type: "line",
							showAllSymbol: true,
							symbolSize: function (value){
								return Math.round(value[2]/10) + 2;
							},
							data: json_data["past"][k]["stage_mdl"],
							itemStyle:{
								normal:{
									color: cur_model_color,
									lineStyle:{ type:"solid" }
								}
							}
						});
						counter_mdls = counter_mdls + 1;
					}
					var max_fore_idx, max_fore_stg;
					for(var k in json_data["fore"]){
						max_fore_idx = -1;
						max_fore_stg = -1;
						for(var cur_stage_index in json_data["fore"][k]["stage_mdl"]){
							// evaluate y value for max/min
							cur_stage_pair = json_data["fore"][k]["stage_mdl"][cur_stage_index];
							if((cur_stage_pair[1] < min_y_label) || (min_y_label == -1)){
								min_y_label = cur_stage_pair[1]; }
							if ((cur_stage_pair[1] > max_y_label) || (max_y_label == 0)){
								max_y_label = cur_stage_pair[1]; }
							
							// convert timestamp to date
							cur_date = new Date(cur_stage_pair[0] * 1000);
							json_data["fore"][k]["stage_mdl"][cur_stage_index][0] = cur_date;
							
							// register max value and index for timeseries
							if(cur_stage_pair[1] > max_fore_stg){
								max_fore_stg = cur_stage_pair[1];
								max_fore_idx = cur_stage_index;
							}
							
							// register min/max timestamp for graph
							if ((cur_stage_pair[0] < min_timestamp)||(min_timestamp == 0)){
								min_timestamp = cur_stage_pair[0];}
							if ((cur_stage_pair[0] > max_timestamp)||(max_timestamp == 0)){
								max_timestamp = cur_stage_pair[0];}
						}
						
						// highlight peak if possible
						if(max_fore_idx != -1){
							json_data["fore"][k]["stage_mdl"][max_fore_idx][2] = 20;
						}
						
						// create graph line object
						legend_array.push(GLB_vars.prototype.get_model_name(k));  // TODO - convert to model title
						cur_model_color = graph_color(counter_mdls, total_mdls);
						series_obj.push({
							name: GLB_vars.prototype.get_model_name(k),
							type: "line",
							symbol: "circle",
							showAllSymbol: true,
							symbolSize: function (value){
								return Math.round(value[2]/10) + 2;
							},
							data: json_data["fore"][k]["stage_mdl"],
							itemStyle:{
								normal:{
									color: cur_model_color,
									lineStyle:{ type:"solid" }
								}
							}
						});
						
						counter_mdls = counter_mdls + 1;
					}
					for(var k in json_data["forealert"]){
						max_fore_idx = -1;
						max_fore_stg = -1;
						for(var cur_stage_index in json_data["forealert"][k]["stage_mdl"]){
							// evaluate y value for max/min
							cur_stage_pair = json_data["forealert"][k]["stage_mdl"][cur_stage_index];
							if((cur_stage_pair[1] < min_y_label) || (min_y_label == -1)){
								min_y_label = cur_stage_pair[1]; }
							if ((cur_stage_pair[1] > max_y_label) || (max_y_label == 0)){
								max_y_label = cur_stage_pair[1]; }
							
							// convert timestamp to date
							cur_date = new Date(cur_stage_pair[0] * 1000);
							json_data["forealert"][k]["stage_mdl"][cur_stage_index][0] = cur_date;
							
							// register max value and index for timeseries
							if(cur_stage_pair[1] > max_fore_stg){
								max_fore_stg = cur_stage_pair[1];
								max_fore_idx = cur_stage_index;
							}
							
							// register min/max timestamp for graph
							if ((cur_stage_pair[0] < min_timestamp)||(min_timestamp == 0)){
								min_timestamp = cur_stage_pair[0];}
							if ((cur_stage_pair[0] > max_timestamp)||(max_timestamp == 0)){
								max_timestamp = cur_stage_pair[0];}
						}
						
						// highlight peak if possible
						if(max_fore_idx != -1){
							json_data["forealert"][k]["stage_mdl"][max_fore_idx][2] = 20;
						}
						
						// create graph line object
						legend_array.push(GLB_vars.prototype.get_model_name(k));  // TODO - convert to model title
						cur_model_color = graph_color(counter_mdls, total_mdls);
						series_obj.push({
							name: GLB_vars.prototype.get_model_name(k),
							type: "line",
							symbol: "circle",
							showAllSymbol: true,
							symbolSize: function (value){
								return Math.round(value[2]/10) + 2;
							},
							data: json_data["forealert"][k]["stage_mdl"],
							itemStyle:{
								normal:{
									color: cur_model_color,
									lineStyle:{ type:"solid" }
								}
							}
						});
						
						counter_mdls = counter_mdls + 1;
					}
					
					var myDataThrAct, myDataThrFld, myDataThrMod, myDataThrMaj;
					
					// define thresholds
					if ((json_data["common"]["stage_threshold_act"] != null) && (json_data["common"]["stage_threshold_act"] != -1)){
						// build graphic object
						myDataThrAct = [[min_timestamp, json_data["common"]["stage_threshold_act"]],
										[max_timestamp, json_data["common"]["stage_threshold_act"]]];
						legend_array.push("Action");
						series_obj.push({
							name: "Action",
							type: "line",
							symbol: "none",
							symbolSize: 0,
							showAllSymbol: false,
							data: myDataThrAct,
							itemStyle:{
								normal:{
									color: modelplus.COLOR_THRESHOLD_ACTION,
									lineStyle:{ type:"dashed" }
								}
							}
						});
						// try to update labels
						if (max_y_label < json_data["common"]["stage_threshold_act"]){
							max_y_label = json_data["common"]["stage_threshold_act"];}
						if (min_y_label > json_data["common"]["stage_threshold_act"]){
							min_y_label = json_data["common"]["stage_threshold_act"];}
					}
					
					if (json_data["common"]["stage_threshold_fld"] != null){
						// build graphic object
						myDataThrFld = [[min_timestamp, json_data["common"]["stage_threshold_fld"]],
										[max_timestamp, json_data["common"]["stage_threshold_fld"]]];
						legend_array.push("Flood");
						series_obj.push({
							name: "Flood",
							type: "line",
							symbol: "none",
							symbolSize: 0,
							showAllSymbol: false,
							data: myDataThrFld,
							itemStyle:{
								normal:{
									color: modelplus.COLOR_THRESHOLD_FLOOD,
									lineStyle:{ type:"dashed" }
								}
							}
						});
						// try to update labels
						if (max_y_label < json_data["common"]["stage_threshold_fld"]){
							max_y_label = json_data["common"]["stage_threshold_fld"];}
						if (min_y_label > json_data["common"]["stage_threshold_fld"]){
							min_y_label = json_data["common"]["stage_threshold_fld"];}
					}
					if (json_data["common"]["stage_threshold_mod"] != null){
						// build graphic object
						myDataThrMod = [[min_timestamp, json_data["common"]["stage_threshold_mod"]],
										[max_timestamp, json_data["common"]["stage_threshold_mod"]]];
						legend_array.push("Moderate");
						series_obj.push({
							name: "Moderate",
							type: "line",
							symbol: "none",
							symbolSize: 0,
							showAllSymbol: false,
							data: myDataThrMod,
							itemStyle:{
								normal:{
									color: modelplus.COLOR_THRESHOLD_MODERATE,
									lineStyle:{ type:"dashed" }
								}
							}
						});
						// try to update labels
						if (max_y_label < json_data["common"]["stage_threshold_mod"]){
							max_y_label = json_data["common"]["stage_threshold_mod"];}
						if (min_y_label > json_data["common"]["stage_threshold_mod"]){
							min_y_label = json_data["common"]["stage_threshold_mod"];}
					}
					if (json_data["common"]["stage_threshold_maj"] != null){
						// build graphic object
						myDataThrMaj = [[min_timestamp, json_data["common"]["stage_threshold_maj"]],
										[max_timestamp, json_data["common"]["stage_threshold_maj"]]];
						legend_array.push("Major");
						series_obj.push({
							name: "Major",
							type: "line",
							symbol: "none",
							symbolSize: 0,
							showAllSymbol: false,
							data: myDataThrMaj,
							itemStyle:{
								normal:{
									color: modelplus.COLOR_THRESHOLD_MAJOR,
									lineStyle:{ type:"dashed" }
								}
							}
						});
						// try to update labels
						if (max_y_label < json_data["common"]["stage_threshold_maj"]){
							max_y_label = json_data["common"]["stage_threshold_maj"];}
						if (min_y_label > json_data["common"]["stage_threshold_maj"]){
							min_y_label = json_data["common"]["stage_threshold_maj"];}
					}
					
					// round y labels extreme values
					max_y_label = Math.ceil(max_y_label + ((max_y_label - min_y_label) * 0.1));
					min_y_label = Math.floor(min_y_label - ((max_y_label - min_y_label) * 0.1));
					
					// add current time delimiter
					var current_date_data;
					if (max_past_timestamp != null){
						current_date_data = [[max_past_timestamp, max_y_label],
											 [max_past_timestamp, min_y_label]];
						if (max_past_timestamp != null){
							series_obj.push({
								name: "Now",
								type: "line",
								symbol: "none",
								symbolSize: 0,
								showAllSymbol: false,
								data: current_date_data,
								itemStyle:{
									normal:{
										color: modelplus.COLOR_NOW,
										lineStyle:{ type:"solid" }
									}
								}
							});
							legend_array.push("Now");
						}
					}
					
					// Initialize after dom ready
					var myChart = ec.init(document.getElementById(modelplus.ids.MODAL_HYDROGRAPH_IFISBASED));
					
					option = {
						title:{
							text:title_str,
							itemGap:0,
							subtext:subtitle_str,
							subtextStyle:{
								color:'#444',
								fontSize:12
							}
						},
						backgroundColor: 'rgba(255,255,255,1)',
						tooltip: {
							show: true,
							formatter: function(parms){
								var stg_txt, hour_txt, date_txt;
								stg_txt = "Stage:"+parms.value[1].toFixed(2)+" ft";
								hour_txt = force_two_digits(parms.value[0].getHours()) + ":" + force_two_digits(parms.value[0].getMinutes());
								date_txt = force_two_digits(parms.value[0].getDate()) + "/" + force_two_digits(parms.value[0].getMonth()+1) + "/" + parms.value[0].getFullYear();
								return(stg_txt + " at " + hour_txt + ", " + date_txt);
							}
						},
						legend: {
							data: legend_array,
							x: 'center',
							y: 'bottom',
							padding: '0',
							type: 'scroll'
						},
						xAxis : [
							{
								type : 'time',
								name : 'Time',
								axisLabel: {
									formatter: "MM/dd/yyyy"
								}
							}
						],
						yAxis : [
							{
								type : 'value',
								name : 'Stage [ft]',
								min : min_y_label,
								max: max_y_label
							}
						],
						toolbox: {
							show : true,
							feature : {
								saveAsImage : {show: true, title: 'Save image'},
								dataZoom : {show: true, title: 'Zoom'}
							}
						},
						series : series_obj
					};
					
					// Load data into the ECharts instance 
					myChart.setOption(option);
					
					modelplus.hydrograph.addHeader({
						position: 'absolute', 
						div_id: modelplus.ids.MODAL_HYDROGRAPH_IFISBASED});
				});
			}
		);
	}
}