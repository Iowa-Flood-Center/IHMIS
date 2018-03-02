<?php
	header("Content-Type: text/plain");
	
	/*********************************************** ARGS **********************************************/
	
	// read sc_runset_id
	if(isset($_GET['sc_runset_id'])){
		$sc_runset_id = $_GET['sc_runset_id'];
	} else {
		echo('{"ERROR":"Missing parameter \'runset_id\'."}');
		exit();
	}
	
	// read sc_modelcomb_id
	if(isset($_GET['sc_modelcomb_id'])){
		$sc_modelcomb_id = $_GET['sc_modelcomb_id'];
	} else {
		echo('{"ERROR":"Missing parameter \'sc_modelcomb_id\'."}');
		exit();
	}
	
	// read sc_modelcomb_id
	$sc_represcomb_id = "hydrographmultiplespast";
	
	/*********************************************** DEFS **********************************************/
	
	/**
	 *
	 *
	 *
	 * RETURN : 
	 */
	function extract_product_set($represcomb_json, $cur_frame_id){
		return($represcomb_json["sc_represcomb"]["requirements"][$cur_frame_id]["sc_product_set"]);
	}
	
	/**
	 *
	 *
	 *
	 * RETURN : 
	 */
	function display_model_past($scmodel_id, $scproductset_json){
		echo(' "pst":"'.$scmodel_id.'" - ');
		foreach($scproductset_json as $cur_prod_id){
			echo($cur_prod_id."; ");
		}
		echo("\n");
		return;
	}
	
	/**
	 *
	 *
	 *
	 * RETURN : 
	 */
	function display_model_forecast($scmodel_id, $scproductset_json){
		echo(' "frc":"'.$scmodel_id.'"'." - ");
		foreach($scproductset_json as $cur_prod_id){
			echo($cur_prod_id."; ");
		}
		echo("\n");
		return;
	}
	
	/*********************************************** CALL **********************************************/
	
	/* definitions */
	$basic_meta_folder = "/local/iihr/andre/model_3_1/".$sc_runset_id."/metafiles/";
	$basic_data_folder = "/local/iihr/andre/model_3_1/".$sc_runset_id."/repres_displayed/";
	$basic_data_folder .= $sc_modelcomb_id."/".$sc_represcomb_id."/";
	$modelcomb_file_path = $basic_meta_folder."sc_modelcombinations/".$sc_modelcomb_id.".json";
	$represcomb_file_path = $basic_meta_folder."sc_represcomps/".$sc_represcomb_id.".json";
	$common_files_folder_path = $basic_data_folder."common/";
	
	// basic files check
	if (!file_exists($modelcomb_file_path)){
		echo('{"ERROR":"Missing file \''.$modelcomb_file_path.'\'."}');
		exit;
	}
	if (!file_exists($represcomb_file_path)){
		echo('{"ERROR":"Missing file \''.$modelcomb_file_path.'\'."}');
		exit;
	}
	
	//
	// First part
	//
	
	/*
	
	// read files
	$modelcomb_json = json_decode(file_get_contents($modelcomb_file_path), true);
	$represcomb_json = json_decode(file_get_contents($represcomb_file_path), true);
	
	// get the models and frames used
	echo("{\n");
	$all_scmodels_id = array_keys($modelcomb_json['sc_modelcombination']['sc_represcomb_set'][$sc_represcomb_id]);
	foreach($all_scmodels_id as $cur_scmodel_id){
		$cur_frame = $modelcomb_json['sc_modelcombination']['sc_represcomb_set'][$sc_represcomb_id][$cur_scmodel_id];
		switch($cur_frame){
			case "modelpaststg":
				display_model_past($cur_scmodel_id, extract_product_set($represcomb_json, "modelpaststg"));
				break;
			case "modelforestg":
				display_model_forecast($cur_scmodel_id, extract_product_set($represcomb_json, "modelpaststg"));
				break;
			default:
				break;
		}
		
		echo("  ".$cur_scmodel_id." -> ".$cur_frame."\n");
	}
	echo("}");
	
	echo("\n\n");
	
	*/
	
	//
	// Second part
	//
	
	// echo($common_files_folder_path);
	
	echo("{\n");
	$all_common_files = scandir($common_files_folder_path);
	$links_array = array();
	foreach($all_common_files as $cur_common_file_name){
		// ignore back folders references
		if (($cur_common_file_name == ".") || ($cur_common_file_name == "..")){ continue; }
		
		// read file
		$cur_common_file_path = $common_files_folder_path.$cur_common_file_name;
		$cur_common_file_json = json_decode(file_get_contents($cur_common_file_path), true);
		$cur_common_linkid = basename($cur_common_file_name, ".json");
		
		$links_array[] = (" \"".$cur_common_linkid."\":\"".$cur_common_file_path."\"");
	}
	echo(implode(",\n", $links_array));
	echo("\n}");
?>