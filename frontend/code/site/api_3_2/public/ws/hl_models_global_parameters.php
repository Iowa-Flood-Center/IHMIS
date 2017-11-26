<?php

use DbModels\HlModel;
use DbModels\HlModelGlobalParameter;

function process_get_request($app){
	
	// $all_retrieved = array(array("This" => "worked"));
	
	// get params
	$from_hlmodel = $app->request->params("from_hlmodel");
	
	// query search
	$all_retrieved = null;
	if(sizeof($app->request->params()) == 0){
		// no argument, gets all
		$all_retrieved = HlModelGlobalParameter::all();
	
	} elseif (!is_null($from_hlmodel)) {
		// gets all listed hl-model and its listed global parameters
		$the_model = HlModel::where('id', (int)$from_hlmodel)->get()->first();
		$all_retrieved = array();
		if(!is_null($the_model)){
			$all_gblparms = $the_model->globalparameters($app)->get();
			foreach($all_gblparms as $cur_gblparms){
				array_push($all_retrieved, $cur_gblparms);
			}
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