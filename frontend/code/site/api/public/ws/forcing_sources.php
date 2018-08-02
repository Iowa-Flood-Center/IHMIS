<?php

use DbModels\ForcingSource;

function process_get_request($app, $req, $res){

	$from_type = $app->util->get_param($req, "from_type");
	$timestamp_ini = $app->util->get_param($req, "timestamp_ini");
	$timestamp_end = $app->util->get_param($req, "timestamp_end");

	$all_retrieved = null;
	
	// query search
	if(sizeof($req->getQueryParams()) == 0){
		// no argument, gets all
		$all_retrieved = ForcingSource::all();
	
	} elseif (!is_null($from_type)) {
		if(is_numeric($from_type)){
			// if is numeric, assume is given type id
			$all_retrieved = ForcingSource::where('forcingtype_id', (int)$from_type)->get();
			
		} else {
			// if is string, assume is given type acronym
			$hl_model_query = $app->dbs->table('static_modelplus_definitions.forcingsource',
		                                       'model_backtime')
		                     ->join('static_modelplus_definitions.forcingtype', 
							        'static_modelplus_definitions.forcingtype.id', 
									'=',
									'static_modelplus_definitions.forcingsource.forcingtype_id')
							 
							 ->select('static_modelplus_definitions.forcingsource.*')
							 ->where('static_modelplus_definitions.forcingtype.acronym',
							         'LIKE',
									 $from_type);
			
			$all_retrieved = $hl_model_query->get();
			
		}
		
	}
	
	if((!is_null($timestamp_ini))&&(!is_null($timestamp_end))){
		if(is_null($all_retrieved)){
			$all_retrieved = ForcingSource::all();
		}
		
		// check each one to see which are available
		foreach($all_retrieved as $cur_key => $cur_retrieved){
			if(!$cur_retrieved->isAvailable($app, $timestamp_ini, 
			                                $timestamp_end)){
				unset($all_retrieved[$cur_key]);
			}
		}
	}
	
	// 
	
	// basic check
	if (is_null($all_retrieved)){
		echo(json_encode($app->invalid_argument));
		return;}
	
	// show it in JSON format
	return($app->util->show_json($res, $all_retrieved));
}

?>