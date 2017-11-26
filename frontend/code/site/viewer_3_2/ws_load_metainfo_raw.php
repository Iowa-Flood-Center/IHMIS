<?php
	header("Content-Type: text/plain");
	include_once("ws_metainfo_lib.php");
	
	$object_id = get_arg("obj_id");
	
	if($object_id == null){ echo('{"ERROR":"ERROR"}'); exit();}

	$sc_model_folder_path = MetaInfoDefs::BASE_FOLDER_PATH.MetaInfoDefs::SCMODEL_FOLDER;
	$sc_model_file_name = $object_id.".json";
	$sc_model_file_path = $sc_model_folder_path."/".$sc_model_file_name;

	// load representations
	ScModel::useConstructTotal();
	$cur_sc_model = new ScModel($sc_model_file_path);
	$cur_representation_set = $cur_sc_model->get_representation_set();
	
	// load comparisons
	$sc_comp_matrix = new ScComparisonMatrix();
	$cur_comparison_set = $sc_comp_matrix->get_comparison_set($object_id);
	
	// load evaluations
	$sc_eval_matrix = new ScEvaluationMatrix();
	$cur_evaluation_set = $sc_eval_matrix->get_evaluation_set($object_id);

	echo("{\n");
	
	echo(" \"id\":\"".$object_id."\",\n");
	
	echo(" \"sc_representation\": ");
	if (sizeof($cur_representation_set)> 0){
		echo("[\"".implode($cur_representation_set, "\",\"")."\"],\n");
	} else {
		echo("[],\n");
	}
	
	echo(" \"sc_comparison\": ");
	if (sizeof($cur_comparison_set)> 0){
		echo("[\"".implode($cur_comparison_set, "\",\"")."\"],\n");
	} else {
		echo("[],\n");
	}
	
	echo(" \"sc_evaluation\": ");
	if (sizeof($cur_evaluation_set)> 0){
		echo("[\"".implode($cur_evaluation_set, "\",\"")."\"]\n");
	} else {
		echo("[]\n");
	}
	
	echo("}");	
?>