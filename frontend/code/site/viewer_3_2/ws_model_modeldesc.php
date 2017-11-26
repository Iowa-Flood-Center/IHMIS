<?php
	
	/************************************* ARGS *************************************/
	
	if (!isset($_GET["model_id"])){
		echo('{"error":"No model id provided."}');
		return;
	} else if (!isset($_GET["runset_id"])) {
		echo('{"error":"No runset id provided."}');
		return;
	} else {
		$model_id = $_GET["model_id"];
		$runset_id = $_GET["runset_id"];
	}
	
	/************************************* DEFS *************************************/
	
	$model_descs_folder_path = "/local/iihr/andre/model_3_1/".$runset_id."/metafiles/sc_models/";
	
	/************************************* CALL *************************************/
	
	// check if description file exists
	$desc_file_path = $model_descs_folder_path.$model_id.".json";
	$desc_file_data = null;
	
	if (file_exists($desc_file_path)){
		// read and print file content if it exists
		$desc_file_data = file_get_contents($desc_file_path);
		
	} else {
		// generate an error message
		$desc_file_data = '{"error":"Description not found for model '.$model_id.'"}';
	}
	
	echo($desc_file_data);
?>