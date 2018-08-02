<?php

	namespace Requester;

	//
	abstract class ModelRequestFactory{
		
		/**
		 *
		 */
		public static function getModelRequest($posts, $count_model){
			
			// basic check
			if(!isset($posts["model_id_".$count_model])){ 
				return(null);
			}
			
			// get most of fields
			$return_obj = new ModelRequest();
			$return_obj->model_id = $posts["model_id_".$count_model];
			$return_obj->model_title = $posts["model_title_".$count_model];
			$return_obj->model_desc = $posts["model_desc_".$count_model];
			$return_obj->hillslope_model_id = $posts["hillslope_model_".$count_model];
			
			// check title and description (fill if left empty)
			if (trim($return_obj->model_title) == ""){ $return_obj->model_title = $return_obj->model_id; }
			if (trim($return_obj->model_desc) == ""){ $return_obj->model_desc = $return_obj->model_title; }
			
			// get forcings sources
			$return_obj->forcings_dict = array();
			$count_fors = 1;
			while(isset($posts["model_for_".$count_model."_".$count_fors])){
				$return_obj->forcings_dict[] = $posts["model_for_".$count_model."_".$count_fors];
				$count_fors += 1;
			}
			
			// get parameters
			$parameter_set = array();
			$count_pars = 1;
			while(isset($posts["model_par_".$count_model."_".$count_pars])){
				$parameter_set[] = $posts["model_par_".$count_model."_".$count_pars];
				$count_pars = $count_pars + 1;
			}
			$return_obj->gbl_parameters = $parameter_set;
			
			// get model representations
			$field_id = "model_repr_".$count_model;
			$return_obj->model_reprs = ModelRequestFactory::read_array($field_id, $posts);
			
			// get model comb representations
			$field_id = "modelseq_repr_".$count_model;
			$return_obj->modelseq_reprs = ModelRequestFactory::read_array($field_id, $posts);
			
			// get evaluation
			$field_id = "model_eval_".$count_model;
			$return_obj->evaluations = ModelRequestFactory::read_array($field_id, $posts);
			
			return($return_obj);
		}
		
		/**
		 * Reads a post string and translate it into array of strings
		 */
		private static function read_array($field_id, $posts){
			if(isset($posts[$field_id])){
				if (is_array($posts[$field_id])){
					return($posts[$field_id]);
				} else {
					if (trim($posts[$field_id]) != ""){
						return(explode(",", $posts[$field_id]));
					}
				}
			} else {
				return(null);
			}
		}
	}

?>