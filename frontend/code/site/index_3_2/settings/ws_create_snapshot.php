<?php
  error_reporting(E_ALL);
  ini_set('display_errors', '1');
  
  header("Content-Type: text/plain");
  include_once("../../viewer_3_1/ws_metainfo_lib.php");
  
  // get arguments
  if (!isset($_GET['runsetid']))
    $scrunset_id = null;
  else
    $scrunset_id = $_GET['runsetid'];
  if (!isset($_GET['runsetname']))
    $scrunset_name = null;
  else
    $scrunset_name = $_GET['runsetname'];
  if (!isset($_GET['runsetabout']))
    $scrunset_about = null;
  else
    $scrunset_about = $_GET['runsetabout'];
  if (!isset($_GET['runsetstart']))
    $scrunset_start = null;
  else
    $scrunset_start = $_GET['runsetstart'];
  if (!isset($_GET['runsetend']))
    $scrunset_end = null;
  else
    $scrunset_end = $_GET['runsetend'];

  // 1-) Define file path
  $source_folder_path = MetaInfoDefs::get_runset_folder_path("realtime");
  $destin_folder_path = MetaInfoDefs::get_runset_folder_path($scrunset_id);

  echo("hws.");
  exit(1);

	

	
	
	// echo('{"Saving as":"'.$runset_name.'"}');
	
	
	
	// 2-) Check if dest folder already exists
	if (file_exists($destin_folder_path)){
		echo('{"error":"Runset id '.$scrunset_id.' already exists."}');
		return;
	}
	
	// 3-) copy entire folder
	exec("cp -r ".$source_folder_path." ".$destin_folder_path);
	exec("chmod ugo+wrx ".$destin_folder_path);
	// echo('{"Debug":"Copy \''.$source_folder_path.'\' to \''.$destin_folder_path.'\'."}');
	
	// 4-) change runset file content
	$destin_runset_file_path = MetaInfoDefs::get_sc_runset_file_path($scrunset_id);
	$destin_runset_file_path = str_replace($scrunset_id.".json", "Runset.json", $destin_runset_file_path);
	$json_content = json_decode(file_get_contents($destin_runset_file_path));
	$json_content->sc_runset->id = $scrunset_id;
	$json_content->sc_runset->title = $scrunset_name;
	$json_content->sc_runset->description = $scrunset_about;
	$json_content->sc_runset->timestamp_ini = $scrunset_start;
	$json_content->sc_runset->timestamp_end = $scrunset_end;
	file_put_contents($destin_runset_file_path, json_encode($json_content));
	
	// 5-) why not debug?
	echo('{"Saved":"'.$destin_runset_file_path.'"}');
?>