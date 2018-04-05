<?php
  header('Content-Type: application/json');
  
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
  $basic_data_folder = "/local/iihr/andre/model_3_1/".$sc_runset_id."/repres_displayed/";
  $basic_data_folder .= $sc_modelcomb_id."/".$sc_represcomb_id."/";
  
  // check if folder exists
  if (!file_exists($basic_data_folder)){
    $out_json["ERROR"] = "Missing file '".$basic_data_folder."'.";
	echo(json_encode($out_json));
    exit;
  }
  
  // list files
  $all_files = scandir($basic_data_folder);
  // $out_json["DEBUG"] = "Read ".count($all_files)." files from '".$basic_data_folder."'.";

  // read each file
  foreach($all_files as $cur_file_name){
	if(!strpos($cur_file_name, '_')) continue;
	
	// read file
    $cur_file_path = $basic_data_folder.$cur_file_name;
	$cur_file_content = json_decode(file_get_contents($cur_file_path));
	
	// define link-id / key
	$cur_link_id = intval(explode(".", explode("_", $cur_file_name)[1])[0]);
	
	$out_json[$cur_link_id] = $cur_file_content;
  }

  echo(json_encode($out_json));
?>
