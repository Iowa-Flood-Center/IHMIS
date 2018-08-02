<?php

use DbModels\HlModel;
use DbModels\ScRepresentationComposition;

function process_get_request($app){
	//

	if(sizeof($app->request->params()) == 0){
		// no argument, gets all
		$all_retrieved_obj = ScRepresentationComposition::all();
		$all_retrieved = Array();
		foreach($all_retrieved_obj as $cur_retrieved){
			$cur_array = $cur_retrieved->toArray();
			$cur_array['roles_mdl'] = $cur_retrieved->scrolesmodel()->get()->toArray();
			array_push($all_retrieved, $cur_array);
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