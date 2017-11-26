<?php
	header("Content-Type: text/plain");
	
	/*********************************************** ARGS **********************************************/
	
	// read sc_runset_id
	if(isset($_GET['sc_runset_id'])){
		$sc_runset_id = $_GET['sc_runset_id'];
	} else {
		exit();
	}
	
	// read sc_model_id
	if(isset($_GET['sc_model_id'])){
		$sc_model_id = $_GET['sc_model_id'];
	} else {
		exit();
	}
	
	// read link_id
	if(isset($_GET['link_id'])){
		$link_id = $_GET['link_id'];
	} else {
		exit();
	}
	
	$sc_represcomb_id = "hydrographmultiplesdot";
	
	/*********************************************** DEFS **********************************************/
	
	/**
	 *
	 * $filename -
	 * $link_id -
	 * RETURN - 
	 */
	function check_file_is_linkid($filename, $link_id){
		// ignore back folders references
		if (($filename == ".") || ($filename == "..")){ return(false); }
		
		$aaa = explode("_",basename($filename, ".json"));
		if ($aaa[1] == $link_id){
			return(true);
		} else {
			//echo($aaa[1]."!=".$link_id.". ");
			return(false);
		}
	}
	
	/**
	 *
	 * $link_id - 
	 * RETURN - 
	 */
	function get_desc_area($link_id){
		$loc_file = "/local/iihr/demir/test1/modelplus_3_1_git/frontend/viewer_3_1/ancillary_files/gauges_location_20170328.csv";
		$f_handle = fopen($loc_file, "r");
		$read_header = false;
		if($f_handle){
			$return_array = null;
			$cur_line = true;
			while($cur_line !== false) {
				$cur_line = fgets($f_handle);
				if($read_header == false){
					$read_header = true;
					continue;
				}
				$cur_line_split = explode(",", $cur_line);
				if(sizeof($cur_line_split) <= 1){ break;}
				if ($cur_line_split[1] == $link_id){
					$return_array["desc"] = trim($cur_line_split[5]);
					$return_array["area"] = trim($cur_line_split[6]);
					break;
				}
			}

			fclose($f_handle);
			return($return_array);
		} else {
			return(null);
		}
	}
	
	/*********************************************** CALL **********************************************/
	
	$root_folder_path = "/local/iihr/andre/model_3_1/".$sc_runset_id."/repres_displayed/".$sc_model_id."/".$sc_represcomb_id."/";
	$common_folder_path = $root_folder_path."common/";
	$modelforestg_folder_path = $root_folder_path."modelforestg/";
	$modelpaststg_folder_path = $root_folder_path."modelpaststg/";
	$modelforestgalert_folder_path = $root_folder_path."modelforestgalert/";
	
	// start variables
	$modelpaststg_dict = array();
	$modelforestg_dict = array();
	$modelforestgalert_dict = array();
	$output_dict = array();
	
	// find respective forecast files
	$all_scmodel_folders = scandir($modelforestg_folder_path);
	# debug check
	# if(sizeof($all_scmodel_folders) > 0){ echo("Got ".sizeof($all_scmodel_folders)." files at '".$modelforestg_folder_path."'. "); }
	foreach($all_scmodel_folders as $cur_scmodel_folder){
		// ignore back folders references
		if (($cur_scmodel_folder == ".") || ($cur_scmodel_folder == "..")){ continue; }
		
		$cur_subfolder_path = $modelforestg_folder_path.$cur_scmodel_folder."/";
		$all_inner_files = scandir($cur_subfolder_path);
		# debug check
		# if(sizeof($all_inner_files) > 0){ echo("Got ".sizeof($all_inner_files)." files at '".$cur_subfolder_path."'. "); }
		foreach($all_inner_files as $cur_inner_file){
			if (check_file_is_linkid($cur_inner_file, $link_id)){
				$cur_inner_file_path = $cur_subfolder_path.$cur_inner_file;
				$modelforestg_dict[$cur_scmodel_folder] = json_decode(file_get_contents($cur_inner_file_path), true);
			}
		}
	}
	
	// find respective forecast alert files
	if (file_exists($modelforestgalert_folder_path)){
		$all_scmodel_folders = scandir($modelforestgalert_folder_path);
		foreach($all_scmodel_folders as $cur_scmodel_folder){
			// ignore back folders references
			if (($cur_scmodel_folder == ".") || ($cur_scmodel_folder == "..")){ continue; }
			
			$cur_subfolder_path = $modelforestgalert_folder_path.$cur_scmodel_folder."/";
			$all_inner_files = scandir($cur_subfolder_path);
			foreach($all_inner_files as $cur_inner_file){
				if (check_file_is_linkid($cur_inner_file, $link_id)){
					$cur_inner_file_path = $cur_subfolder_path.$cur_inner_file;
					$modelforestgalert_dict[$cur_scmodel_folder] = json_decode(file_get_contents($cur_inner_file_path), true);
				}
			}
		}
	}
	
	// find respective past files
	$all_scmodel_folders = scandir($modelpaststg_folder_path);
	foreach($all_scmodel_folders as $cur_scmodel_folder){
		// ignore back folders references
		if (($cur_scmodel_folder == ".") || ($cur_scmodel_folder == "..")){ continue; }
		
		$cur_subfolder_path = $modelpaststg_folder_path.$cur_scmodel_folder."/";
		$all_inner_files = scandir($cur_subfolder_path);
		foreach($all_inner_files as $cur_inner_file){
			if (check_file_is_linkid($cur_inner_file, $link_id)){
				$cur_inner_file_path = $cur_subfolder_path.$cur_inner_file;
				$modelpaststg_dict[$cur_scmodel_folder] = json_decode(file_get_contents($cur_inner_file_path), true);
			}
		}
	}
	
	// load common information
	$common_file_path = $common_folder_path.$link_id.".json";
	$common_dict = json_decode(file_get_contents($common_file_path), true);
	$desc_area = get_desc_area($link_id);
	
	// build output object and print it
	$output_dict["forealert"] = $modelforestgalert_dict;
	$output_dict["fore"] = $modelforestg_dict;
	$output_dict["past"] = $modelpaststg_dict;
	$output_dict["common"] = $common_dict;
	if($desc_area != null){
		$output_dict["common"]["desc"] = $desc_area["desc"];
		$output_dict["common"]["area"] = $desc_area["area"];
	} else {
		$output_dict["common"]["desc"] = "Undefined";
		$output_dict["common"]["area"] = "Undefined";
	}
	echo(json_encode($output_dict));
?>