<?php
	header("Content-Type: text/plain");

	// read sc_model_id
	if(isset($_GET['sc_model_id'])){
		$sc_model_id = $_GET['sc_model_id'];
	} else {
		exit();
	}
	
	// read sc_reference_id
	if(isset($_GET['sc_reference_id'])){
		$sc_reference_id = $_GET['sc_reference_id'];
	} else {
		exit();
	}
	
	// read sc_runset_id
	if(isset($_GET['sc_runset_id'])){
		$sc_runset_id = $_GET['sc_runset_id'];
	} else {
		exit();
	}

	/* definitions */
	$imgs_folder = "/local/iihr/andre/model_3_1/".$sc_runset_id."/repres_displayed/".$sc_model_id."/hydroforecast_".$sc_reference_id."/";
	$imgs_format = ".png";

	/*********************************************** DEFS **********************************************/
	
	/**
	 * 
	 * $sc_model_id : 
	 * $cur_timestamp : 
	 * RETURN : Associative list in the form of [link_id]->timestamp
	 */
	function list_available_hydroforecasts_linkid($sc_model_id, $cur_timestamp){
		// list all files in directory
		$return_files = array();
		$all_file_names = scandir($GLOBALS['imgs_folder']);
		foreach($all_file_names as $cur_file_name){
			if (!endsWith($cur_file_name, $GLOBALS['imgs_format'])){ continue; }
			$cur_basename = basename($cur_file_name, $GLOBALS['imgs_format']);
			$splited_filename = explode("_", $cur_basename);
			if(($cur_timestamp == null) || ($cur_timestamp == $splited_filename[0])){
				//$return_files[$splited_filename[1]] = $splited_filename[0];
				$return_files[] = '"'.$splited_filename[1].'":'.$splited_filename[0];
			}
		}
		return($return_files);
	}
	
	/**
	 * Auxiliar function for string processing
	 * $haystack :
	 * $needle :
	 * RETURN : Boolean
	 */
	function endsWith($haystack, $needle){
		return $needle === '' || substr_compare($haystack, $needle, -strlen($needle)) === 0;
	}

	/*********************************************** CALL **********************************************/
	
	$all_available_hydroforecasts = list_available_hydroforecasts_linkid("fc254ifc01norain", null);
	echo("{\n  ");
	echo(implode(",\n  ", $all_available_hydroforecasts));
	echo("\n}");
?>