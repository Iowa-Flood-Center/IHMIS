<?php

use DbArtefacts\Pois;
use DbArtefacts\PoisLinkId;

function process_get_request($app, $req, $res){
	
	// query search
	$all_retrieved = null;
	if (sizeof($req->getQueryParams()) == 0){
		// no argument, gets all
		$all_retrieved = Pois::all();
	} else {
		// has arguments - consider each
		
		// add 'connected_to' filter
		$connected_to = $app->util->get_param($req, "connected_to");
        if (!is_null($connected_to)){
			$all_retrieved = array();
			if((sizeof($connected_to) == 1) && ($connected_to == "link_id")){
				$all_retrieved = PoisLinkId::all();
			} elseif (in_array("com_id", $connected_to)){
				$all_retrieved = array();
				array_push($all_retrieved, "TODO: Implement com_id case.");
			}
		} else {
			$all_retrieved = Pois::all();
		}
		
		// add 'type' filter
		$type_filter = $app->util->get_param($req, "type");
		if (!is_null($type_filter)){
			if(!is_array($type_filter))
				$type_filter = [$type_filter];
			$all_retrieved_tmp = array();
			foreach($all_retrieved as $cur_pois){
				if(in_array($cur_pois->type, $type_filter)){
					array_push($all_retrieved_tmp, $cur_pois);
				}
			}
			$all_retrieved = $all_retrieved_tmp;
			$all_retrieved_tmp = null;
		}
		
		// add 'clean description' modifier
		$clean_description = $app->util->get_param($req, "clean_description");
		if (!is_null($clean_description)){
			$accepted_values = array("on", 1, "1");
			if (in_array($clean_description, $accepted_values)){
				$search = "/\(.*\)/";
				foreach($all_retrieved as $cur_pois){
					$cur_desc = $cur_pois->description;
					$cur_desc = trim(preg_replace($search, "", $cur_desc));
					$cur_pois->description = $cur_desc;
				}
			}
		}
	}
	
	// basic check
	if (is_null($all_retrieved)){
		return($app->invalid_argument);
		return;
	}
	
	// show
	return($app->util->show_json($res, $all_retrieved));
}

?>