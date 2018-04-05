function custom_display(reference_id_arg){
	"use strict";
	
	var sc_evaluation_id = "nashsutcliffe";
	var second_legend_style_css_noa;
	var model_id, runset_id;
	var all_images_dict = null;
	var used_timestamp;
	var reference_id;
	var legend_url;
	var root_url;
	
	root_url = modelplus.url.base_frontend_webservices;

	// deal with optional argument
	if (typeof reference_id_arg === 'undefined') { reference_id_arg = null; }
	
	// defines statically image URL and div style
	legend_url = root_url + "imgs/legends/nashsutcliffe.png";
	second_legend_style_css_noa = "color:#999999";
	
	// get reference_id from argument or from selected radio button
	model_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();  // TODO - do it correct
	runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
	if(reference_id_arg != null) {
		reference_id = reference_id_arg;
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
				reference_id = "usgsgagesstage";  // TODO - update it
			}
		});
	}
	
	// defines source of information
	var ws_data_url = modelplus.viewer.ws + "custom_ws/nashsutcliffe.php";
	ws_data_url += "%i%sc_model_id="+model_id;
	ws_data_url += "%e%sc_reference_id="+reference_id;
	ws_data_url += "%e%sc_runset_id=" + runset_id;
	
	// load all links available and locations	
	$.when($.getJSON(ws_data_url),
	       modelplus.api.get_gages_by_type([2, 3], true, true))
      .then(function(data_1, data_2){
		display_when_possible(data_1[0], data_2[0]);
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
	 * n: Number. Numeric value
	 * RETURN: String.
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
	function display_when_possible(all_points_classification, gages_location_dict){
		var cur_lat, cur_lng, cur_linkid, cur_linkid_int;
		var cur_latlng, cur_marker, cur_class;
		var cur_class, nbsps, cur_linkid_loc;
		
		if (typeof(GLB_vars.prototype.nashsutcliffe) === 'undefined'){
			GLB_vars.prototype.nashsutcliffe = {};
		}
		
		// for each link_id, plots a stuff with its color
		var cur_message;
		for (var cur_linkid in all_points_classification){
			
			cur_linkid_int = parseInt(cur_linkid);
			if(isNaN(cur_linkid_int)) continue;
			
			// find location
			cur_lat = null;
			cur_lng = null;
			for(var idx=0; idx<gages_location_dict.length; idx++){
				cur_linkid_loc = gages_location_dict[idx]["link_id"];
				if (cur_linkid_loc == cur_linkid){
					cur_lat = parseFloat(gages_location_dict[idx]["lat"]);
					cur_lng = parseFloat(gages_location_dict[idx]["lng"]);
					break;
				}
			}
			if (cur_lat == null) continue;
			
			// case when element is a link_id
			cur_latlng = {lat:cur_lat, lng:cur_lng};
			cur_class = get_color_of_coef(all_points_classification[cur_linkid]["ns_coeff"]);
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
				modelplus.dom.display_message_block(this.message);
			});
			
			// create reference list for icon in global var if necessary
			if(typeof(GLB_visual.prototype.polygons[sc_evaluation_id]) === 'undefined'){
				GLB_visual.prototype.polygons[sc_evaluation_id] = [];
			}
			GLB_visual.prototype.polygons[sc_evaluation_id].push(cur_marker);
		}
		
		// define human readable date and time
		var cur_date = new Date(GLB_vars.prototype.nashsutcliffe.timestamp * 1000);
		var cur_date_hr = twoDigits(cur_date.getMonth()+1)+"/"+twoDigits(cur_date.getDate())+"/"+cur_date.getFullYear();
		var cur_time_hr = twoDigits(cur_date.getHours())+":"+twoDigits(cur_date.getMinutes());
		
		// replace or create top legend if necessary
		if ($("#"+modelplus.ids.LEGEND_TOP_DIV).length > 0){
			$('#'+modelplus.ids.LEGEND_TOP_DIV).remove();
			delete $("#"+modelplus.ids.LEGEND_TOP_DIV);
		}
		var img_html = "<img src='"+legend_url+"' />";
		
		nbsps = "&nbsp;&nbsp;&nbsp;";
		
		var date_html = "";
		var div_html = img_html + date_html;
		
		modelplus.dom.show_legend_top(sc_evaluation_id, div_html);
	}
}
