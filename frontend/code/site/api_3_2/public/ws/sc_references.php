<?php

use DbModels\ScReference;

function process_get_request($app, $req, $res){

  // get params
  $timeset = $app->util->get_param($req, "timeset");
  
  // query search
  if(sizeof($req->getQueryParams()) == 0){
    // no argument, gets all
    $all_retrieved = ScReference::all();
  
  } elseif (!is_null($timeset)) {
    if($timeset == "realtime"){
      $all_retrieved = ScReference::where("realtime", true)->get();
    } elseif($timeset == "historical") {
      $all_retrieved = ScReference::whereNotNull("timestamp_min")->get();
    } else {
      $all_retrieved = array();
    }
    
  }
  
  // show it in JSON format
  return($app->util->show_json($res, $all_retrieved));
}

?> 