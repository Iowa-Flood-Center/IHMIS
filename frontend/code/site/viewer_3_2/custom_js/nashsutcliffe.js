function custom_display(reference_id_arg){
	
	var sc_evaluation_id = "nashsutcliffe";
	var second_legend_style_css, second_legend_style_css_a;
	var all_points_classification = null;
	var gages_location_dict = null;
	var all_images_dict = null;
	var ws_gages_location_url;
	var used_timestamp;
	var reference_id;
	var legend_url;
	var root_url;
	
	root_url = modelplus.url.base_frontend_webservices;

	// deal with optional argument
	if (typeof reference_id_arg === 'undefined') { reference_id_arg = null; }
	
	// defines statically image URL and div style
	legend_url = root_url + "imgs/legends/nashsutcliffe.png";
	second_legend_style_css = "display:block; left:50%; margin-left:-145px; top:0; z-index:100; position:absolute; border: 1px solid grey; " +
							  "text-align:center; font-family:PFDinTextCompProMedium,Helvetica,Arial,sans-serif; font-size:15px; " +
							  "background-color:#FFFFFF;"
	second_legend_style_css_a = "cursor: pointer;";
	second_legend_style_css_noa = "color:#999999";
	
	// get reference_id from argument or from selected radio button
	model_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();  // TODO - do it correct
	runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
	if(reference_id_arg != null) {
		reference_id = reference_id_arg;
		console.log("Got reference id '" + reference_id + "' from argument.");
	} else {
		reference_id = "mock";
		$(".npact").each(function() {
			var cur_radio_id, splitted_radio;
			cur_radio_id = $(this).attr('id');
			
			if(cur_radio_id.indexOf('_') > -1){
				splitted_radio = cur_radio_id.split("_");
				if(splitted_radio[0] == "npnashsutcliffe"){
					reference_id = splitted_radio[1];
				}
			} else {
				console.log("Getting standard reference_id because cur_radio_id = '" + cur_radio_id + "'.");
				console.log("Inner html: " + $(this).html());
				reference_id = "usgsgagesstage";  // TODO - update it
			}
		});
	}
	
	// defines source of information
	ws_data_url = modelplus.viewer.ws + "custom_ws/nashsutcliffe.php";
	ws_data_url += "%i%sc_model_id="+model_id;
	ws_data_url += "%e%sc_reference_id="+reference_id;
	ws_data_url += "%e%sc_runset_id=" + runset_id;
	ws_gages_location_url = modelplus.viewer.ws + "ws_gages_location.php";
	
	// load data
	// alert("PHP: " + ws_data_url);
	console.log("nashsutcliffe.js: URL 1 - '"+ws_data_url+"'.");
	$.ajax({
		url: ws_data_url
	}).success(function(data){
		all_points_classification = JSON.parse(data);
		display_when_possible();
	});
	
	// load all locations
	console.log("nashsutcliffe.js: URL 2 - '"+ws_gages_location_url+"'.");
	$.ajax({
		url: ws_gages_location_url
	}).success(function(data){
		gages_location_dict = JSON.parse(data);
		display_when_possible();
	});
	
	/**
	 * Just convert NS-Coefficient value into the respective colour.
	 * ns_coef : NS Coefficient. Expected to be less-equal than 1
	 * RETURN : String describing a colour in the format of "#..."
	 */
	function get_color_of_coef(ns_coef){
		if (ns_coef < -2){
			return("#b2182b");
		} else if (ns_coef < -1) {
			return("#ef8a62");
		} else if (ns_coef < -0.1){
			return("#fddbc7");
		} else if (ns_coef < 0.1){
			return("#FFFFFF");
		} else if (ns_coef < 0.4){
			return("#d1e5f0");
		} else if (ns_coef < 0.7){
			return("#67a9cf");
		} else if (ns_coef <= 1.0) {
			return("#2166ac");
		} else {
			return("#000000");
		}
	}
	
	/**
	 * Forces a number to have 2 or more digits
	 *
	 *
	 */
	function n(n){
		return n > 9 ? "" + n: "0" + n;
	}
	
	/**
	 * Converts a timestamp into a pleasant format (MM/DD/YYYY - HH:mm)
	 * a_timestamp:
	 * RETURN: String
	 */
	function format_date(a_timestamp){
		var date_obj, mo, dd, yyyy, hh, mi;
		date_obj = new Date(a_timestamp * 1000);
		mo = n(date_obj.getMonth() + 1);
		dd = n(date_obj.getDate());
		yyyy = date_obj.getFullYear();
		hh = n(date_obj.getHours());
		mi = n(date_obj.getMinutes());
		return(mo + "/" + dd + "/" + yyyy + ", " + hh + ":" + mi);
	}
	
	/**
	 * Function that displays information available at 'GLB_vars.prototype.nashsutcliffe' variable.
	 * RETURN : None.
	 */
	function display_when_possible(){
		var cur_lat, cur_lng, cur_linkid;
		var cur_latlng, cur_marker, cur_class;
		var cur_class;
		var nbsps;
		if (all_points_classification == null){
			// alert("Still waiting for data.");
			return
		} else if (gages_location_dict == null) {
			// alert("Still waiting for data.");
			return
		} else {
			
			if (typeof(GLB_vars.prototype.nashsutcliffe) === 'undefined'){
				GLB_vars.prototype.nashsutcliffe = {};
			}
			
			// for each link_id, plots a stuff with its colour
			// alert(JSON.stringify(all_points_classification));
			
			for (var cur_linkid in all_points_classification){
				
				// alert(cur_linkid + " -> " + all_points_classification[cur_linkid]["ns_coeff"]);
				
				// find location
				json_gage = gages_location_dict["gauge"];
				cur_lat = null;
				cur_lng = null;
				for(idx=0; idx<json_gage.length; idx++){
					cur_linkid_loc = json_gage[idx]["link_id"];
					if (cur_linkid_loc == cur_linkid){
						cur_lat = parseFloat(json_gage[idx]["lat"]);
						cur_lng = parseFloat(json_gage[idx]["lng"]);
						break;
					}
				}
				if (cur_lat == null){
					continue;
				}
				
				// case when element is a link_id
				cur_latlng = {lat:cur_lat, lng:cur_lng};
				cur_class = get_color_of_coef(all_points_classification[cur_linkid]["ns_coeff"]);
				// alert("Creating " + cur_linkid + ": "+ all_points_classification[cur_linkid]["ns_coeff"] +" -> " + cur_class + " at " +cur_lat+ "/" + cur_lng);
				cur_message = "N.S. Coeff: " + all_points_classification[cur_linkid]["ns_coeff"].toFixed(2) + "<br />";
				cur_message += "Number of points: " + all_points_classification[cur_linkid]["num_values"] + "<br />";
				cur_message += "From " + format_date(all_points_classification[cur_linkid]["min_timestamp"]);
				cur_message += " to " + format_date(all_points_classification[cur_linkid]["max_timestamp"]);
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
					id:cur_linkid,
					message:cur_message
				});
				google.maps.event.addListener(cur_marker, "click", function () {
					display_message_block(this.message);
				});
				
				// create reference list for icon in global var if necessary
				if(typeof(GLB_visual.prototype.polygons[sc_evaluation_id]) === 'undefined'){
					GLB_visual.prototype.polygons[sc_evaluation_id] = [];
				}
				GLB_visual.prototype.polygons[sc_evaluation_id].push(cur_marker);
				// alert(cur_linkid + " -> " + all_points_classification[cur_linkid]);
			}
			
			// define human readable date and time
			cur_date = new Date(GLB_vars.prototype.nashsutcliffe.timestamp * 1000),
			cur_date_hr = twoDigits(cur_date.getMonth()+1)+"/"+twoDigits(cur_date.getDate())+"/"+cur_date.getFullYear();
			cur_time_hr = twoDigits(cur_date.getHours())+":"+twoDigits(cur_date.getMinutes());
			
			// replace or create top legend if necessary
			if ($("#"+modelplus.ids.LEGEND_TOP_DIV).length > 0){
				$('#'+modelplus.ids.LEGEND_TOP_DIV).remove();
				delete $("#"+modelplus.ids.LEGEND_TOP_DIV);
			}
			img_html = "<img src='"+legend_url+"' />";
			
			nbsps = "&nbsp;&nbsp;&nbsp;";
			
			// date_html = gobad_html + nbsps + gobah_html + nbsps + "At " + cur_time_hr + ", " + cur_date_hr + "." + nbsps + gofah_html + nbsps + gofad_html;
			date_html = "";
			div_html = img_html + date_html;
			div_obj = $('<div id="'+modelplus.ids.LEGEND_TOP_DIV+'" style="'+second_legend_style_css+'">'+div_html+'</div>');
			div_hid = $('<input type="hidden" id="'+modelplus.ids.LEGEND_TOP_HID+'" value="'+sc_evaluation_id+'" />');
			div_obj.append(div_hid);
			$("body").append(div_obj);
		}
	}
}
