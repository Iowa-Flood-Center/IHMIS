<?php

use Results\RunsetResult as RunsetResult;

function process_post_request($app, $req, $res){

  // get arguments
  $post_data = $req->getParsedBody();
  
  RunsetResult::setApp($app);
  
  // basic check on posted arguments
  if(sizeof($post_data) == 0){
    $return_array = array("Exception" => "No parameter provided.");
    return($app->util->show_json($res, $return_array));
  } elseif (!array_key_exists('id', $post_data)) {
    $return_array = array("Exception" => "Missing 'runset_id' argument.");
    return($app->util->show_json($res, $return_array));
  } elseif (!array_key_exists('name', $post_data)) {
    $return_array = array("Exception" => "Missing 'runset_name' argument.");
    return($app->util->show_json($res, $return_array));
  } elseif (!array_key_exists('about', $post_data)) {
    $return_array = array("Exception" => "Missing 'runset_about' argument.");
    return($app->util->show_json($res, $return_array));
  } elseif (!array_key_exists('timestamp_ini', $post_data)) {
    $return_array = array("Exception" => "Missing 'timestamp_ini' argument.");
    return($app->util->show_json($res, $return_array));
  } elseif (!array_key_exists('timestamp_end', $post_data)) {
    $return_array = array("Exception" => "Missing 'timestamp_end' argument.");
    return($app->util->show_json($res, $return_array));
  }

  // 
  
  try{
    if(RunsetResult::saveRealtimeSnapshot($post_data)){
	  $return_array = array("Success"=>"yes");
    } else {
	  $return_array = array("Success"=>"no");
    }
  } catch (Exception $e){
    $return_array = array("Exception"=>$e->getMessage());
  }
  
  return($app->util->show_json($res, $return_array));
}

?>