<?php

use Results\ForecastSet as ForecastSet;

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

function process_get_request($app, $req, $res){
	// get params
	$runset_id = $app->util->get_param($req, "runset_id");
	$model_id = $app->util->get_param($req, "model_id");

	// basic check
	if(is_null($runset_id)){
		echo(json_encode(Array()));
		return;
	}
	
	ForecastSet::set_app($app);
	if(!is_null($model_id)){
		// $all_retrieved = Array(ModelResult::withId($model_id, $runset_id));
	} else {
		$all_retrieved = ForecastSet::all($runset_id);
	}
	
	// show it in JSON format
	return($app->util->show_json($res, $all_retrieved));
}

function process_delete_request($app, $sc_runset_id){
	echo(json_encode(array("error" => "Function not implemented yet.")));
}


?>
