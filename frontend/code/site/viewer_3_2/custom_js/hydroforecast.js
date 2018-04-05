function custom_display(){
	
	var all_images_dict = null;
	var gages_location_dict = null;
	var ws_all_images_url, ws_gages_location_url, icon_address, single_image_address_frame;
	var url_root_open, url_root_files;
	var sc_evaluation_id = "hydroforecast";
	var sc_model_id, sc_runset_id;
	var possible_select_box_val;
	var reference_id;
	
	// get runset
	sc_runset_id = $('#'+ modelplus.ids.MENU_RUNSET_SBOX).val();
	
	// basic check - runset
	if (sc_runset_id == ""){
		alert("No runset selected.");
		return;
	}
	
	// get model and reference
	possible_select_box_val = $("#np" + sc_evaluation_id + "_sel").val();
	if (possible_select_box_val !== undefined){
		splitted_select_box_val = possible_select_box_val.split("_");
		reference_id = splitted_select_box_val[0];
		sc_model_id = splitted_select_box_val[1];
		
	} else {
		sc_model_id = $('#'+ modelplus.ids.MENU_MODEL_MAIN_SBOX).val();
	
		// search reference
		reference_id = "mock";
		$(".npact").each(function() {
			var cur_radio_id, splitted_radio;
			cur_radio_id = $(this).attr('id');
		
			if(cur_radio_id.indexOf('_') > -1){
				splitted_radio = cur_radio_id.split("_");
				if(splitted_radio[0] == "nphydroforecast"){
					reference_id = splitted_radio[1];
				}
			}
		});
	
		if(sc_model_id == ""){
			alert("No model selected.");
			return;
		}
	}
	
	// build relevant http addressees
	url_root_open = modelplus.url.base_frontend_webservices;
	url_root_files = modelplus.url.base_realtime_folder + sc_runset_id + "/";
	icon_address = url_root_open + "imgs/map_icons/gauge_ifc.png";
	ws_all_images_url = GLB_webservices.prototype.http + "custom_ws/hydroforecast.php%i%sc_model_id="+sc_model_id+"%e%sc_reference_id="+reference_id+"%e%sc_runset_id="+sc_runset_id;
	ws_gages_location_url = GLB_webservices.prototype.http + "ws_gages_location.php";
	single_image_folder_address = url_root_files + "repres_displayed/"+sc_model_id+"/hydroforecast_"+reference_id+"/";
	
	/**
	 *
	 * link_id : 
	 * timestamp : 
	 * RETURN :
	 */
	function build_image_name(link_id, timestamp){
		return(timestamp + "_" + link_id + ".png");
	}
	
	// load one
	// alert("Ajaxing: " + ws_all_images_url);
	$.ajax({
		url: ws_all_images_url
	}).success(function(data){
		all_images_dict = JSON.parse(data);
		display_when_possible();
	});
	
	// load other
	$.ajax({
		url: ws_gages_location_url
	}).success(function(data){
		gages_location_dict = JSON.parse(data);
		display_when_possible();
	});
	
	/**
	 * Function that only works properly when global vars 'all_images_dict' and 'gages_location_dict' are not null
	 * RETURN : None.
	 */
	function display_when_possible(){
		if (all_images_dict == null){
			// alert("Still waiting for imaged JSON.");
		} else if (gages_location_dict == null) {
			// alert("Still waiting for gages JSON.");
		} else {
			// for each gauge, searches if there is an image for it
			json_gage = gages_location_dict["gauge"];
			for(idx=0; idx<json_gage.length; idx++){
				cur_linkid = json_gage[idx]["link_id"];
				if(typeof(all_images_dict[cur_linkid]) !== 'undefined'){
					// define icon, marker and action
					cur_latlng = {lat:parseFloat(json_gage[idx]["lat"]), lng:parseFloat(json_gage[idx]["lng"])};
					cur_icon = new google.maps.MarkerImage(
						icon_address,
						new google.maps.Size(21, 34),
						new google.maps.Point(0,0),
						new google.maps.Point(10, 34));
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
						var img_url = single_image_folder_address + build_image_name(this.id, all_images_dict[this.id]);
						modelplus.dom.display_hidrograph_block(img_url);
					});
					// create reference list for icon in global var if necessary
					if(typeof(GLB_visual.prototype.polygons[sc_evaluation_id]) === 'undefined'){
						GLB_visual.prototype.polygons[sc_evaluation_id] = [];
					}
					GLB_visual.prototype.polygons[sc_evaluation_id].push(cur_marker);
				}
			}
		}
	}
}
