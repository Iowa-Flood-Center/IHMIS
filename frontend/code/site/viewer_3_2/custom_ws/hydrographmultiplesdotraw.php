<?php
    // TODO - this should be an JSON
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
	$sc_represcomb_id = "hydrographmultiplesdot";
	
	/*********************************************** DEFS **********************************************/
	
	/*********************************************** CALL **********************************************/
	
	// define file paths
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
		echo('{"ERROR":"Missing file \''.$represcomb_file_path.'\'."}');
		exit;
	}
	
	// plot data
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
		
		$links_array[] = (" \"".$cur_common_linkid."\":".$cur_common_file_json["fld_level"]);
	}
	echo(implode(",\n", $links_array));
	echo("\n}");
?>