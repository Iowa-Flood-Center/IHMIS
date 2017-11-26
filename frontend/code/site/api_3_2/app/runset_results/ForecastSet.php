<?php

  namespace Results;
  
  class ForecastSet{
	  
    const ROOT_ATTR = "forecast_matrix";   // must-have
    private static $app;            // must-have
    
    const SUB_FOLDER_PATH = "/metafiles/sc_models/";
    const SUB_FILE_PATH = "/metafiles/cross_matrices/Forecast_matrix.json";
	const SUB_FILE_EXT = ".json";
	
	// //////////////////// INTERFACE //////////////////// //
	
	/**
     * List all models from Runset
     */
    public static function all($runset_id){
      // basic check
      if(!isset(self::$app)) return(array());
      
      $folder_path = self::$app->fss->runsets_result_folder_path;
      $file_path = $folder_path . $runset_id . ForecastSet::SUB_FILE_PATH;
      
      $return_array = ForecastSet::fromFile($file_path);
      $return_array = (is_null($return_array)) ? Array() : $return_array;
      
      return($return_array);
    }
	
	// ///////////////////// GENERAL ///////////////////// //
	
	/**
	 *
	 */
	public static function setApp($app) { self::$app = $app; }
	
	/**
	 *
	 */
	public static function fromFile($file_path){
      if(!file_exists($file_path)){echo($file_path."\n"); return(null);}
      $return_obj = new self();
	  $return_obj->attr = json_decode(file_get_contents($file_path));
	  $root_attr = self::ROOT_ATTR;
	  $return_obj = get_object_vars($return_obj->attr->$root_attr);
	  return($return_obj);
	}
  
  }
  
?>
