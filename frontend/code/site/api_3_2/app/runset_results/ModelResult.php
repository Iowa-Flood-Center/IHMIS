<?php

  namespace Results;
  
  class ModelResult{
    
    const ROOT_ATTR = "sc_model";   // must-have
    public $attr;                   // must-have
    private static $app;            // must-have
    
    const SUB_FOLDER_PATH = "/metafiles/sc_models/";
    const SUB_FILE_PATH_FRAME = "/metafiles/sc_models/%s.json";
	const SUB_FILE_EXT = ".json";
    
    // //////////////////// INTERFACE //////////////////// //
    
    /**
     * List all models from Runset
     */
    public static function all($runset_id){
      // basic check
      if(!isset(self::$app)) return(array());
      
      $return_array = Array();
      
      $folder_path = self::$app->fss->runsets_result_folder_path;
      $folder_path .= $runset_id . ModelResult::SUB_FOLDER_PATH;
      $all_files = scandir($folder_path);
      foreach($all_files as $cur_file){
        if(($cur_file == ".") || ($cur_file == "..")){ continue; }
        try{
          // $cur_obj = json_decode(file_get_contents($folder_path . $cur_file));
		  $cur_obj = ModelResult::withId(basename($cur_file, ModelResult::SUB_FILE_EXT), 
		                                 $runset_id);
		  array_push($return_array, $cur_obj);
        } catch (Exception $e) {
		  echo("Exception: ".$e->getMessage());
          continue;
        }
      }
      
      return($return_array);
    }
    
    /**
     * Create an object from the root folder path
     */
    public static function withId($model_id, $runset_id){
      $folder_path = self::$app->fss->runsets_result_folder_path;
      $file_sub_path = sprintf(ModelResult::SUB_FILE_PATH_FRAME, $model_id);
      $file_path = $folder_path.$runset_id.$file_sub_path;
      $return_obj = ModelResult::fromFile($file_path);
	  // $return_obj = Array();
      return($return_obj);
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
	  foreach($return_obj as $key => $val){
		  if (preg_match("/_script$/", $key)){
			  unset($return_obj[$key]);
		  }
	  }
	  return($return_obj);
	}
    
  }

?>