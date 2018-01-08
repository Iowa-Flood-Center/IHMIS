<?php

  namespace Results;
  
  use Results\MetaFile as MetaFile;
  
  class ModelCombinationResult extends MetaFile{
    
    const ROOT_ATTR = "sc_modelcombination";              // must-have
    const SUB_META_FOLDER_NAME = "sc_modelcombinations";  // must-have
    
    // //////////////////// INTERFACE //////////////////// //
    
    /**
     * List all models from Runset
     */
    public static function all($runset_id){
      // basic check
      if(!isset(MetaFile::$app)) return(array("Error" => "No app set."));
      
      $return_array = Array();
      
      $folder_path = MetaFile::get_folder_path($runset_id, static::SUB_META_FOLDER_NAME);
      $all_files = scandir($folder_path);

      foreach($all_files as $cur_file){
        if(($cur_file == ".") || ($cur_file == "..")){ continue; }
        try{
          $cur_eval_id = basename($cur_file, ModelResult::SUB_FILE_EXT);
          $cur_obj = static::withId($cur_eval_id, $runset_id);
          array_push($return_array, $cur_obj);
        } catch (Exception $e) {
          
        }
      }
      return($return_array);
    }
    
    /**
     * Create an object from the root folder path
     */
    public static function withId($modelcomb_id, $runset_id){
      // define file path
      $folder_path = MetaFile::get_folder_path($runset_id, static::SUB_META_FOLDER_NAME);
      $file_name = $modelcomb_id . MetaFile::FILE_EXT;
      $file_path = $folder_path.$file_name;
      
      // read file content
      $return_obj = static::from_file($file_path);
      return($return_obj);
    }
    
	/**
	 *
	 */
	public static function withTitle($model_title, $runset_id){
      $all_files = ModelCombinationResult::get_all_model_meta_file_path($runset_id);
	  $model_obj = null;
	  foreach($all_files as $cur_file_path){
        $cur_model_obj = MetaFile::from_file($cur_file_path);
		if($cur_model_obj['title'] != $model_title) continue;
		$model_obj = $cur_model_obj;
		break;
      }
	  return($model_obj);
	}
	
	/**
	 *
	 */
	private static function get_all_model_meta_file_path($runset_id){
      // basic check
      if (!isset(self::$app)) return(null);
	
      $folder_path = MetaFile::get_folder_path($runset_id, static::SUB_META_FOLDER_NAME);
      $all_files = scandir($folder_path);
	  
	  $all_files = array_filter($all_files, function($file_name){
		return((($file_name == ".")||($file_name == "..")) ? false : true);
	  });
	  
	  foreach($all_files as $cur_key => $cur_file_name){
        $all_files[$cur_key] = $folder_path . $cur_file_name;
	  }
	  
	  return($all_files);
	}
  }
?>