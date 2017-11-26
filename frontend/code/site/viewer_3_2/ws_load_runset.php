<?php 
	header("Content-Type: text/plain");
	include_once("ws_metainfo_lib.php");
	
	# get arguments
	$runset_id = get_arg("runsetid");
	
	# open json
	echo("{\n");
	
	# load basic sc runset information
	$runset_file_path = MetaInfoDefs::get_sc_runset_file_path($runset_id);
	if(file_exists($runset_file_path)){
		$runset_file_content = file_get_contents($runset_file_path);
		$runset_json_content = json_decode($runset_file_content, true);
		echo("  \"sc_runset\":\n");
		echo("    ".json_encode($runset_json_content["sc_runset"])."\n");
	} else {
		echo("  \"sc_runset\":\"File '".$runset_file_path."' not found.\"\n");
	}
	echo("  ,\n");
	
	# load basic sc model information
	$all_sc_model_str = array();
	$all_sc_model_obj = MetaInfoDefs::load_all_sc_models($runset_id);
	foreach($all_sc_model_obj as $cur_sc_model_obj){
		
		$cur_sc_model_str =  "    {\n";
		$cur_sc_model_str .= "      \"id\":\"".$cur_sc_model_obj->get_id()."\",\n";
		$cur_sc_model_str .= "      \"title\":\"".$cur_sc_model_obj->get_name()."\",\n";
		$cur_sc_model_str .= "      \"title_acronym\":\"".$cur_sc_model_obj->get_title_acronym()."\",\n";
		$cur_sc_model_str .= "      \"show_main\":\"".ScObject::boolean_to_string($cur_sc_model_obj->get_showmain())."\"\n";
		$cur_sc_model_str .= "    }";
		
		// $all_sc_model_str[] = "{\"id\":\"".$cur_sc_model_obj->get_id()."\", \"title\":\"".$cur_sc_model_obj->get_name()."\", \"title_acronym\":\"".$cur_sc_model_obj->get_title_acronym()."\"}";
		$all_sc_model_str[] = $cur_sc_model_str;
	}

	# print basic sc model information
	echo("  \"sc_model\":[\n");
	echo(implode($all_sc_model_str, ",\n")."\n");
	echo("  ], \n");
	
	# load basic sc model combination information
	$all_sc_modelcomb_str = array();
	$all_sc_modelcomb_obj = MetaInfoDefs::load_all_sc_modelcombinations($runset_id);
	foreach($all_sc_modelcomb_obj as $cur_sc_modelcomb_obj){
		$all_sc_modelcomb_str[] = "{\"id\":\"".$cur_sc_modelcomb_obj->get_id()."\", \"title\":\"".$cur_sc_modelcomb_obj->get_name()."\"}";
	}
	
	# print basic sc model combination information
	echo("  \"sc_model_combination\":[\n");
	echo("     ".implode($all_sc_modelcomb_str, ",\n     ")."\n");
	echo("  ], \n");
	
	# load basic sc reference information
	$all_sc_reference_str = array();
	$all_sc_reference_obj = MetaInfoDefs::load_all_sc_references($runset_id);
	foreach($all_sc_reference_obj as $cur_sc_reference_obj){
		$cur_sc_reference_str = array();
		$cur_sc_reference_str[] = "\"id\":\"".$cur_sc_reference_obj->get_id()."\"";
		$cur_sc_reference_str[] = "\"title\":\"".$cur_sc_reference_obj->get_title()."\"";
		if($cur_sc_reference_obj->get_title_acronym() != null){
			$cur_sc_reference_str[] = "\"title_acronym\":\"".$cur_sc_reference_obj->get_title_acronym()."\"";
		}
		$all_sc_reference_str[] = "{".implode(",\n      ", $cur_sc_reference_str)."}";
	}

	# print basic sc reference information
	echo("  \"sc_reference\":[\n");
	echo("     ".implode($all_sc_reference_str, ",\n     ")."\n");
	echo("  ], \n");
	
	# load basic representations information
	$all_sc_representation_str = array();
	$all_sc_representation_obj = MetaInfoDefs::load_all_sc_representations($runset_id);
	foreach($all_sc_representation_obj as $cur_sc_representation_obj){
		$cur_sc_representation_str = array();
		$cur_sc_representation_str[] = "\"id\":\"".$cur_sc_representation_obj->get_id()."\"";
		$cur_sc_representation_str[] = "\"description\":\"".$cur_sc_representation_obj->get_description()."\"";
		$cur_sc_representation_str[] = "\"representation\":\"".$cur_sc_representation_obj->get_representation()."\"";
		if (!is_null($cur_sc_representation_obj->get_callSelect())){
			$cur_sc_representation_str[] = "\"call_select\":\"".$cur_sc_representation_obj->get_callSelect()."\"";
		}
		if (!is_null($cur_sc_representation_obj->get_callRadio())){
			$cur_sc_representation_str[] = "\"call_radio\":\"".$cur_sc_representation_obj->get_callRadio()."\"";
		}
		if (!is_null($cur_sc_representation_obj->get_legend())){
			$cur_sc_representation_str[] = "\"legend\":\"".$cur_sc_representation_obj->get_legend()."\"";
		}
		if (!is_null($cur_sc_representation_obj->get_legend_sing())){
			$cur_sc_representation_str[] = "\"legend_sing\":\"".$cur_sc_representation_obj->get_legend_sing()."\"";
		}
		if (!is_null($cur_sc_representation_obj->get_legend_comp())){
			$cur_sc_representation_str[] = "\"legend_comp\":\"".$cur_sc_representation_obj->get_legend_comp()."\"";
		}
		if (!is_null($cur_sc_representation_obj->get_time_interval())){
			$cur_sc_representation_str[] = "\"time_interval\":\"".$cur_sc_representation_obj->get_time_interval()."\"";
		}
		if (!is_null($cur_sc_representation_obj->get_calendar_type())){
			$cur_sc_representation_str[] = "\"calendar_type\":\"".$cur_sc_representation_obj->get_calendar_type()."\"";
		}
		$all_sc_representation_str[] = "{".implode(",\n      ", $cur_sc_representation_str)."}\n     ";
	}
	
	# print basic sc representation information
	echo("  \"sc_representation\":[\n");
	echo("     ".implode($all_sc_representation_str, ",\n     ")."\n");
	echo("  ], \n");
	
	# TODO - load evaluation
	$all_sc_evaluation_str = array();
	$all_sc_evaluation_obj = MetaInfoDefs::load_all_sc_evaluations($runset_id);
	foreach($all_sc_evaluation_obj as $cur_sc_evaluation_obj){
		$cur_sc_evaluation_str = array();
		$cur_sc_evaluation_str[] = "\"id\":\"".$cur_sc_evaluation_obj->get_id()."\"";
		$cur_sc_evaluation_str[] = "\"description\":\"".$cur_sc_evaluation_obj->get_description()."\"";
		$all_sc_evaluation_str[] = "{".implode(",\n      ", $cur_sc_evaluation_str)."}\n     ";
	}
	
	# print basic sc evaluation information
	echo("  \"sc_evaluation\":[\n");
	echo("     ".implode($all_sc_evaluation_str, ",\n     "));
	echo("], \n");
	
	# load matrix
	$comp_mtx = MetaInfoDefs::load_comparison_matrix($runset_id);
	if (sizeof($comp_mtx) > 0){
		foreach($comp_mtx as $cur_comp_key => $cur_comp_set){
			$all_comp_str[] = "{\"id\":\"".$cur_comp_key."\", \"params\":[\"".implode($cur_comp_set, "\", \"")."\"]}";
		}
	} else {
		$all_comp_str[] = "";
	}
	
	# print matrix
	echo("  \"comp_mtx\":[\n");
	echo("     ".implode($all_comp_str, ",\n     ")."\n");
	echo("  ], \n");
	
	# TODO - load evaluation matrix
	
	# load menu
	
	$menu_content = MetaInfoDefs::load_menu_raw_str($runset_id);
	echo("  ".substr(trim($menu_content), 1, sizeof(trim($menu_content))-2));
	
	# close json
	echo("}\n\n");
?>