<?php
	header("Content-Type: text/plain");
	include_once("ws_metainfo_lib.php");
	
	// get arguments
	$runset_id = get_arg("runsetid");
	$model_id = get_arg("modelid");
	
	// basic check
	if($runset_id == null){ echo('{"ERROR":"ERROR", "REASON":"Missing runset id"}'); exit();}
	if($model_id == null){ echo('{"ERROR":"ERROR", "REASON":"Missing model id"}'); exit();}
	
	// get file path of model and model combination
	$sc_file_name = $model_id.".json";
	$sc_model_folder_path = MetaInfoDefs::get_metafiles_folder_path($runset_id).MetaInfoDefs::SCMODEL_FOLDER;
	$sc_model_file_path = $sc_model_folder_path."/".$sc_file_name;
	$sc_modelcomb_folder_path = MetaInfoDefs::get_metafiles_folder_path($runset_id).MetaInfoDefs::SCMODELCOMB_FOLDER;
	$sc_modelcomb_file_path = $sc_modelcomb_folder_path."/".$sc_file_name;
	
	// check if the file exists (selected element is a model)
	if (file_exists($sc_model_file_path)){
	
		// load representations
		ScModel::useConstructTotal();
		$cur_sc_model = new ScModel($sc_model_file_path);
		$cur_representation_set = $cur_sc_model->get_representation_set();
		
		// load comparisons
		$sc_comp_matrix = new ScComparisonMatrix();
		$cur_comparison_set = $sc_comp_matrix->get_comparison_set($runset_id, $model_id);
		
		// load evaluations
		$sc_eval_matrix = new ScEvaluationMatrix($runset_id);
		$cur_evaluation_set = $sc_eval_matrix->get_evaluation_set($runset_id, $model_id);

		// write output
		echo("{\n");
		echo(" \"id\":\"".$model_id."\",\n");
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
		
	} else if (file_exists($sc_modelcomb_file_path)) {
		
		// load representations
		ScModelCombination::useConstructTotal();
		$cur_sc_modelcomb = new ScModelCombination($sc_modelcomb_file_path);
		$cur_repres_set = $cur_sc_modelcomb->get_repres_set();
		$cur_represcomb_set = $cur_sc_modelcomb->get_represcomb_set();
		
		// load evaluations matrix
		$sc_eval_matrix = new ScEvaluationMatrix($runset_id);
				
		// load evaluations related to the model comb.
		$sc_evaluations_id = array();
		if ((!is_null($cur_represcomb_set)) && (sizeof($cur_represcomb_set) > 0)){
			foreach($cur_represcomb_set as $cur_represcomb){
				foreach(array_keys($cur_represcomb) as $cur_scmodel_id){
					$saw_scmodels[] = $cur_scmodel_id;
					$cur_evaluation_set = $sc_eval_matrix->get_evaluation_set($runset_id, $cur_scmodel_id);
					foreach($cur_evaluation_set as $cur_evaluation_id_set){
						$sc_evaluations_id[] = $cur_evaluation_id_set."_".$cur_scmodel_id;
		}	}	}	}
		
		// write output
		echo("{\n");
		echo(" \"id\":\"".$cur_sc_modelcomb->get_id()."\",\n");
		if (!is_null($cur_repres_set)){
			echo(" \"sc_representation\":".json_encode($cur_repres_set).",\n");
		}
		if (!is_null($cur_represcomb_set)){
			echo(" \"sc_represcomb\":".json_encode($cur_represcomb_set).",\n");
		}
		echo(" \"sc_evaluation_mdl\":".json_encode($sc_evaluations_id)."\n");
		echo("}");
		
	} else {
		echo('{');
		echo(' "ERROR":"ERROR",\n');
		echo(' "REASON":"Files \''.$sc_model_file_path.'\' and \''.$sc_modelcomb_file_path.'\' do not exist."'); 
		echo('}');
		exit();
	}
?>