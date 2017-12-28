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
		public function show_json($response, $all_retrieved){
			$return_array = array();
			foreach($all_retrieved as $cur_screpresentation){
				if (is_object($cur_screpresentation)){
					if(method_exists($cur_screpresentation, 'toArray')){
						array_push($return_array, $cur_screpresentation->toArray());
					} else {
						array_push($return_array, get_object_vars($cur_screpresentation));
					}
				} elseif(is_array($cur_screpresentation)) {
					array_push($return_array, $cur_screpresentation);
				} else {
					$error_tag = "ERROR";
					$error_msg = "Invalid object format (".gettype($cur_screpresentation).").";
					echo(json_encode(array($error_tag=>$error_msg)));
					exit();
				}
			}
			return($response->withJson($return_array));
		}
		
		/**
		 * Gets the value of a parameter if it exists. Null otherwise.
		 * $request: Slim\Http\Request
		 * $param_id: String
		 */
		public function get_param($request, $param_id){
			$all_params = $request->getQueryParams();
			if(array_key_exists($param_id, $all_params))
				return($all_params[$param_id]);
			else
				return(null);
		}
	}
	
	if(!isset($app->util)){
		$app->util = new AppUtil();
	}
}

?>