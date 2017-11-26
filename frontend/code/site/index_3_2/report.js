
			GLB_url = function(){};
			GLB_url.prototype.report = "http://s-iihr50.iihr.uiowa.edu/andre/model_3_1_reports/report_realtime.json";
			GLB_url.prototype.report_rain = "http://s-iihr50.iihr.uiowa.edu/andre/model_3_1_reports/report_rain_realtime.json";
			GLB_url.prototype.base_folder = "imgs/report/";
			
			GLB_msg = function(){};
			GLB_msg.prototype.s_hpc_54 = "";
			GLB_msg.prototype.s_web_54 = "";
			GLB_msg.prototype.s_54_auto = "";
			GLB_msg.prototype.s_54_50 = "";
			
			/**
			 *
			 * the_timestamp :
			 * RETURN :
			 */
			function timestampToIowa(the_timestamp){
				
				// basic check
				if (the_timestamp == -1){
					return("Undefined");
				} else {
					return(new Date(the_timestamp * 1000).toLocaleString('en-US'));
				}
			}
			
			/**
			 *
			 * the_timestamp :
			 * RETURN :
			 */
			function timestampToUTC(the_timestamp){
				var the_date, the_offset, timestamp_ms;
				
				// basic check
				if (the_timestamp == -1){
					return("Undefined");
				}
				
				// 
				timestamp_ms = the_timestamp * 1000;
				the_date = new Date(timestamp_ms).toLocaleString('en-US');
				the_offset = new Date(timestamp_ms).getTimezoneOffset() * 60000;
				the_date = new Date(timestamp_ms + the_offset).toLocaleString('en-US');
				return(the_date);
			}
			
			/**
			 *
			 * date_obj :
			 * RETURN :
			 */
			function formatDateString(date_obj){
				return(date_obj.split(',')[0]);
			}
			
			/**
			 *
			 * data_code :
			 * RETURN :
			 */
			function show_message(data_code){
				$("#the_info").html(GLB_msg.prototype[data_code]);
			}
			
			/**
			 *
			 * json_obj :
			 * min_timestamp :
			 * max_timestamp :
			 * RETURN :
			 */
			function define_hpc_arrow_color(json_obj, min_timestamp, max_timestamp){
				var flag_ok, any_data, cur_dict, cur_i, cur_mdl;
				
				// start variables
				flag_ok = true;
				any_data = false;
				cur_dict = {
					updated:[],
					delayed:[],
					nodata:[]
				};
				
				// evaluate all models
				for(cur_i = 0; cur_i < json_obj.reports_models.length; cur_i++){
					cur_mdl = json_obj.reports_models[cur_i];
						
					// ignore "no values"
					if(cur_mdl.last_input_data_for == -1){
						cur_dict.nodata.push(cur_mdl.sc_model_desc);
						continue;
					}
						
					// check if value is updated or not
					any_data = true;
					if ((cur_mdl.last_input_data_for < max_timestamp) && 
						(cur_mdl.last_input_data_for > min_timestamp)){
						flag_ok = flag_ok;
						cur_dict.updated.push(cur_mdl.sc_model_desc);
					} else {
						flag_ok = false;
						cur_dict.delayed.push(cur_mdl.sc_model_desc);
					}
				}
				
				// build shown data
				GLB_msg.prototype.s_hpc_54 = built_str_model_dict(cur_dict);
				if((flag_ok) && (any_data)){
					return(GLB_url.prototype.base_folder + "arrow_dr_blue.png");
				} else if (!any_data){
					return(GLB_url.prototype.base_folder + "arrow_dr_grey.png");
				} else {
					return(GLB_url.prototype.base_folder + "arrow_dr_red.png");
				}
			}
			
			/**
			 *
			 * json_obj :
			 * min_timestamp :
			 * max_timestamp :
			 * RETURN :
			 */
			function define_web_arrow_color(json_obj, min_timestamp, max_timestamp){
				var cur_r, cur_rp, cur_reference, cur_reference_prods, cur_reference_prod, all_references_id;
				var has_any, any_delay;
				
				// read data, defining the color and the info data
				has_any = false;
				any_delay = false;
				all_references_id = Object.keys(json_obj.reports_references);
				for(cur_r = 0; cur_r < all_references_id.length; cur_r++){
					cur_reference_id = all_references_id[cur_r];
					cur_reference = json_obj.reports_references[cur_reference_id];
					GLB_msg.prototype.s_web_54 += " - " + cur_reference.sc_reference_id + ": ";
					
					cur_reference_prods = cur_reference.sc_reference_products;
					for(cur_rp = 0; cur_rp < cur_reference_prods.length; cur_rp++){
						cur_reference_prod = cur_reference_prods[cur_rp];
						// alert(cur_reference_prod + " as " + cur_rp + " in " + cur_reference_prods.length);
						
						if ((cur_reference_prod.last_reference_for < max_timestamp) && 
							(cur_reference_prod.last_reference_at > min_timestamp)){
							GLB_msg.prototype.s_web_54 += '<span class="on_time" >ON TIME</span>';
							has_any = true;
						} else {
							if ((cur_reference_prod.last_reference_for != -1)&&((typeof cur_reference_prod.last_reference_for !== 'undefined'))) {
								GLB_msg.prototype.s_web_54 += '<span class="delayed" >DELAYED</span>';
								has_any = true;
								any_delay = true;
							} else {
								GLB_msg.prototype.s_web_54 += '<span class="no_data" >NO DATA</span>';
							}
						}
						GLB_msg.prototype.s_web_54 += '<br />';
					
						GLB_msg.prototype.s_web_54 += '<span class="time">';
						GLB_msg.prototype.s_web_54 += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
						GLB_msg.prototype.s_web_54 += 'At : ' + timestampToIowa(cur_reference_prod.last_reference_at);
						GLB_msg.prototype.s_web_54 += '(<a href="#" title="'+timestampToUTC(cur_reference_prod.last_reference_at)+'">UTC</a>)';
						GLB_msg.prototype.s_web_54 += '<br />';
						GLB_msg.prototype.s_web_54 += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
						GLB_msg.prototype.s_web_54 += 'For: ' + timestampToIowa(cur_reference_prod.last_reference_for);
						GLB_msg.prototype.s_web_54 += '(<a href="#" title="'+timestampToUTC(cur_reference_prod.last_reference_for)+'">UTC</a>)';
						GLB_msg.prototype.s_web_54 += '<br />';
						GLB_msg.prototype.s_web_54 += '</span>';
					}
				}
				
				if ((has_any) && (!any_delay)){
					return(GLB_url.prototype.base_folder + "arrow_dl_blue.png");
				} else if ((has_any) && (any_delay)) {
					return(GLB_url.prototype.base_folder + "arrow_dl_red.png");
				} else {
					return(GLB_url.prototype.base_folder + "arrow_dl_grey.png");
				}
			}
			
			/**
			 *
			 * json_obj :
			 * min_timestamp :
			 * max_timestamp :
			 * RETURN :
			 */
			function define_auto_arrow_color(json_obj, min_timestamp, max_timestamp){
				var cur_m, cur_mp, cur_model, cur_prod_id;
				var color_code;
				
				GLB_msg.prototype.s_54_auto = "";
				color_code = 1;  // 1:blue, 2:yellow, 3:red
				
				// read data, defining the color and the info data
				for(cur_m = 0; cur_m < json_obj.reports_models.length; cur_m++){

					cur_model = json_obj.reports_models[cur_m];
					GLB_msg.prototype.s_54_auto += " - " + cur_model.sc_model_id + ":<br />";
					for(cur_mp = 0; cur_mp < cur_model.sc_products.length; cur_mp++){
						cur_prod = cur_model.sc_products[cur_mp];
						cur_prod_id = cur_prod.sc_product_id;
						
						if(cur_prod.last_input_data_for == -1){
							GLB_msg.prototype.s_54_auto += " --- " + cur_prod_id + ": No data.<br />"; 
							continue;
						}
						
						GLB_msg.prototype.s_54_auto += " --- " + cur_prod_id + ": ";
						if ((cur_prod.last_input_data_for < max_timestamp) && 
							(cur_prod.last_input_data_at > min_timestamp)){
							color_code = color_code;
							GLB_msg.prototype.s_54_auto += '<span class="on_time" >ON TIME</span>'; 
						} else {
							color_code = 3;
							GLB_msg.prototype.s_54_auto += '<span class="delayed" >DELAYED</span>'; 
						}
						GLB_msg.prototype.s_54_auto += "<br />";
						
						GLB_msg.prototype.s_54_auto += '<span class="time">';
						GLB_msg.prototype.s_54_auto += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
						GLB_msg.prototype.s_54_auto += 'At : ' + timestampToIowa(cur_prod.last_input_data_at);
						GLB_msg.prototype.s_54_auto += '(<a href="#" title="'+timestampToUTC(cur_prod.last_input_data_at)+'">UTC</a>)';
						GLB_msg.prototype.s_54_auto += '<br />';
						GLB_msg.prototype.s_54_auto += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
						GLB_msg.prototype.s_54_auto += 'For: ' + timestampToIowa(cur_prod.last_input_data_for);
						GLB_msg.prototype.s_54_auto += '(<a href="#" title="'+timestampToUTC(cur_prod.last_input_data_for)+'">UTC</a>)';
						GLB_msg.prototype.s_54_auto += '<br />';
						GLB_msg.prototype.s_54_auto += '</span>';
					}
				}
				
				// 
				if(color_code == 3){
					return(GLB_url.prototype.base_folder + "arrow_cc_red.png");
				} else if(color_code == 2){
					return("");
				} else {
					return(GLB_url.prototype.base_folder + "arrow_cc_blue.png");
				}
			}
			
			/**
			 *
			 * json_obj : 
			 * min_timestamp : 
			 * max_timestamp : 
			 * RETURN :
			 */
			function define_representation_arrow_color(json_obj, min_timestamp, max_timestamp){
				var has_any, any_delay;
			
				GLB_msg.prototype.s_54_50 = "";
				color_code = 1;  // 1:blue, 2:yellow, 3:red, 4:no data
				
				// read data, defining the color and the info data
				has_any = false;
				any_delay = false;
				for(cur_m = 0; cur_m < json_obj.reports_models.length; cur_m++){
					cur_model = json_obj.reports_models[cur_m];
					cur_model_id = cur_model.sc_model_id;
					GLB_msg.prototype.s_54_50 += " - " + cur_model_id + ":<br />";
					for(cur_mp = 0; cur_mp < cur_model.sc_representations.length; cur_mp++){
						cur_repr = cur_model.sc_representations[cur_mp];
						cur_repr_id = cur_repr.sc_representation_id;
						
						if(cur_repr.last_input_data_for == -1){
							GLB_msg.prototype.s_54_50 += " -" + cur_repr_id + ": No data.<br />"; 
							continue;
						}
						
						// determine color
						GLB_msg.prototype.s_54_50 += " --- " + cur_repr_id + ": ";
						if ((cur_repr.last_representation_for < max_timestamp) && 
							(cur_repr.last_representation_at > min_timestamp)){
							color_code = color_code;
							GLB_msg.prototype.s_54_50 += '<span class="on_time" >ON TIME</span>';
							has_any = true;
						} else {
							if ((cur_repr.last_representation_for != -1)&&((typeof cur_repr.last_representation_for !== 'undefined'))) {
								color_code = 3;
								GLB_msg.prototype.s_54_50 += '<span class="delayed" >DELAYED</span>';
								has_any = true;
								any_delay = true;
							} else {
								GLB_msg.prototype.s_54_50 += '<span class="no_data" >NO DATA</span>';
							}
						}
						GLB_msg.prototype.s_54_50 += "<br />";
						if (cur_repr.last_representation_for != -1){
							GLB_msg.prototype.s_54_50 += '<span class="time">';
							GLB_msg.prototype.s_54_50 += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
							GLB_msg.prototype.s_54_50 += 'At : ' + timestampToIowa(cur_repr.last_representation_at);
							GLB_msg.prototype.s_54_50 += '(<a href="#" title="'+timestampToUTC(cur_repr.last_representation_at)+'">UTC</a>)<br />';
							GLB_msg.prototype.s_54_50 += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;';
							GLB_msg.prototype.s_54_50 += 'For: ' + timestampToIowa(cur_repr.last_representation_for);
							GLB_msg.prototype.s_54_50 += '(<a href="#" title="'+timestampToUTC(cur_repr.last_representation_for)+'">UTC</a>)<br />';
							GLB_msg.prototype.s_54_50 += '</span>';
						}
					}
				}
				
				if ((has_any) && (!any_delay)){
					return(GLB_url.prototype.base_folder + "arrow_l_blue.png");
				} else if ((has_any) && (any_delay)) {
					return(GLB_url.prototype.base_folder + "arrow_l_red.png");
				} else {
					return(GLB_url.prototype.base_folder + "arrow_l_grey.png");
				}
			}
			
			/**
			 *
			 * model_dictionary :
			 * RETURN :
			 */
			function built_str_model_dict(model_dictionary){
				var return_str, cur_i;
				
				return_str = "";
				
				return_str += '<span class="on_time" >ON TIME</span>:<br />';
				for(cur_i = 0; cur_i < model_dictionary.updated.length; cur_i++){
					return_str += "&nbsp;&nbsp;" + model_dictionary.updated[cur_i] + "<br />";
				}
				
				return_str += '<span class="delayed" >DELAYED</span>:<br />';
				for(cur_i = 0; cur_i < model_dictionary.delayed.length; cur_i++){
					return_str += "&nbsp;&nbsp;" + model_dictionary.delayed[cur_i] + "<br />";
				}
				
				return_str += '<span class="no_data" >NO DATA</span>:<br />';
				for(cur_i = 0; cur_i < model_dictionary.nodata.length; cur_i++){
					return_str += "&nbsp;&nbsp;" + model_dictionary.nodata[cur_i] + "<br />";
				}
				
				return(return_str);
			}
			
			/**
			 *
			 * RETURN :
			 */
			function replace_diagram(){
				var s_hpc_54_arrow, s_web_54_arrow, s_54_auto, s_54_50;
				var the_html, base_folder;
				
				base_folder = "imgs/report/";
				
				$.getJSON(GLB_url.prototype.report, function( data ) {
					var root_obj, cur_i, cur_mdl, flag_ok;
					var min_timestamp, max_timestamp;
					var cur_dict;
					
					root_obj = data.runset_report;
					
					// set up last window timestamps
					max_timestamp = root_obj.report_timestamp_creation;
					min_timestamp = max_timestamp - (60 * 60);
					
					// define arrows colours
					s_hpc_54_arrow = define_hpc_arrow_color(root_obj, min_timestamp, max_timestamp);
					s_web_54_arrow = define_web_arrow_color(root_obj, min_timestamp, max_timestamp);
					s_54_auto = define_auto_arrow_color(root_obj, min_timestamp, max_timestamp);
					s_54_50 = define_representation_arrow_color(root_obj, min_timestamp, max_timestamp);
				
					// show image
					the_html = '';
					the_html += '<div style="display:block; position:relative; width:556px; heigth:307px">';
					the_html += '<img src="'+base_folder+'system_noarrows.png" style="position:static" />';
					the_html += '<img src="'+s_54_auto+'" style="position:absolute; left:380px; top:230px" onclick="show_message(\'s_54_auto\')" />';
					the_html += '<img src="'+s_hpc_54_arrow+'" style="position:absolute; left:220px; top:90px" onclick="show_message(\'s_hpc_54\')" />';
					the_html += '<img src="'+s_web_54_arrow+'" style="position:absolute; left:380px; top:90px" onclick="show_message(\'s_web_54\')" />';
					the_html += '<img src="'+s_54_50+'" style="position:absolute; left:120px; top:200px" onclick="show_message(\'s_54_50\')" />';
					the_html += '</div>';
				
					$("#the_content").html(the_html);
				});
			}
			
			/**
			 *
			 * RETURN :
			 */
			function replace_log(){
				var json_url, json_content;
					var cur_i, cur_mdl, div_content;
					
					json_url = GLB_url.prototype.report;
					
					$.getJSON(json_url, function( data ) {
						var inner_html, root_obj;
						var cur_mdl, cur_prod;
						
						// alert("MyJSON: " + data);
						root_obj = data.runset_report;
						inner_html = "Runset: " + root_obj.runset_id + "<br />";
						inner_html += "Report time (Iowa): " + timestampToIowa(data.runset_report.report_timestamp_creation) + "<br />";
						inner_html += "Report time (UTC): " + timestampToUTC(data.runset_report.report_timestamp_creation) + "<br />";
						
						inner_html += "Models: <br />";
						
						for(cur_i = 0; cur_i < root_obj.reports_models.length; cur_i++){
							cur_mdl = root_obj.reports_models[cur_i];
							inner_html += "-" + cur_mdl.sc_model_desc + "(" + cur_mdl.sc_model_id + ")<br />";
							inner_html += "-- New data at: " + timestampToIowa(cur_mdl.last_input_data_at) + "("+cur_mdl.last_input_data_at+")<br />";
							inner_html += "-- New data for: " + timestampToIowa(cur_mdl.last_input_data_for) + "<br />";
							inner_html += "-- Products: " + "<br />";
							for(cur_j = 0; cur_j < cur_mdl.sc_products.length; cur_j++){
								cur_prod = cur_mdl.sc_products[cur_j];
								inner_html += "--- " + cur_prod.sc_product_title + "(" + cur_prod.sc_product_id + ")" + "<br />";
								inner_html += "---- Newest data at: " + timestampToIowa(cur_prod.last_input_data_at) + " (UTC: " + timestampToUTC(cur_prod.last_input_data_at) + ").<br />";
								inner_html += "---- Newest data for: " + timestampToIowa(cur_prod.last_input_data_for) + " (UTC: " + timestampToUTC(cur_prod.last_input_data_for) + ").<br />";
							}
						}
						
						$("#the_content").html(inner_html);
						$("#the_info").html(inner_html);
					});
					return;
			}
			
			/**
			 *
			 * RETURN :
			 */
			function replace_log_rain(){
				var json_content;
				
				$.getJSON(GLB_url.prototype.report_rain, function(data) {
					var root_obj, inner_html, all_daily_timestamps, all_model_ids;
					var cur_model_obj, cur_register, cur_timestamp, cur_percent, cur_label;
					var cur_i, cur_m;
					
					root_obj = data.runset_rain_report;
					inner_html = "Runset: " + root_obj.runset_id + "<br />";
					inner_html += "Report time (Iowa): " + timestampToIowa(root_obj.report_timestamp_creation) + "<br />";
					inner_html += "Report time (UTC): " + timestampToUTC(root_obj.report_timestamp_creation) + "<br />";
					inner_html += "----------------<br />";
					
					all_model_ids = Object.keys(root_obj.reports_models_rain);
					inner_html += "<strong>Daily rainfall accumulation:</strong><br />";
					for(cur_m = 0; cur_m < all_model_ids.length; cur_m++){					
						cur_model_id = all_model_ids[cur_m];
						cur_model_obj = root_obj.reports_models_rain[cur_model_id];
						inner_html += "Model: " + cur_model_obj.model_title + " (" + cur_model_obj.model_id + ")<br />";
						all_daily_timestamps = Object.keys(cur_model_obj.daily_rain_report);
						all_daily_timestamps.sort();
						all_daily_timestamps.reverse();
						for(cur_i = 0; cur_i < all_daily_timestamps.length; cur_i++){
							cur_timestamp = all_daily_timestamps[cur_i];
							cur_register = cur_model_obj.daily_rain_report[cur_timestamp];
							cur_percent = cur_register.rain / (cur_register.rain + cur_register.no_rain);
							
							if (cur_percent == 0){
								cur_label = "<span style='color:#ff0000;'>None</span>";
							} else if (cur_percent < 25) {
								cur_label = "<span style='color:#8888ff;'>Low</span>";
							} else if (cur_percent < 50) {
								cur_label = "<span style='color:#5555cc;'>Average</span>";
							} else {
								cur_label = "<span style='color:#000099;'>High</span>";
							}
							
							inner_html += "&nbsp;At " + formatDateString(timestampToIowa(cur_timestamp)) + ": ";
							// inner_html += " (UTC: " + formatDateString(timestampToUTC(cur_timestamp)) + ")<br />";
							inner_html += cur_label + " (" + cur_percent + "% : ";
							inner_html += cur_register.rain + " of " + cur_register.no_rain + " hillslopes)<br />";
							
						}
					}
					
					$("#the_content").html(inner_html);
				})
			}
			
			function onload_function(){
				$('.tab a').click(function(){
					$('.tab a').parent().css("background-color", "#efefef");
					$(this).parent().css("background-color", "#f5f5f5");
				});
			}
