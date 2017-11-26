<?php

use DbArtefacts\Pois;

function process_get_request($app){
	
	// query search
	$all_retrieved = null;
	if (sizeof($app->request->params()) == 0){
		// no argument, gets all
		$all_retrieved = Pois::all();
		
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