<?php
  
  namespace Results;
  
  class EvaluationMatrixResult extends MetaFile{
	
	const ROOT_ATTR = "evaluation_matrix";          // must-have
    const SUB_META_FOLDER_NAME = "cross_matrices";  // must-have
    const FILE_BASENAME = "Evaluation_matrix";
	
	/**
	 * 
	 * RETURN: Array of Strings. All pairs "EVALUATION_REFERENCE" associated with given model.
	 */
	public static function forModel($runset_id, $model_id){
	  $return_array = Array();
	  $read_base_matrix = EvaluationMatrixResult::get_base($runset_id);
	  foreach($read_base_matrix as $cur_key => $cur_array){
		if(!in_array($model_id, $cur_array)) continue;
		array_push($return_array, $cur_key);
	  }
	  return($return_array);
	}
  }
?>