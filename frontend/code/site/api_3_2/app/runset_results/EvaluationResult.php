<?php
  
  namespace Results;
  
  class EvaluationResult{
	  
	const ROOT_ATTR = "sc_evaluation";   // must-have
    public $attr;                        // must-have
    private static $app;                 // must-have
	
	// //////////////////// INTERFACE //////////////////// //
	
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