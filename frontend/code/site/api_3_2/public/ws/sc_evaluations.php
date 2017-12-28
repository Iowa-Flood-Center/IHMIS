<?php

use DbModels\ScEvaluation;

function process_get_request($app, $req, $res){
	
	// get params
	$from_references = $app->util->get_param($req, "from_references");
	$for_hlmodel = $app->util->get_param($req, "for_hlmodel");
	
	// query search
	if(sizeof($req->getQueryParams()) == 0) {
		// no argument, gets all
		$all_retrieved = ScEvaluation::all();
	
	} else if((!is_null($from_references))&&(!is_null($for_hlmodel))) {
		// filter by reference and hl model, find commons
		$all_ref = ScEvaluation::fromReferences($app, explode(",",$from_references));
		$all_hlm = ScEvaluation::forHlModel($app, $for_hlmodel);
		$all_retrieved = array();
		foreach($all_ref as $cur_ref){
			foreach($all_hlm as $cur_hlm){
				// if($cur_ref["id"] == $cur_hlm["id"]){
				if($cur_ref->id == $cur_hlm->id){
					$pre_add = false;
					foreach($all_retrieved as $cur_add){
						if($cur_add->id == $cur_ref->id){
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
	
	} else if(!is_null($from_references)) {
		// filter by reference
		$all_retrieved = ScEvaluation::fromReferences($app, 
		                                              explode(",",$from_references));
	} else if(!is_null($for_hlmodel)){
		// filter by hl-model
		$all_retrieved = ScEvaluation::forHlModel($app, $for_hlmodel);
	}
	
	// show it in JSON format
	return($app->util->show_json($res, $all_retrieved));
}

?>