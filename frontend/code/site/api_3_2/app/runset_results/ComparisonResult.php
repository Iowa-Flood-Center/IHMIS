<?php

  namespace Results;
  
  use Results\MetaFile as MetaFile;
  
  class ComparisonResult extends MetaFile{
    
	const ROOT_ATTR = "comparison_matrix";          // must-have
	const SUB_META_FOLDER_NAME = "cross_matrices";  // must-have
	const FILE_BASENAME = "Comparison_matrix";
	
	// //////////////////// INTERFACE //////////////////// //
	
	/**
	 * RETURN: Array of Strings. All representation IDs from given model.
	 */
	public static function withModel($runset_id, $model_id){
      
	}
	
	/**
	 * Deletes all files from a comparison
	 */
	public static function delete($model_1_id, $model_2_id, $runset_id){
      // TODO
	}
	
	/**
	 * Deletes all files from a comparison
	 */
	public static function delete_model($model_id, $runset_id){
      // TODO
	}

  }

?>