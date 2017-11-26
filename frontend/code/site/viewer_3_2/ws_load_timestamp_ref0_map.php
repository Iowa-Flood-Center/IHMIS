<?php
	// basic check - arguments
	if ((!isset($_GET['sc_model_id'])) || (!isset($_GET['sc_representation_id']))){
		echo("-1");
		exit();
	}
	
	// read arguments
	$sc_runset_id = $_GET['sc_runset_id'];
	$sc_model_id = $_GET['sc_model_id'];
	$sc_representation_id = $_GET['sc_representation_id'];
	
	// establishes file path
	$reference_folder_path = "/local/iihr/andre/model_3_1/".$sc_runset_id."/txts_timestamp_ref0/".$sc_model_id."/";
	$reference_file_name = $sc_representation_id.".txt";
	$reference_file_path = $reference_folder_path.$reference_file_name;
	
	// read file content if it exists
	if(file_exists($reference_file_path)){
		echo(file_get_contents($reference_file_path));
	} else {
		echo($reference_file_path);
	}
?>