<?php

use DbModels\HlModel;

function process_get_request($app){
	// get params
	$show_main = $app->request->params("show_main");
	$timestamp_ini = $app->request->params("timestamp_ini");
	$timestamp_end = $app->request->params("timestamp_end");
	
	// query search
	$all_retrieved = null;
	if (sizeof($app->request->params()) == 0){
		// no argument, gets all
		$all_retrieved = HlModel::all();
		
	} elseif (!is_null($show_main)) {
		// gets only public-available hl-models
		$all_retrieved = HlModel::where('show_main', $show_main)->get();
		
	} elseif ((!is_null($timestamp_ini)) && (!is_null($timestamp_end))) {
		// gets only models with initial conditions available between given dates
		$all_retrieved = HlModel::inTimestampsInterval($app, $timestamp_ini, $timestamp_end);
		
	}
	
	// basic check
	if (is_null($all_retrieved)){
		echo(json_encode($app->invalid_argument));
		return;}
	
	// show
	$return_array = array();
	foreach($all_retrieved as $cur_hlmodel){
		if (is_array($cur_hlmodel)){
			array_push($return_array, $cur_hlmodel);
		} elseif (is_object($cur_hlmodel)) {
			array_push($return_array, $cur_hlmodel->toArray());
		} elseif (is_null($cur_hlmodel)) {
			continue;
		} else {
			array_push($return_array, $cur_hlmodel);
		}
	}
	echo(json_encode($return_array));
}
?>