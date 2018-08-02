function custom_display(){
	"use strict";

	var sc_runset_id, sc_model_id;
	var sc_evaluation_id;
	var base_url, json_reader_ws;
	var all_images_dict;  // TODO - create a decent way to call global variables
	
	sc_runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
	sc_model_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
	sc_evaluation_id = "hydrographsd";
	
	// get reference in selected button id
	var reference_id = "mock";	
	$(".npact").each(function() {
		var cur_radio_id, splitted_radio;
		cur_radio_id = $(this).attr('id');
		
		if(cur_radio_id.indexOf('_') > -1){
			splitted_radio = cur_radio_id.split("_");
			if(splitted_radio[0] == "np" + sc_evaluation_id){
				reference_id = splitted_radio[1];
			}
		}
	});
	
	// build relevant http addressees
	base_url = modelplus.url.base_frontend_webservices;
	var icon_address = base_url + "imgs/map_icons/hidrog.png";
	var ws_all_images_url = modelplus.viewer.ws + "custom_ws/hydrographsd.php";
	ws_all_images_url += "%i%sc_runset_id="+sc_runset_id;
	ws_all_images_url += "%e%sc_model_id="+sc_model_id;
	ws_all_images_url += "%e%sc_reference_id="+reference_id;
	
	// load all required data
	$.when($.getJSON(ws_all_images_url),
	       modelplus.api.get_gages_by_type([2, 3, 4], true, true))
	  .then(function(data_1, data_2){
        all_images_dict = data_1[0];
		var gages_location_dict = data_2[0];
		var chart_lib_url = modelplus.url.custom_display_js_folder + "/echarts/dist/echarts.js";
		modelplus.scripts.load(chart_lib_url, function(){
		  display_when_possible(all_images_dict, gages_location_dict);
		})
	  });
	  
	/**
	 *
	 * link_id : 
	 * timestamp : 
	 * RETURN :
	 */
	function build_json_name(link_id, timestamp){
		return(timestamp + "_" + link_id + ".png");
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
	function get_rawdata_url(runset_id, model_id, reference_id, link_id, timestamp){
		var retr_url;
		retr_url = modelplus.viewer.ws + "custom_ws/hydrographsd_readjson.php";
		retr_url += "%i%sc_runset_id="+runset_id;
		retr_url += "%e%sc_model_id="+model_id;
		retr_url += "%e%sc_reference_id="+reference_id;
		retr_url += "%e%link_id="+link_id;
		retr_url += "%e%timestamp="+timestamp;
		return(retr_url);
	}
	
	/**
	 * Plots all hydrograph icons on the maps.
	 * Only runs when global vars 'all_images_dict' and 'gages_location_dict' are not null
	 * RETURN : None.
	 */
	function display_when_possible(all_images_dict, gages_location_dict){

		// get reference id
		reference_id = "mock";
		$(".npact").each(function() {
			var cur_radio_id, splitted_radio;
			cur_radio_id = $(this).attr('id');
			if(cur_radio_id.indexOf('_') > -1){
				splitted_radio = cur_radio_id.split("_");
				if(splitted_radio[0] == "np" + sc_evaluation_id){
					reference_id = splitted_radio[1];
				}
			}
		});

		// for each gauge, searches if there is an image for it
		var cur_linkid, cur_latlng, cur_icon, cur_marker;
		var json_gage = gages_location_dict;
		for(var idx=0; idx<gages_location_dict.length; idx++){
			cur_linkid = gages_location_dict[idx]["link_id"];
			if(typeof(all_images_dict[cur_linkid]) !== 'undefined'){
				// define icon, marker and action
				cur_latlng = {lat:parseFloat(gages_location_dict[idx]["lat"]), 
				              lng:parseFloat(gages_location_dict[idx]["lng"])};
				cur_icon = {
					url: icon_address,
					origin: new google.maps.Point(0,0),
				anchor: new google.maps.Point(7,7)};
				cur_marker = new google.maps.Marker({
					position:cur_latlng,
					map:map,
					icon:cur_icon,
					title:gages_location_dict[idx].description,
					link_id:gages_location_dict[idx].link_id,
					reference_id:reference_id
						
				});
				google.maps.event.addListener(cur_marker, "click", on_icon_click);
				// create reference list for icon in global var if necessary
				if(typeof(GLB_visual.prototype.polygons[sc_evaluation_id]) === 'undefined'){
					GLB_visual.prototype.polygons[sc_evaluation_id] = [];
				}
				GLB_visual.prototype.polygons[sc_evaluation_id].push(cur_marker);
			}
		}
	}
	
	
	function on_icon_click() {

		var json_reader_ws, runset_id, model_id, reference_id, link_id, timestamp;
		var base_url = modelplus.url.base_frontend_webservices;
		
		// set up variables						
		runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
		model_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
		link_id = this.link_id;
		reference_id = this.reference_id;
		timestamp = all_images_dict[this.link_id];
		
		// 
		json_reader_ws = get_rawdata_url(runset_id, model_id, reference_id, link_id, timestamp);
		
		modelplus.hydrograph.create_tmp();
		
		
		/********************************************************************************************/
		
		
		
		var url_form;
		var base_url = modelplus.url.base_frontend_webservices;
					
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
			
				$.ajax({
					url: json_reader_ws
				}).done(function(data){
				
					// read and parse data
					var json_data = JSON.parse(data);
				
					// prepare data objects
					var title_str, title_desc_str, title_area_str;
					var myDataObs = [];
					var myDataMdl = null;
					var myDataThrAct = [];
					var myDataThrFld = [];
					var myDataThrMod = [];
					var myDataThrMaj = [];
					var cur_element, count;
					var min_timestamp = null;
					var max_timestamp = null;
					var max_data = 0;
					var min_data = null;
					var max_y_label, min_y_label;
					var max_x_label, min_x_label;
					var prv_mdl_val, cur_mdl_val;
					var max_mdl_val, max_mdl_idx;
					var count_added;
					var min_timestamp_mdl = null;
					var min_timestamp_obs = null;
					var subtitle_str = null;
					
					function get_model_hidrograph_raw_data(args){
						var raw_data_url;
						raw_data_url = get_rawdata_url(args["runset_id"],
						                               args["model_id"],
													   args["reference_id"],
													   args["link_id"],
													   args["timestamp"]);
						window.open(raw_data_url);
					}
					
					// fill model list object
					max_mdl_val = 0;
					max_mdl_idx = null;
					prv_mdl_val = null;
					cur_mdl_val = null;
					count_added = 0;
					for(count = 0; count < json_data.stage_mdl.length; count++){
						cur_mdl_val = json_data.stage_mdl[count][1];
						cur_element = [new Date(json_data.stage_mdl[count][0] * 1000), cur_mdl_val];
						
						// basic check - ignore null values
						if (cur_mdl_val == null){ continue; }
						
						// basic check - continuity broken - restart the timeseries
						if ((prv_mdl_val == null)||((cur_mdl_val * 2) < prv_mdl_val)||((cur_mdl_val / 2) > prv_mdl_val)){
							// delete myDataMdl;
							myDataMdl = [];
							count_added = 0;
							min_timestamp_mdl = null;
							max_mdl_val = 0;
						}
						
						// add to the time series
						myDataMdl.push(cur_element);
						prv_mdl_val = cur_mdl_val;
						count_added = count_added + 1;
						
						// check max value
						if (cur_mdl_val > max_mdl_val){
							max_mdl_val = cur_mdl_val;
							max_mdl_idx = count_added;
						}
						
						// check min value
						if ((min_data == null) || (cur_mdl_val < min_data)){
							min_data = cur_mdl_val;
						}
						
						// check min/max timestamps
						if ((min_timestamp_mdl == null) || (min_timestamp_mdl > json_data.stage_mdl[count][0])){
							min_timestamp_mdl = json_data.stage_mdl[count][0];
						}
						if ((max_timestamp == null) || (max_timestamp < json_data.stage_mdl[count][0])){
							max_timestamp = json_data.stage_mdl[count][0];
						}
					}
					max_data = max_mdl_val;
					
					// basic check
					if ((max_mdl_idx == myDataMdl.length) && (max_mdl_idx > 0)){
						max_mdl_idx = max_mdl_idx - 1;
					}
					
					// set highlighted model value
					if (max_mdl_idx != null){
						var mark_x = myDataMdl[max_mdl_idx][0];
						var mark_y = myDataMdl[max_mdl_idx][1];
						myDataMdl[max_mdl_idx] = [mark_x, mark_y, 20, modelplus.util.date_to_datetimestr(mark_x)];
					}
					
					// fill observed list object
					for(count = 0; count < json_data.stage_obs.length; count++){
						var mark_x;
						mark_x = new Date(json_data.stage_obs[count][0] * 1000);
						cur_element = [mark_x, json_data.stage_obs[count][1], 
									   20, modelplus.util.date_to_datetimestr(mark_x)];
						myDataObs.push(cur_element);
						
						if ((min_timestamp_obs == null) || (min_timestamp_obs > json_data.stage_obs[count][0])){
							min_timestamp_obs = json_data.stage_obs[count][0];
						}
						if ((max_timestamp == null) || (max_timestamp < json_data.stage_obs[count][0])){
							max_timestamp = json_data.stage_obs[count][0];
						}
						
						// check min and max value
						if ((min_data == null) || (json_data.stage_obs[count][1] < min_data)){
							min_data = json_data.stage_obs[count][1];
						}
						if ((max_data == null) || (json_data.stage_obs[count][1] > max_data)){
							max_data = json_data.stage_obs[count][1];
						}
					}
					
					min_timestamp = Math.max(min_timestamp_mdl, min_timestamp_obs);
					
					// fill thresholds
					if (json_data.stage_threshold_act != null){
						myDataThrAct = [[new Date(min_timestamp * 1000), json_data.stage_threshold_act],
										[new Date(max_timestamp * 1000), json_data.stage_threshold_act]];
						if((max_data == null)||(json_data.stage_threshold_act > max_data)){ 
							max_data = json_data.stage_threshold_act; 
						}
						if ((min_data == null) || (json_data.stage_threshold_act < min_data)){
							min_data = json_data.stage_threshold_act;
						}
					}
					if (json_data.stage_threshold_fld != null){
						myDataThrFld = [[new Date(min_timestamp * 1000), json_data.stage_threshold_fld],
										[new Date(max_timestamp * 1000), json_data.stage_threshold_fld]];
						if((max_data == null)||(json_data.stage_threshold_fld > max_data)){
							max_data = json_data.stage_threshold_fld;
						}
						if ((min_data == null) || (json_data.stage_threshold_fld < min_data)){
							min_data = json_data.stage_threshold_fld;
						}
					}
					if (json_data.stage_threshold_mod != null){
						myDataThrMod = [[new Date(min_timestamp * 1000), json_data.stage_threshold_mod],
										[new Date(max_timestamp * 1000), json_data.stage_threshold_mod]];
						if((max_data == null)||(json_data.stage_threshold_mod > max_data)){
							max_data = json_data.stage_threshold_mod;
						}
						if ((min_data == null) || (json_data.stage_threshold_mod < min_data)){
							min_data = json_data.stage_threshold_mod;
						}
					}
					if (json_data.stage_threshold_maj != null){
						myDataThrMaj = [[new Date(min_timestamp * 1000), json_data.stage_threshold_maj],
										[new Date(max_timestamp * 1000), json_data.stage_threshold_maj]];
						if((max_data == null)||(json_data.stage_threshold_maj > max_data)){
							max_data = json_data.stage_threshold_maj;
						}
						if ((min_data == null) || (json_data.stage_threshold_maj < min_data)){
							min_data = json_data.stage_threshold_maj;
						}
					}
					
					// 
					max_y_label = Math.ceil(max_data + ((max_data - min_data) * 0.1));
					min_y_label = Math.floor(min_data - ((max_data - min_data) * 0.1));
					max_x_label = new Date(max_timestamp);
					min_x_label = new Date(min_timestamp);
					
					// fills title and subtitle
					if((typeof json_data.pois_description != 'undefined')&&(json_data.pois_description != "")){
						title_str = "Station: " + json_data.pois_description;
					} else {
						title_str = "Station: " + "[UNDEFINED]";
					}
					try{
						subtitle_str = "Drainage Area: " + json_data.up_area.toFixed(2) + "km^2";
					}catch(err){
						subtitle_str = "";
					}
			
					// Initialize after dom ready
					var myChart = ec.init(document.getElementById(modelplus.ids.MODAL_HYDROGRAPH_IFISBASED));
					
					var option = {
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
							formatter: function(parms){return("Stage: " + parms.value[1].toFixed(2) + " ft, " + parms.value[3]);}
						},
						legend: {
							data:['Modeled', 'Observed', 'Action', 'Flood', 'Moderate', 'Major'],
							x: 'center',
							y: 'bottom',
							type: 'scroll'
						},
						xAxis : [
							{
								type : 'time',
								name : 'Time',
								min: new Date(min_x_label * 1000),
								max: new Date(max_x_label * 1000),
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
						series : [
							{
								name:"Modeled",
								type:"line",
								showAllSymbol: true,
								symbolSize: function (value){
									return Math.round(value[2]/10) + 2;
								},
								data: myDataMdl,
								itemStyle:{
									normal:{ color: "#3366ff" }
								}
							},
							{
								name:"Observed",
								type:"scatter",
								showAllSymbol: true,
								symbolSize: 2,
								symbolSize: function (value){
									return Math.round(value[2]/12) + 1;
								},
								data: myDataObs,
								itemStyle:{
									normal:{ color: "#000000" }
								}
							},
							{
								name:"Action",
								type:"line",
								symbol: "none",
								symbolSize: 0,
								showAllSymbol: false,
								data: myDataThrAct,
								itemStyle:{
									normal:{
										color: "#ffff55",
										lineStyle:{ type:"dashed" }
									}
								}
							},
							{
								name:"Flood",
								type:"line",
								symbol: "none",
								symbolSize: 0,
								showAllSymbol: false,
								data: myDataThrFld,
								itemStyle:{
									normal:{
										color: "#ff9933",
										lineStyle:{ type:"dashed" }
									}
								}
							},
							{
								name:"Moderate",
								type:"line",
								symbol: "none",
								symbolSize: 0,
								showAllSymbol: false,
								data: myDataThrMod,
								itemStyle:{
									normal:{
										color: "#ff0000",
										lineStyle:{ type:"dashed" }
									}
								}
							},
							{
								name:"Major",
								type:"line",
								symbol: "none",
								symbolSize: 0,
								showAllSymbol: false,
								data: myDataThrMaj,
								itemStyle:{
									normal:{
										color: "#ff77ff",
										lineStyle:{ type:"dashed" }
									}
								}
							}
						]
					};
			
					// Load data into the ECharts instance 
					myChart.setOption(option);
					
					// add header to the hydrograph modal
					modelplus.hydrograph.addHeader({
						position: 'absolute', 
		                div_id: modelplus.ids.MODAL_HYDROGRAPH_IFISBASED,
						raw_data_function: get_model_hidrograph_raw_data,
						raw_data_argument: {
							"runset_id": runset_id,
							"model_id": model_id,
							"reference_id": reference_id,
							"link_id": link_id, 
							"timestamp": timestamp
						}
						
					});
				});
			}
		);
		
		
	}
}
