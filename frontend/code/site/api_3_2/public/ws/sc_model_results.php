<?php

use Results\ModelResult as ModelResult;

function process_get_request($app){
	// get params
	$runset_id = $app->request->params("runset_id");
	$model_id = $app->request->params("model_id");
	
	ModelResult::setApp($app);
	
	$all_retrieved = array();
	if(!is_null($runset_id)){
		if(!is_null($model_id)){
			$all_retrieved = Array(ModelResult::withId($model_id, $runset_id));
		} else {
			$all_retrieved = ModelResult::all($runset_id);
		}
	}
	
	// show
	echo(json_encode($all_retrieved));
}

function process_delete_request($app, $sc_runset_id){
	echo(json_encode(array("error" => "Function not implemented yet.")));
}

?>