<?php

use DbModels\ScReference;

function process_get_request($app){

	// get params
	$timeset = $app->request->params("timeset");
	
	// query search
	if(sizeof($app->request->params()) == 0){
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
	$return_array = array();
	foreach($all_retrieved as $cur_screpresentation){
		if (is_object($cur_screpresentation)){
			array_push($return_array, $cur_screpresentation->toArray());
		} elseif(is_array($cur_screpresentation)) {
			array_push($return_array, $cur_screpresentation);
		} else {
			echo("What is '".$cur_screpresentation."'?<br />");
		}
	}
	echo(json_encode($return_array));
}

?> 