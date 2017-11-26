<?php
	header("Content-Type: text/plain");
	include_once("ws_metainfo_lib.php");
	
	// get argument
	$runset_id = get_arg("runsetid");
	
	// basic check
	if($runset_id == null){ 
		echo('{"ERROR":"ERROR"}'); 
		exit();
	}
	
	$sc_runset_folder_path = MetaInfoDefs::get_metafiles_folder_path($runset_id);
	
	// echo($sc_runset_folder_path);
	
	// list all sc_models ids
	
	
	echo('{');
	
	echo('}');
?>