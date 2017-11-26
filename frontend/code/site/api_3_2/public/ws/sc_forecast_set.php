<?php

use Results\ForecastSet as ForecastSet;

function process_get_request($app){
	// get params
	$runset_id = $app->request->params("runset_id");
	$model_id = $app->request->params("model_id");

	// basic check
	if(is_null($runset_id)){
		echo(json_encode(Array()));
		return;
	}
	
	
	ForecastSet::setApp($app);
	if(!is_null($model_id)){
		// $all_retrieved = Array(ModelResult::withId($model_id, $runset_id));
	} else {
		$all_retrieved = ForecastSet::all($runset_id);
	}
	echo(json_encode($all_retrieved));
	//echo("[]");
}

function process_delete_request($app, $sc_runset_id){
	echo(json_encode(array("error" => "Function not implemented yet.")));
}


?>
