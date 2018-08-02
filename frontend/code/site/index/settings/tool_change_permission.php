<?php
	header("Content-Type: text/plain");
	include_once("../../viewer_3_1/ws_metainfo_lib.php");
	
	// 0-) Get arguments
	if (!isset($_GET['runset_id'])){
		echo("Missing 'runset id'.");
		exit();
	}
	$scrunset_id = $_GET['runset_id'];
	
	// 1-) Define file path
	$runset_file_path = MetaInfoDefs::get_runset_folder_path($scrunset_id);
	
	// 1.5-) Basic check
	if(!file_exists($runset_file_path)){
		echo("Folder '".$runset_file_path."' not found.");
		exit();
	}
	
	// 2-) Set up recursive functions
	system("chmod -R ugo+rw ".$runset_file_path);
	
	// 3-) Bye bye
	echo("Changed permissions recursively on folder '".$runset_file_path."'.")
?>