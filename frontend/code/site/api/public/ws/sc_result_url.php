<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

function process_get_request($app, $req, $res){

  $sc_runset_id = $app->util->get_param($req, "sc_runset_id");
  $sc_model_id = $app->util->get_param($req, "sc_model_id");
  $sc_result_id = $app->util->get_param($req, "sc_result_id");
  $time = $app->util->get_param($req, "time");

  $all_retrieved = array();

  $all_retrieved['url'] = $app->fss->runsets_result_folder_url;
  if($sc_runset_id != null){
    $all_retrieved['url'] .= $sc_runset_id."/";
    $all_retrieved['url'] .= "repres_displayed/";
    if($sc_model_id != null){
      $all_retrieved['url'] .= $sc_model_id."/";
      if($sc_result_id != null){
        $all_retrieved['url'] .= $sc_result_id."/";
        if($time != null){
          $all_retrieved['url'] .= $time.$sc_result_id.'.png';
  }}}}

  // show
  return($app->util->show_json($res, $all_retrieved));
}

?>