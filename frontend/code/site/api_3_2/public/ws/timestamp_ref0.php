<?php

function process_get_request($app, $req, $res){

  // get params
  $sc_runset_id = $app->util->get_param($req, "sc_runset_id");
  $sc_model_id = $app->util->get_param($req, "sc_model_id");
  $sc_result_id = $app->util->get_param($req, "sc_result_id");

  $all_retrieved = array();
  if(in_array(null, array($sc_runset_id, $sc_model_id, $sc_result_id))){
    return($app->util->show_json($res, $all_retrieved));
  }

  // establishes file path
  $reference_folder_path = $app->fss->runsets_result_folder_path;
  $reference_folder_path .= $sc_runset_id."/txts_timestamp_ref0/";
  $reference_folder_path .= $sc_model_id."/";
  $reference_file_name = $sc_result_id.".txt";
  $reference_file_path = $reference_folder_path.$reference_file_name;

  // read file content if it exists
  if(file_exists($reference_file_path)){
    $raw_content = file_get_contents($reference_file_path);
    if(is_int($raw_content))
      $ref_timestamp = $raw_content;
    else
      $ref_timestamp = intval($raw_content);
    array_push($all_retrieved, $ref_timestamp);
  } else {
    array_push($all_retrieved, -1);
  }
  
  // show
  return($app->util->show_json($res, $all_retrieved));
}
	
?>
