<?php
	include_once("common/class_FoldersDefs.php");
	header('Content-type: application/json');

	// basic check - arguments
	if ((!isset($_GET['sc_model_id'])) || (!isset($_GET['sc_representation_id']))){
		echo("-1");
		exit();
	}
	
	// read arguments
	$sc_runset_id = $_GET['sc_runset_id'];
	$sc_model_id = $_GET['sc_model_id'];
	$sc_representation_id = $_GET['sc_representation_id'];
	
	// establishes file paths for timestamp 0 and timestamp init
	$general_file_name = $sc_representation_id.".txt";
	
	$ref0_folder_path = FoldersDefs::RUNSET_ROOT_FOLDERPATH.$sc_runset_id."/txts_timestamp_ref0/".$sc_model_id."/";
	$ref0_file_path = $ref0_folder_path.$general_file_name;
	
	$init_folder_path = FoldersDefs::RUNSET_ROOT_FOLDERPATH.$sc_runset_id."/txts_timestamp_init/".$sc_model_id."/";
	$init_file_path = $init_folder_path.$general_file_name;
	
	// create output object
	$output_array = array();
	
	// read files content if they exist
	if(file_exists($ref0_folder_path)){
		$output_array["ref0_timestamp"] = trim(file_get_contents($ref0_file_path));
	} else {
		$output_array["ref0_timestamp"] = null;}
		
	if(file_exists($init_folder_path)){
		$output_array["init_timestamp"] = trim(file_get_contents($init_file_path));
	} else {
		$output_array["init_timestamp"] = null;}
	
	echo(json_encode($output_array));
?>