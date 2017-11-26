<?php
	header("Content-Type: text/plain");
	include_once("ws_metainfo_lib.php");
	
	$runset_id = get_arg("runsetid");
	
	// load basic sc model information
	$all_sc_model_obj = MetaInfoDefs::load_all_sc_models($runset_id);
	
	// basic check
	if($all_sc_model_obj == NULL){
		echo("[]");
		exit();
	}
	
	// list all files and print it
	$all_sc_model_str = array();
	foreach($all_sc_model_obj as $cur_sc_model_obj){
		$cur_sc_model_str = " {\n";
		$cur_sc_model_str .= "  \"id\":\"".$cur_sc_model_obj->get_id()."\", \n";
		$cur_sc_model_str .= "  \"title\":\"".$cur_sc_model_obj->get_name()."\", \n";
		$cur_sc_model_str .= "  \"show_main\":\"".ScObject::boolean_to_string($cur_sc_model_obj->get_showmain())."\"\n";
		$cur_sc_model_str .= "}";
		$all_sc_model_str[] = $cur_sc_model_str;
	}
	echo("[\n".implode($all_sc_model_str, ",")."]");
?>