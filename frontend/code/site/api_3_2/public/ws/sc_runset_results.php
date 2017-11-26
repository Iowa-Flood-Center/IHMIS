<?php

use Results\RunsetResult as RunsetResult;

function process_get_request($app){
	
	$with_id = $app->request->params("id");
	
	RunsetResult::setApp($app);
	
	// query search
	if(sizeof($app->request->params()) == 0){
		$return_runsetresults = RunsetResult::all();
	
	} elseif (!is_null($with_id)) {
		$return_runsetresults = RunsetResult::where('id', $with_id);
	
	} else {
		$return_runsetresults = array("error"=>"unexpected parameter");
	}
	
	// show it in JSON format
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
	echo(json_encode($return_array));
}

function process_delete_request($app, $sc_runset_id){
	echo(json_encode(array("error" => "Function not implemented yet.")));
}

?>
