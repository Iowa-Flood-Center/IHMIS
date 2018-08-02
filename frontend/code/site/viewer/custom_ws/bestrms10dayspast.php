<?php
  require_once("libs/debug.php");
  require_once("libs/headers.php");
  
  /*********************************************** ARGS **********************************************/
	
  // read sc_reference_id
  if(isset($_GET['sc_modelcomb_id'])){
    $sc_modelcomb_id = $_GET['sc_modelcomb_id'];
  } else {
    exit();
  }
	
  // read sc_runset_id
  if(isset($_GET['sc_runset_id'])){
    $sc_runset_id = $_GET['sc_runset_id'];
  } else {
    exit();
  }
  
  // read sc_modelcomb_id
  $sc_represcomb_id = "bestrms10dayspast";

  /*********************************************** DEFS **********************************************/
  
  /*********************************************** CALL **********************************************/
  
  $out_json = array();
  
  /* definitions */
  $basic_data_folder_url = "repres_displayed/";
  $basic_data_folder_url .= $sc_modelcomb_id."/".$sc_represcomb_id."/";
  
  // check if folder exists
  if (!DataAccess::check_datafile_exists($basic_data_folder_url, 
                                         $sc_runset_id)){
    $out_json["ERROR"] = "Missing folder '".$basic_data_folder_url."'.";
	echo(json_encode($out_json));
    exit;
  }
  
  // list files
  $all_files = DataAccess::list_datafolder_content($basic_data_folder_url,
                                                   $sc_runset_id,
                                                   ".json");

  // read each file
  foreach($all_files as $cur_file_name){
	if(!strpos($cur_file_name, '_')) continue;
	
	// read file
    $cur_file_path = $basic_data_folder_url.$cur_file_name;
    $cur_file_content = DataAccess::get_datafile_content($cur_file_path,
                                                         $sc_runset_id);
    $cur_file_content = json_decode($cur_file_content);
	
	// define link-id / key
	$cur_link_id = intval(explode(".", explode("_", $cur_file_name)[1])[0]);
	
	$out_json[$cur_link_id] = $cur_file_content;
  }

  echo(json_encode($out_json));
?>
