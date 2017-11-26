<?php
	header("Content-Type: text/plain");
	include_once("ws_metainfo_lib.php");
	
	// 0-) Get arguments
	if (!isset($_GET['runset_id'])){
		echo("Missing 'runset id'.");
		exit();
	} else if (!isset($_GET['show_main'])){
		echo("Missing 'show/main' parameter.");
		exit();
	}
	$scrunset_id = $_GET['runset_id'];
	$show_main = (int)$_GET['show_main'];
	
	// 1-) Define file path
	$runset_file_path = MetaInfoDefs::get_sc_runset_file_path($scrunset_id);
	
	// 2-) Read file
	$json_content = json_decode(file_get_contents($runset_file_path), true);
	
	// 3-) Change content
	if($show_main == 1){
		$json_content['sc_runset']['show_main'] = true;
	} else {
		$json_content['sc_runset']['show_main'] = false;
	}
	
	// 4-) Save file
	$fw = fopen($runset_file_path, 'w+');
	fwrite($fw, json_encode($json_content));
	fclose($fw);
?>