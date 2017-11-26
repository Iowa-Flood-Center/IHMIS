<?php
	header("Content-Type: text/plain");
	include_once("ws_metainfo_lib.php");

	// basic check
	if (!isset($_GET['runset_id'])){
		echo("Missing 'runset id'.");
		exit();
	}
	
	$runsets_rood_folder_path = MetaInfoDefs::BASE_FOLDER_PATH;
	
	//
	$runset_id = $_GET['runset_id'];
	$root_folder_path = $runsets_rood_folder_path.$runset_id;
	$sh_command = "rm -r ".$root_folder_path;
	
	echo("Executing '".$sh_command."'.<br />");
	echo(system($sh_command));
?>