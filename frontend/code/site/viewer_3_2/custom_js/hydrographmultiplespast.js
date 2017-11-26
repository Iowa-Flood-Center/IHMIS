function custom_display(){
	var modelcomb_id, runset_id, represcomb_id;
	var all_links_dict, gages_location_dict;
	var root_url, ws_data_url;
	
	/**
	 *
	 * model_number :
	 * total_models
	 * RETURN :
	 */
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
	
	runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
	modelcomb_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
	reprcomp_id = "hydrographmultiplespast";
	
	all_links_dict = null;
	gages_location_dict = null;
	
	// build URLs
	root_url = modelplus.url.base_frontend_webservices;
	icon_address = root_url + "imgs/map_icons/hidrog.png";
	ws_data_url = GLB_webservices.prototype.http + "custom_ws/"+reprcomp_id+".php%i%sc_runset_id="+runset_id+"%e%sc_modelcomb_id="+modelcomb_id;
	ws_gages_location_url = GLB_webservices.prototype.http + "ws_gages_location.php";
	
	// load all links available
	$.ajax({
		url: ws_data_url
	}).success(function(data){
		all_links_dict = JSON.parse(data);
		display_when_possible();
	});
	
	// load all locations
	$.ajax({
		url: ws_gages_location_url
	}).success(function(data){
		gages_location_dict = JSON.parse(data);
		display_when_possible();
	});
	
	/**
	 * Function that only works properly when global vars 'all_links_dict' and 'gages_location_dict' are not null
	 * RETURN : None.
	 */
	function display_when_possible(){
		var chart_lib_url;
		var json_gage, cur_linkid;
		var cur_latlng, cur_icon, cur_marker;
		// var count_found=0, count_missed=0;
		
		// basic check - variables must have been set
		if ((all_links_dict == null) || (gages_location_dict == null)){ return; }
		
		chart_lib_url = modelplus.url.base_frontend_webservices + "/custom_js/echarts/dist/echarts.js";
		
		// create reference list for icon in global var if necessary
		if(typeof(GLB_visual.prototype.polygons[reprcomp_id]) === 'undefined'){
			GLB_visual.prototype.polygons[reprcomp_id] = [];
		}
		
		// for each link available, looks for a respective gauge location
		json_gage = gages_location_dict["gauge"];
		for(idx=0; idx<json_gage.length; idx++){
			cur_linkid = json_gage[idx]["link_id"];
			
			// basic check - gage location was found
			if(typeof(all_links_dict[cur_linkid]) === 'undefined'){ continue; }
			
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
			
			google.maps.event.addListener(cur_marker, "click", function () {
				var runset_id, model_id, link_id, json_reader_ws;
				
				// set up variables						
				runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
				model_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
				link_id = this.id;
				
				json_reader_ws = GLB_webservices.prototype.http + "custom_ws/"+reprcomp_id+"_readjson.php%i%sc_runset_id="+runset_id+"%e%sc_model_id="+model_id+"%e%link_id="+link_id;
				
				modelplus.hydrograph.create();
				// display_hidrograph_block("");  // TODO - disappear with that
				
				// configure for module loader
				require.config({
					paths: {
						echarts: root_url + 'custom_js/echarts/dist'
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
				
						console.log("hydrographmultiplespast: Calling '" + json_reader_ws + "'.");
						$.ajax({
							url: json_reader_ws
						}).done(function(data){
							var json_data, myChart, div_modal_ctt, inner_html, option;
							var min_y_label, max_y_label, counter_mdls;
							var title_str, legend_array;
							var cur_stage_pair, cur_stage_index, cur_date;
							var min_timestamp, max_timestamp;
							var cur_max_y = null;
							var cur_max_y_idx = null;
							
							// read and parse data
							json_data = JSON.parse(data);
							// console.log("hydrographmultiplespast: Data for graph is '" + data + "'.");
							
							title_str = "Station: " + json_data["common"]["description"];
							subtitle_str = "Drainage Area: " + json_data["common"]["up_area"].toFixed(2) + "km^2";
							
							// define legend, y-min, y-max
							series_obj = [];
							legend_array = [];
							min_y_label = -1;
							max_y_label = 0;
							min_timestamp = 0;
							max_timestamp = 0;
							counter_mdls = 1;
							for(var k in json_data["past"]){ 
								cur_max_y = null;
								for(var cur_stage_index in json_data["past"][k]["stage_mdl"]){
									
									// evaluate y value for global max/min 
									cur_stage_pair = json_data["past"][k]["stage_mdl"][cur_stage_index];
									if((cur_stage_pair[1] < min_y_label) || (min_y_label == -1)){
										min_y_label = cur_stage_pair[1]; 
									}
									if ((cur_stage_pair[1] > max_y_label) || (max_y_label == 0)){
										max_y_label = cur_stage_pair[1];
									}
									
									// evaluate y value for local max/min
									if ((cur_max_y == null)||(cur_max_y < cur_stage_pair[1])){
										cur_max_y = cur_stage_pair[1];
										cur_max_y_idx = cur_stage_index;
									}
									
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
								json_data["past"][k]["stage_mdl"][cur_max_y_idx][2] = 20;
								
								legend_array.push(json_data["past"][k]["sc_model_title"]);
								cur_model_color = graph_color(counter_mdls, Object.keys(json_data["past"]).length);
								series_obj.push({
									name: json_data["past"][k]["sc_model_title"],
									type: "line",
									smooth: true,
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
							console.log("Found " + Object.keys(json_data["sref"]).length + " tags of 'sref'.");
							for(var k in json_data["sref"]){
								max_sref_idx = -1;
								max_sref_stg = -1;
								for(var cur_stage_index in json_data["sref"][k]["stage_obs"]){
									// evaluate y value for max/min
									cur_stage_pair = json_data["sref"][k]["stage_obs"][cur_stage_index];
									if((cur_stage_pair[1] < min_y_label) || (min_y_label == -1)){
										min_y_label = cur_stage_pair[1]; }
									if ((cur_stage_pair[1] > max_y_label) || (max_y_label == 0)){
										max_y_label = cur_stage_pair[1]; }
									
									// convert timestamp to date
									cur_date = new Date(cur_stage_pair[0] * 1000);
									json_data["sref"][k]["stage_obs"][cur_stage_index][0] = cur_date;
									
									// register max value and index for timeseries
									if(cur_stage_pair[1] > max_sref_stg){
										max_sref_stg = cur_stage_pair[1];
										max_sref_idx = cur_stage_index;
									}
									
									// register min/max timestamp for graph
									if ((cur_stage_pair[0] < min_timestamp)||(min_timestamp == 0)){
										min_timestamp = cur_stage_pair[0];}
									if ((cur_stage_pair[0] > max_timestamp)||(max_timestamp == 0)){
										max_timestamp = cur_stage_pair[0];}
										
									json_data["sref"][k]["stage_obs"][cur_stage_index][2] = 10;
								}
								
								// highlight peak if possible
								if(max_sref_idx != -1){
									json_data["sref"][k]["stage_obs"][max_sref_idx][2] = 20;
								}
								
								// create graph line object
								correct_title = json_data["sref"][k]["sc_reference_title"];
								false_title = "Reference";
								contole_lenght = json_data["sref"][k]["stage_obs"].length;
								console.log("Adding reference with size " + contole_lenght);
								// console.log("Adding reference with size " + contole_lenght + " from " + json_data["sref"][k]["stage_obs"][0][0] + " to " + json_data["sref"][k]["stage_obs"][contole_lenght-1][0] + ".");
								// console.log("        from " + json_data["sref"][k]["stage_obs"][0][0] + " to " + json_data["sref"][k]["stage_obs"][contole_lenght-1][0] + ".");
								if (json_data["sref"][k]["stage_obs"].length > 0){
									legend_array.push(correct_title);
									series_obj.push({
										name: correct_title,
										type: "scatter",
										showAllSymbol: true,
										symbolSize: function (value){
											return Math.round(value[2]/10) + 2;
										},
										data: json_data["sref"][k]["stage_obs"],
										itemStyle:{
											normal:{
												color: "#000000"
											}
										}
									});
								}
							}
							
							// define thresholds
							if (json_data["common"]["stage_threshold_act"] != null){
								// build graphic object
								myDataThrAct = [[min_timestamp, json_data["common"]["stage_threshold_act"]],
												[max_timestamp, json_data["common"]["stage_threshold_act"]]];
								// legend_array.push("Action");
								series_obj.push({
									name: "Action",
									type: "line",
									symbol: "none",
									symbolSize: 0,
									showAllSymbol: false,
									data: myDataThrAct,
									itemStyle:{
										normal:{
											color: modelplus.COLOR_THRESHOLD_ACTION
										}
									},
									markPoint: {
									  itemStyle: {
										normal: {
										  color: 'transparent'
										}
									  },
									  label: {
										normal: {
										  show: true,
										  position: 'left',
										  formatter: function(){ return("Action") },
										  padding: [60, -17, 0, 0],
										  align: 'right',
										  textStyle: {
											color: modelplus.COLOR_THRESHOLD_ACTION,
											fontSize: 11
										  }
										}
									  },
									  data: [{
										coord: [max_timestamp, json_data["common"]["stage_threshold_act"]]
									  }]
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
								// legend_array.push("Flood");
								series_obj.push({
									name: "Flood",
									type: "line",
									symbol: "none",
									symbolSize: 0,
									showAllSymbol: false,
									data: myDataThrFld,
									itemStyle:{
										normal:{
											color: modelplus.COLOR_THRESHOLD_FLOOD
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
								// legend_array.push("Moderate");
								series_obj.push({
									name: "Moderate",
									type: "line",
									symbol: "none",
									symbolSize: 0,
									showAllSymbol: false,
									data: myDataThrMod,
									itemStyle:{
										normal:{
											color: modelplus.COLOR_THRESHOLD_MODERATE
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
								//legend_array.push("Major");
								series_obj.push({
									name: "Major",
									type: "line",
									symbol: "none",
									symbolSize: 0,
									showAllSymbol: false,
									data: myDataThrMaj,
									itemStyle:{
										normal:{
											color: modelplus.COLOR_THRESHOLD_MAJOR
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
							
							// Initialize after dom ready
							myChart = ec.init(document.getElementById('modal_content_hidrograph_div'));
							
							option = {
								title:{
									text:title_str,
									textStyle:{
										fontSize:30
									},
									itemGap:0,
									subtext:subtitle_str,
									subtextStyle:{
										color:'#444',
										fontSize:0
									}
								},
								backgroundColor: 'rgba(255,255,255,1)',
								tooltip: {
									show: true,
									formatter: function(parms){
										var stg_txt, date_txt;
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
									padding: '5',
									textStyle:{
										fontSize:20
									}
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
						
							// alert("Found "+ count_found +", missed "+ count_missed +" out of "+ ws_data_url.length + ".");
							/*
							div_modal_ctt = $('#modal_content_hidrograph_div');
							inner_html = "<p style='background-color:#FFFFFF'><span id='modal_close_span' onclick='close_model_hidrograph_desc()'>Close</span></p>";
							div_modal_ctt.append(inner_html);
							*/
							modelplus.hydrograph.addHeader();
						});
					}
				);
			});
			
			// add polygon to the reference list
			GLB_visual.prototype.polygons[reprcomp_id].push(cur_marker);
		}
		
		loadScript(chart_lib_url, function(){});
	}
	
	/**
	 *
	 * msg_html :
	 * RETURN :
	 */
	function display_hidrograph_block(hidrograph_img_url){
		var div_modal = document.getElementById('modal_hidrograph_div');
		var div_modal_ctt = $('#modal_content_hidrograph_div');
		var inner_html;
	
		div_modal.style.display = "block";
		// div_modal.style.height = "400px";
		// div_modal.style.width = "800px";
		//div_modal.style.backgroundColor="#FFFFFF";
		div_modal_ctt.css("background-color", "white");
		div_modal_ctt.height("500px");
		div_modal_ctt.width("850px");
		
		/*
		inner_html = "<p><span id='modal_close_span' onclick='close_model_hidrograph_desc()'>&#10799;</span></p>";
		inner_html += "<img src='" + hidrograph_img_url + "' />";
		div_modal_ctt.html(inner_html);
		*/
	}
}