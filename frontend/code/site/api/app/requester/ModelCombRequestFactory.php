<?php

	namespace Requester;

	//
	abstract class ModelCombRequestFactory{
		
		public static function getModelCombRequests($posts){
			
			// organizing input in an array
			$modelcomb_dict = array();
			foreach($posts as $cur_key => $cur_value) {
				if (!preg_match('/^modelcomb_.+$/', $cur_key)) continue;
				
				// 
				$cur_splitted = explode("_", $cur_key);
				$cur_repr_comb = $cur_splitted[1];
				foreach($cur_value as $cur_subvalue){
				
					$cur_splitted = explode("_", $cur_subvalue);
					$cur_role = $cur_splitted[0];
					$cur_model_id = $cur_splitted[1];
					
					// 
					if(!array_key_exists($cur_repr_comb, $modelcomb_dict)){
						$modelcomb_dict[$cur_repr_comb] = array();
					}
					$modelcomb_dict[$cur_repr_comb][$cur_model_id] = $cur_role;
				}
			}
			
			// creating objects
			$return_dict = array();
			foreach($modelcomb_dict as $cur_key => $cur_value) {
				$cur_obj = new ModelCombRequest($cur_key, $cur_value);
				array_push($return_dict, $cur_obj);
			}
			
			// 
			if(count($return_dict) > 0){
				return($return_dict);
			} else {
				return(null);
			}
		}
	}

?>