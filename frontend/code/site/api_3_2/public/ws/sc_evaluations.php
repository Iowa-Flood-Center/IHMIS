<?php

use DbModels\ScEvaluation;

function process_get_request($app){
	
	// get params
	$from_references = $app->request->params("from_references");
	$for_hlmodel = $app->request->params("for_hlmodel");
	
	// query search
	if(sizeof($app->request->params()) == 0) {
		// no argument, gets all
		$all_retrieved = ScEvaluation::all();
	
	} else if((!is_null($from_references))&&(!is_null($for_hlmodel))) {
		// filter by reference and hl model, find commons
		$all_ref = ScEvaluation::fromReferences($app, explode(",",$from_references));
		$all_hlm = ScEvaluation::forHlModel($app, $for_hlmodel);
		$all_retrieved = array();
		foreach($all_ref as $cur_ref){
			foreach($all_hlm as $cur_hlm){
				if($cur_ref["id"] == $cur_hlm["id"]){
					$pre_add = false;
					foreach($all_retrieved as $cur_add){
						if($cur_add["id"] == $cur_ref["id"]){
							$pre_add = true;
							break;
						}
					}
					if($pre_add == false){
						array_push($all_retrieved, $cur_ref);
					}
				}
			}
		}
		
		/*
		try{
			$all_retrieved = array_intersect($all_ref, $all_hlm);
		} catch(ErrorException $e){
			echo("Caught exception: '".$e->getMessage()."' for '".gettype($all_ref)."' and '".gettype($all_hlm)."'.<br />");
			echo("<pre>");
			print_r($all_ref);
			echo("</pre>");
			echo("<br />");
			echo("<pre>");
			print_r($all_hlm);
			echo("</pre>");
			exit();
		}
		*/
	
	} else if(!is_null($from_references)) {
		// filter by reference
		$all_retrieved = ScEvaluation::fromReferences($app, 
		                                              explode(",",$from_references));
	} else if(!is_null($for_hlmodel)){
		// filter by hl-model
		$all_retrieved = ScEvaluation::forHlModel($app, $for_hlmodel);
	}
	
	// show it in JSON format
	$app->util->show_json($all_retrieved);
}

?>