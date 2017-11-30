<?php

use DbModels\HlModel;
use DbModels\ScProduct;
use DbModels\ScRepresentation;

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

function process_get_request($app){

	// get possible params
	$from_scproducts = $app->request->params("from_products");
	$from_schlmodel = $app->request->params("from_hlmodel");
	$from_schlmodelcomp = $app->request->params("from_hlmodel_compareto");
	$from_combining = $app->request->params("from_combining");
	
	// query search
	if(sizeof($app->request->params()) == 0){
		// no argument, gets all
		$all_retrieved = ScRepresentation::all();
	
	} elseif (!is_null($from_scproducts)) {
		// gets all listed products, and for each, gets its representation		
		$all_scproducts_ids = explode(",", $from_scproducts);
		$all_products = ScProduct::whereIn('acronym', $all_scproducts_ids)->get();
		$all_retrieved = array();
		foreach($all_products as $cur_product){
			$all_retrieved = array_merge($all_retrieved, 
			                             $cur_product->get_screpresentations());
		}
		$all_retrieved = array_unique($all_retrieved);
		
	} elseif ((!is_null($from_schlmodel))&&(is_null($from_schlmodelcomp))) {
		// 
		$the_model = HlModel::where('id', (int)$from_schlmodel)->get()->first();
		$all_retrieved = array();
		if (is_null($the_model)){
			array_push($all_retrieved, array("error"=>
			                                 "No ".$from_schlmodel." model found."));
		} else {
			$all_representations = $the_model->screpresentations($app);
			foreach($all_representations as $cur_representation){
				array_push($all_retrieved, $cur_representation);
			}
		}
	} elseif ((!is_null($from_schlmodel))&&(!is_null($from_schlmodelcomp))) {
		//
		$the_model_1 = HlModel::where('id', (int)$from_schlmodel)->get()->first();
		$the_model_2 = HlModel::where('id', (int)$from_schlmodelcomp)->get()->first();

		$all_retrieved = array();
		if (is_null($the_model_1)){
			array_push($all_retrieved, array("error"=>
			                                 "No ".$from_schlmodel." model found."));
		} elseif (is_null($the_model_2)) {
			array_push($all_retrieved, array("error"=>
			                                 "No ".$from_schlmodelcomp." model found."));
		} else {
			$all_representations = $the_model_1->screpresentations_comparable($app, 
			                                                                  $the_model_2);
			foreach($all_representations as $cur_representation){
				array_push($all_retrieved, $cur_representation);
			}
		}
		
	} 
	elseif (!(is_null($from_combining))) {
		
		// search for valid Representations combined
		$simple_representations = explode(",", $from_combining);
		$all_retrieved = ScRepresentation::byCombining($simple_representations);
		
		if (ctype_digit(implode('', $simple_representations))){
			// consider given values as IDS
			$all_retrieved = array();
		} else {
			// consider given values as acronyms
			$all_retrieved = ScRepresentation::byCombining($simple_representations);
		}

	} else {
		$all_retrieved = array();
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