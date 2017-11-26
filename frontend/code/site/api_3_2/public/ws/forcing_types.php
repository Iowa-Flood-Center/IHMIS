<?php

use DbModels\HlModel;
use DbModels\ForcingType;

function process_get_request($app){
	
	// get params
	$from_schlmodel = $app->request->params("from_hlmodel");
	
	// query search
	if(sizeof($app->request->params()) == 0){
		// no argument, gets all
		$all_retrieved = ForcingType::all();
	
	} elseif (!is_null($from_schlmodel)) {
		// gets the hl-model and lists its forcing types
		$the_model = HlModel::where('id', (int)$from_schlmodel)->get()->first();
		$all_forcings = $the_model->forcingtypes($app)->orderBy('order','ASC')->get();
		$all_retrieved = array();
		foreach($all_forcings as $cur_forcing){
			array_push($all_retrieved, $cur_forcing);
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