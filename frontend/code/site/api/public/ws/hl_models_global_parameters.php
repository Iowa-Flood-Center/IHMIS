<?php

use DbModels\HlModel;
use DbModels\HlModelGlobalParameter;

function process_get_request($app, $req, $res){
  
  // get params
  $from_hlmodel = $app->util->get_param($req, "from_hlmodel");
  
  // query search
  $all_retrieved = null;
  if(sizeof($req->getQueryParams()) == 0){
    // no argument, gets all
    $all_retrieved = HlModelGlobalParameter::all();
  
  } elseif (!is_null($from_hlmodel)) {
    // gets all listed hl-model and its listed global parameters
    $the_model = HlModel::where('id', (int)$from_hlmodel)->get()->first();
    $all_retrieved = array();
    if(!is_null($the_model)){
      $all_gblparms = $the_model->globalparameters($app)->get();
      foreach($all_gblparms as $cur_gblparms){
        array_push($all_retrieved, $cur_gblparms);
      }
    }
  }
  
  // show it in JSON format
  return($app->util->show_json($res, $all_retrieved));
}

?>