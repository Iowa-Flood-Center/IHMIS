function custom_display(opt_timestamp){
	
	var sc_evaluation_id = "disclausgssih";
	var all_images_dict = null;
	var ws_gages_location_url;
	var reference_id, runset_id;
	var second_legend_style_css, second_legend_style_css_a;
	var used_timestamp;
	var legend_url;
	var root_url;

	root_url = modelplus.url.base_frontend_webservices;
	
	// deal with optional argument
	if (typeof opt_timestamp === 'undefined') {
		used_timestamp = null;
	} else {
		used_timestamp = opt_timestamp;
	}
	runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
	
	// defines statically image URL and div style
	legend_url = root_url + "imgs/legends/disclausgssih_ref.png";
	second_legend_style_css = "display:block; left:50%; margin-left:-145px; top:0; z-index:100; position:absolute; border: 1px solid grey; " +
							  "text-align:center; font-family:PFDinTextCompProMedium,Helvetica,Arial,sans-serif; font-size:15px; " +
							  "background-color:#FFFFFF;"
	second_legend_style_css_a = "cursor: pointer;";
	second_legend_style_css_noa = "color:#999999";
	
	// get reference_id from selected radio button  -  TODO - transfer to a common place
	reference_id = "mock";
	$(".npact").each(function() {
		var cur_radio_id, splitted_radio;
		cur_radio_id = $(this).attr('id');
		
		if(cur_radio_id.indexOf('_') > -1){
			splitted_radio = cur_radio_id.split("_");
			if(splitted_radio[0] == "nphydroforecast"){
				reference_id = splitted_radio[1];
			}
		} else {
			reference_id = "usgsgagesdischclass";
		}
	});
	
	// defines source of information
	ws_data_url = modelplus.viewer.ws + "custom_ws/disclausgssih.php";
	ws_data_url += "%i%sc_reference_id="+reference_id;
	if(used_timestamp != null){
		ws_data_url += "%e%ref_timestamp=" + used_timestamp;
	}
	ws_data_url += "%e%sc_runset_id=" + runset_id;
	
	// load data
	$.ajax({
		url: ws_data_url
	}).success(function(data){
		all_points_classification = JSON.parse(data);
		display_when_possible();
	});
	
	/**
	 * Just convert USGS's numerical value for the respective colour.
	 * usgs_class_number :
	 * RETURN : String describing a colour in the format of "#..."
	 */
	function get_color_of_usgs_class(usgs_class_number){
		switch(usgs_class_number){
			case 0:
				return("#FFFFFF");
				break;
			case 1:
			case 2:
			case 3:
				return("#FFFED5");
				break;
			case 4:
				return("#AFDFC1");
				break;
			case 5:
				return("#4DC2CF");
				break;
			case 6:
				return("#3692c5");
				break;
			case 7:
			case 8:
				return("#3149e5");
				break;
			default:
				return("#FF0000");
				break;
		}
	}
	
	/**
	 * Function that displays information available at '' variable.
	 * RETURN : None.
	 */
	function display_when_possible(){
		var cur_lat, cur_lng, cur_linkid;
		var cur_latlng, cur_marker, cur_class;
		var cur_class;
		var nbsps;
		if (all_points_classification == null){
			// alert("Still waiting for data.");
		} else {
			// for each link_id, plots a stuff with its colour
			for(cur_linkid in all_points_classification){
				// case when element is the timestamp
				if(cur_linkid == 'timestamp'){
					GLB_vars.prototype.disclausgssih = all_points_classification[cur_linkid];
					continue;
				} else if (cur_linkid == 'timestamp_prev_d'){
					GLB_vars.prototype.disclausgssih_prev_d = all_points_classification[cur_linkid];
					continue;
				} else if (cur_linkid == 'timestamp_prev_h'){
					GLB_vars.prototype.disclausgssih_prev_h = all_points_classification[cur_linkid];
					continue;
				} else if (cur_linkid == 'timestamp_next_h'){
					GLB_vars.prototype.disclausgssih_next_h = all_points_classification[cur_linkid];
					continue;
				} else if (cur_linkid == 'timestamp_next_d'){
					GLB_vars.prototype.disclausgssih_next_d = all_points_classification[cur_linkid];
					continue;
				}
				
				// case when element is a link_id
				if (all_points_classification[cur_linkid]['classif'] == 0){
					continue;
				}
				cur_lat = all_points_classification[cur_linkid]['lat'];
				cur_lng = all_points_classification[cur_linkid]['lng'];
				cur_latlng = {lat:parseFloat(cur_lat), lng:parseFloat(cur_lng)};
				cur_class = get_color_of_usgs_class(all_points_classification[cur_linkid]['classif']);
				cur_marker = new google.maps.Marker({
					position:cur_latlng,
					map:map,
					icon:{path: google.maps.SymbolPath.CIRCLE,
						fillColor: cur_class,
						strokeColor: "#777777",
						strokeWeight: 1,
						fillOpacity: 1,
						scale: 5
					},
					zIndex: 10,
					draggable: false,
					id:cur_linkid
				});
				google.maps.event.addListener(cur_marker, "click", function () {
					// alert("Link id: " + this.id);
					/*
					var img_url = single_image_folder_address + build_image_name(this.id, all_images_dict[this.id]);
					modelplus.dom.display_hidrograph_block(img_url);
					*/
				});
				
				// create reference list for icon in global var if necessary
				if(typeof(GLB_visual.prototype.polygons[sc_evaluation_id]) === 'undefined'){
					GLB_visual.prototype.polygons[sc_evaluation_id] = [];
				}
				GLB_visual.prototype.polygons[sc_evaluation_id].push(cur_marker);
				// alert(cur_linkid + " -> " + all_points_classification[cur_linkid]);
			}
			
			// define human readable date and time
			cur_date = new Date(GLB_vars.prototype.disclausgssih * 1000),
			cur_date_hr = twoDigits(cur_date.getMonth()+1)+"/"+twoDigits(cur_date.getDate())+"/"+cur_date.getFullYear();
			cur_time_hr = twoDigits(cur_date.getHours())+":"+twoDigits(cur_date.getMinutes());
			
			// replace or create top legend if necessary
			if ($("#"+modelplus.ids.LEGEND_TOP_DIV).length > 0){
				$('#'+modelplus.ids.LEGEND_TOP_DIV).remove();
				delete $("#"+modelplus.ids.LEGEND_TOP_DIV);
			}
			img_html = "<img src='"+legend_url+"' />";
			
			nbsps = "&nbsp;&nbsp;&nbsp;";
			gobad_html = define_gobad_html(second_legend_style_css_a, second_legend_style_css_noa);  // go-back-arrow
			gobah_html = define_gobah_html(second_legend_style_css_a, second_legend_style_css_noa);  // go-back-arrow
			gofah_html = define_gofah_html(second_legend_style_css_a, second_legend_style_css_noa);  // go-forward-arrow-hourly
			gofad_html = define_gofad_html(second_legend_style_css_a, second_legend_style_css_noa);  // go-forward-arrow-daily
			date_html = gobad_html + nbsps + gobah_html + nbsps + "At " + cur_time_hr + ", " + cur_date_hr + "." + nbsps + gofah_html + nbsps + gofad_html;
			div_html = img_html + "<br />" + date_html;
			div_obj = $('<div id="'+modelplus.ids.LEGEND_TOP_DIV+'" style="'+second_legend_style_css+'">'+div_html+'</div>');
			$("body").append(div_obj);
		}
	}
}

