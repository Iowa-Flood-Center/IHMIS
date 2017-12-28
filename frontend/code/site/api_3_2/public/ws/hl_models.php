<?php

use DbModels\HlModel;

function process_get_request($app, $req, $res){
  // get params
  $show_main = $app->util->get_param($req, "show_main");
  $timestamp_ini = $app->util->get_param($req, "timestamp_ini");
  $timestamp_end = $app->util->get_param($req, "timestamp_end");
  
  // query search
  $all_retrieved = null;
  if (sizeof($req->getQueryParams()) == 0){
    // no argument, gets all
    $all_retrieved = HlModel::all();
    
  } elseif (!is_null($show_main)) {
    // gets only public-available hl-models
    $all_retrieved = HlModel::where('show_main', $show_main)->get();
    
  } elseif ((!is_null($timestamp_ini)) && (!is_null($timestamp_end))) {
    // gets only models with initial conditions available between given dates
    $all_retrieved = HlModel::inTimestampsInterval($app, $timestamp_ini, $timestamp_end);
	//echo(sizeof($all_retrieved)."_".$timestamp_ini."_".$timestamp_end."_");
  }
  
  // basic check
  if (is_null($all_retrieved)){
    echo(json_encode($app->invalid_argument));
    return;}
  
  // show it in JSON format
  return($app->util->show_json($res, $all_retrieved));
}
?>