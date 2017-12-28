<?php

use DbModels\HlModel;
use DbModels\ForcingType;

function process_get_request($app, $req, $res){
  
  // get params
  $from_schlmodel = $app->util->get_param($req, "from_hlmodel");
  
  // query search
  if(sizeof($req->getQueryParams()) == 0){
    // no argument, gets all
    $all_retrieved = ForcingType::all();
  
  } elseif (!is_null($from_schlmodel)) {
    // gets the hl-model and lists its forcing types
    $the_model = HlModel::where('id', (int)$from_schlmodel)->get()->first();
    $all_forcings = $the_model->forcingtypes($app)->orderBy('order','ASC')->get();
    $all_retrieved = array();
    foreach($all_forcings as $cur_forcing){
      array_push($all_retrieved, $cur_forcing);
    }
    
  }
  
  // show it in JSON format
  return($app->util->show_json($res, $all_retrieved));
}

?>