/**
 *
 * style_css_a :
 * style_css_noa :
 * RETURN : String.
 */
function define_gobad_html(style_css_a, style_css_noa){
	var return_html;
	
	return_html = "";
	if (GLB_vars.prototype.disclausgssih_prev_d == -1){
		// case 'no next hour available'
		return_html = "<span style='"+style_css_noa+"' >&lt;&lt;</span>";
	} else {
		return_html = "<a onclick='gobad_click();' style='"+style_css_a+"' >&lt;&lt;</a>";
	}
	return (return_html);
}

/**
 *
 * style_css_a :
 * style_css_noa :
 * RETURN : String.
 */
function define_gobah_html(style_css_a, style_css_noa){
	var return_html;
	
	return_html = "";
	if (GLB_vars.prototype.disclausgssih_prev_h == -1){
		// case 'no next hour available'
		return_html = "<span style='"+style_css_noa+"' >&lt;</span>";
	} else {
		return_html = "<a onclick='gobah_click();' style='"+style_css_a+"' >&lt;</a>";
	}
	return (return_html);
}

/**
 *
 * RETURN : String.
 */
function define_gofah_html(style_css_a, style_css_noa){
	var return_html;
	
	return_html = "";
	if (GLB_vars.prototype.disclausgssih_next_h == -1){
		// case 'no next hour available'
		return_html = "<span style='"+style_css_noa+"' >&gt;</span>";
	} else {
		return_html = "<a onclick='gofah_click();' style='"+style_css_a+"' >&gt;</a>";
	}
	return (return_html);
}

/**
 *
 * RETURN : String.
 */
function define_gofad_html(style_css_a, style_css_noa){
	var return_html;
	
	return_html = "";
	if (GLB_vars.prototype.disclausgssih_next_d == -1){
		// case 'no next hour available'
		return_html = "<span style='"+style_css_noa+"' >&gt;&gt;</span>";
	} else {
		return_html = "<a onclick='gofad_click();' style='"+style_css_a+"' >&gt;&gt;</a>";
	}
	return (return_html);
}

/**
 * Function called by 'GO Back Arrow Daily' click.
 * RETURN : None. Changes performed in interface.
 */
function gobad_click(){
	GLB_vars.prototype.disclausgssih -= (24 * 3600);  // return in time
	goa_click();
}

/**
 * Function called by 'GO Back Arrow Hourly' click.
 * RETURN : None. Changes performed in interface.
 */
function gobah_click(){
	GLB_vars.prototype.disclausgssih -= 3600;  // return in time
	goa_click();
}

/**
 * Function called by 'GO Forward Arrow Hourly' click.
 * RETURN : None. Changes performed in interface.
 */
function gofah_click(){
	GLB_vars.prototype.disclausgssih += 3600;  // go ahead in time one hour
	goa_click();
}

/**
 * Function called by 'GO Forward Arrow Daily' click.
 * RETURN : None. Changes performed in interface.
 */
function gofad_click(){
	GLB_vars.prototype.disclausgssih += (24*3600);  // go ahead in time one day
	goa_click();
}

/**
 * Function called by a 'GO Arrow' click.
 * RETURN : None. Changes performed in interface.
 */
function goa_click(){
	var display_address;
	
	display_address = modelplus.url.custom_display_js_folder + "disclausgssih.js";
	
	delete custom_display;
	hide_custom_display("disclausgssih");
	modelplus.scripts.load(display_address, function(){
		if(typeof custom_display !== 'undefined'){
			custom_display(GLB_vars.prototype.disclausgssih);
		} else {
			// alert("'custom_display' undefined for 'disclausgssih'");
		}
	});
}
