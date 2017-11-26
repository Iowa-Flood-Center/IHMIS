<?php

/**
 * Returns TRUE if the current server is Sandbox or FALSE if it is Deploy
 */
function is_sandbox(){
	$sandbox_sname = 's-iihr50.iihr.uiowa.edu';
	return ($_SERVER['SERVER_NAME']==$sandbox_sname) ? true : false;
}

/**
 * Loads the utility functions used by Model Plus into the $app variable
 */
function load_utils($app){
	
	class AppUtil{
		
		/**
		 * 
		 * $arguments : Array of arrays or array of objects with the method 'toArray()'
		 * RETURN : True. Values are echoed.
		 */
		public function show_json($all_retrieved){
			$return_array = array();
			foreach($all_retrieved as $cur_screpresentation){
				if (is_object($cur_screpresentation)){
					array_push($return_array, $cur_screpresentation->toArray());
				} elseif(is_array($cur_screpresentation)) {
					array_push($return_array, $cur_screpresentation);
				} else {
					$error_tag = "ERROR";
					$error_msg = "Invalid object format (".gettype($cur_screpresentation).").";
					echo(json_encode(array($error_tag=>$error_msg)));
					exit();
				}
			}
			echo(json_encode($return_array));
		}
	}
	
	if(!isset($app->util)){
		$app->util = new AppUtil();
	}
}

?>