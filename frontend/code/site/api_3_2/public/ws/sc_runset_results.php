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
  } elseif (!array_key_exists('runset_id', $post_data)) {
    $return_array = array("Exception" => "Missing 'runset_id' argument.");
    return($app->util->show_json($res, $return_array));
  }

  $runset_id = $post_data['runset_id'];
  try{
    if(sizeof($post_data) == 1){
      // create empty object in the file system
      RunsetResult::create(['id' => $runset_id]);
      $return_array = array("Success" => "Reserved runset id '".$runset_id."'");
	  
    } else {
      $any_change = false;
	  $target_runset = RunsetResult::where('id', $runset_id)[0];
      if(array_key_exists('show_main', $post_data)) {
        $any_change = true;
		$target_runset->show_main($post_data['show_main']);
      }
	  if(array_key_exists('hide_main', $post_data)) {
		$any_change = true;
		$target_runset->hide_main($post_data['hide_main']);
      }
	  if (!$any_change){
		$return_array = array("Failure" => "No valid action.");
	  } else {
		$return_array = array("Success" => "Edited runset with id '".$runset_id."'");
      }
    }
  } catch(Exception $exp) {
    $return_array = array("Exception" => $exp->getMessage());
  }
  return($app->util->show_json($res, $return_array));
}

function process_get_request($app, $req, $res){
  $with_id = $app->util->get_param($req, "id");
  $concurrently_id = $app->util->get_param($req, "concurrently_id");
  
  RunsetResult::setApp($app);
  
  // query search
  if(sizeof($req->getQueryParams()) == 0){
    $return_runsetresults = RunsetResult::all();
  } elseif (!is_null($with_id)) {
    $return_runsetresults = RunsetResult::where('id', $with_id);
  } elseif (!is_null($concurrently_id)) {
    $return_runsetresults = RunsetResult::concurrentlyTo($concurrently_id);
    // $return_runsetresults = array("error"=>"unexpected parametera");
  } else {
    $return_runsetresults = array("error"=>"unexpected parameter");
  }
  
  // translate result into array
  $return_array = array();
  foreach($return_runsetresults as $cur_runsetresult){
    if (is_object($cur_runsetresult)){
      array_push($return_array, $cur_runsetresult->toArray());
    } elseif(is_array($cur_runsetresult)) {
      array_push($return_array, $cur_runsetresult);
    } else {
      echo("What is '".$cur_runsetresult."'?\n");
    }
  }
  
  // sort array by init_timestamp
  usort($return_array, function($runset_a, $runset_b){
    $SORT_FIELD = 'timestamp_ini';
    if(!isset($runset_a[$SORT_FIELD])){
      return(-1);
    } elseif(!isset($runset_b[$SORT_FIELD])){
      return(1);
    } elseif ($runset_a[$SORT_FIELD] < $runset_b[$SORT_FIELD]) {
      return(-1);
    } else {
      return(1);
    }
  });
  
  // show it in JSON format
  return($app->util->show_json($res, $return_array));
}

function process_delete_request($app, $sc_runset_id){
  echo(json_encode(array("error" => "Function not implemented yet.")));
}

?>