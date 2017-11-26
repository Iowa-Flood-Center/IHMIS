<?php 
	header("Content-Type: text/plain");
	include_once("ws_metainfo_lib.php");
	
	# open json
	echo("{\n");
	
	# load basic sc model information
	$all_sc_model_str = array();
	$all_sc_model_obj = MetaInfoDefs::load_all_sc_models();
	foreach($all_sc_model_obj as $cur_sc_model_obj){
		$all_sc_model_str[] = "{\"id\":\"".$cur_sc_model_obj->get_id()."\", \"title\":\"".$cur_sc_model_obj->get_name()."\"}";
	}

	# print basic sc model information
	echo("  \"sc_model\":[\n");
	echo("     ".implode($all_sc_model_str, ",\n     ")."\n");
	echo("  ], \n");
	
	# load basic sc reference information
	$all_sc_reference_str = array();
	$all_sc_reference_obj = MetaInfoDefs::load_all_sc_references();
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
	$all_sc_representation_obj = MetaInfoDefs::load_all_sc_representations();
	foreach($all_sc_representation_obj as $cur_sc_representation_obj){
		$cur_sc_representation_str = array();
		$cur_sc_representation_str[] = "\"id\":\"".$cur_sc_representation_obj->get_id()."\"";
		$cur_sc_representation_str[] = "\"description\":\"".$cur_sc_representation_obj->get_description()."\"";
		$cur_sc_representation_str[] = "\"representation\":\"".$cur_sc_representation_obj->get_representation()."\"";
		if (!is_null($cur_sc_representation_obj->get_callSelect())){
			$cur_sc_representation_str[] = "\"call_select\":\"".$cur_sc_representation_obj->get_callSelect()."\"";
		}
		if (!is_null($cur_sc_representation_obj->get_callSelect())){
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
		$all_sc_representation_str[] = "{".implode(",\n      ", $cur_sc_representation_str)."}\n     ";
	}
	
	# print basic sc representation information
	echo("  \"sc_representation\":[\n");
	echo("     ".implode($all_sc_representation_str, ",\n     ")."\n");
	echo("  ], \n");
	
	# TODO - load evaluation
	$all_sc_evaluation_str = array();
	$all_sc_evaluation_obj = MetaInfoDefs::load_all_sc_evaluations();
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
	$comp_mtx = MetaInfoDefs::load_comparison_matrix();
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
	
	$menu_content = MetaInfoDefs::load_menu_raw_str();
	echo("  ".substr(trim($menu_content), 1, sizeof(trim($menu_content))-2));
	
	# close json
	echo("}\n\n");
?>