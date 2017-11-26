<?php

use DbPrecipitations\PrecipitationSource; 

function process_get_request($app){
	
	// get params
	$show_main = $app->request->params("show_main", '1');
	$timestamp_ini = $app->request->params("timestamp_ini");
	$timestamp_end = $app->request->params("timestamp_end");
	
	// query search
	if(sizeof($app->request->params()) == 0){
		// no argument, gets all
		$all_retrieved = PrecipitationSource::all();
	
	}  else {
		
		if ((!is_null($timestamp_ini)) && (!is_null($timestamp_end))) {
			// basic check - valid timestamps
			if ($timestamp_end <= $timestamp_ini){
				$return_array = array("error"=>"Invalid timestamps");
				echo(json_encode($return_array));
				exit(0);
			}
			
			// get all accepted precipitation sources
			if($show_main == "all"){
				$all_precips = PrecipitationSource::all();
			} else {
				$all_precips = PrecipitationSource::where('show_main', 
				                                          $show_main);
				$all_precips = $all_precips->get();
			}
			
			// for each, evaluate if data is available
			$all_retrieved = array();
			foreach($all_precips as $cur_precip){
				
				// get number of registers
				$cur_schema = $cur_precip["schema_name"];
				$cur_table = $cur_schema.".map_index";
				try{
					$precip_count = $app->dbs->table($cur_table, 
					                                 'precipitation');
					$whereRaw = "unix_time >= ".$timestamp_ini." AND ";
					$whereRaw .= "unix_time <= ".$timestamp_end;
					$precip_count = $precip_count->whereRaw($whereRaw);
					$precip_count = $precip_count->count();
				}catch(Exception $e){
					$precip_count = 0;
				}
				
				// check if it is enought data
				$delta_timestamp = $timestamp_end - $timestamp_ini;
				$expct_count = ($delta_timestamp / 
				                ($cur_precip["time_resolution"] * 60)) + 1;
								
				if($expct_count == $precip_count){
					array_push($all_retrieved, $cur_precip);
				}
			}
		}
		
		// $all_retrieved = array(array("TODO"=>"todo timestamp"));
		
	}
	
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