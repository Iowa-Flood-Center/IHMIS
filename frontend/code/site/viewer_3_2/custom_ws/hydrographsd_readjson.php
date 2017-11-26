<?php
	header("Content-Type: text/plain");
	
	// TODO - move this variable out of here
	$base_runset_folder_path = "/local/iihr/andre/model_3_1/";

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
	
	// read sc_reference_id
	if(isset($_GET['sc_reference_id'])){
		$sc_reference_id = $_GET['sc_reference_id'];
	} else {
		exit();
	}
	
	// read link_id
	if(isset($_GET['link_id'])){
		$link_id = $_GET['link_id'];
	} else {
		exit();
	}
	
	// read timestamp
	if(isset($_GET['timestamp'])){
		$timestamp = $_GET['timestamp'];
	} else {
		exit();
	}
	
	/* definitions */
	$sc_eval_id = "hydrographsd";

	# get file path
	$json_folder = $base_runset_folder_path.$sc_runset_id."/repres_displayed/".$sc_model_id."/".$sc_eval_id."_".$sc_reference_id."/";
	$json_filename = $timestamp."_".$link_id.".json";
	$json_filepath = $json_folder.$json_filename;
	
	# read file and display it
	readfile($json_filepath);
?>