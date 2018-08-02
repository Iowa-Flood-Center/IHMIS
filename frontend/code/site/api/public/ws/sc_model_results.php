<?php

use Results\MetaFile as MetaFile;
use Results\ModelResult as ModelResult;
use Results\ModelCombinationResult as ModelCombinationResult;

function process_get_request($app, $req, $res){
  // get params
  $runset_id = $app->util->get_param($req, "runset_id");
  $model_id = $app->util->get_param($req, "model_id");
  $model_title = $app->util->get_param($req, "model_title");
  
  MetaFile::set_app($app);
  ModelResult::setApp($app);
  
  $all_retrieved = array();
  if(!is_null($runset_id)){
    if(!is_null($model_id)){
      $all_retrieved_single = Array(ModelResult::withId($model_id, $runset_id));
      $all_retrieved_combined = Array(ModelCombinationResult::withId($model_id, $runset_id));
    } elseif(!is_null($model_title)) {
      $all_retrieved_single = Array(ModelResult::withTitle($model_title, $runset_id));
      $all_retrieved_combined = Array(ModelCombinationResult::withTitle($model_title, $runset_id));
    } else {
      $all_retrieved_single = ModelResult::all($runset_id);
      $all_retrieved_combined = ModelCombinationResult::all($runset_id);
    }
    $all_retrieved = array_merge($all_retrieved_single, $all_retrieved_combined);
    $all_retrieved = array_filter($all_retrieved);
  }

  // show
  return($app->util->show_json($res, $all_retrieved));
}

function process_delete_request($app, $sc_runset_id){
  echo(json_encode(array("error" => "Function not implemented yet.")));
}

?>