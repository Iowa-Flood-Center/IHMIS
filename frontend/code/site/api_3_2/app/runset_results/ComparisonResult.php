<?php

  namespace Results;
  
  class ComparisonResult{
    
	const ROOT_ATTR = "sc_model";   // must-have
    public $attr;                   // must-have
    private static $app;            // must-have
	
	const SUB_FILE_PATH = "/metafiles/cross_matrices/Comparison_matrix.json";
	
	// //////////////////// INTERFACE //////////////////// //
	
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
	
	// ///////////////////// GENERAL ///////////////////// //
	
	/**
	 *
	 */
	public static function setApp($app) { self::$app = $app; }
  }

?>