<?php

  namespace Results;
  
  use Results\ComparisonResult as ComparisonResult;
  
  class ModelResult{
    
    const ROOT_ATTR = "sc_model";   // must-have
    public $attr;                   // must-have
    private static $app;            // must-have
    
	const SUB_REPR_FOLDER_PATH = "/repres_displayed/";
	const SUB_REF0_FOLDER_PATH = "/txts_timestamp_ref0/";
    const SUB_META_FOLDER_PATH = "/metafiles/sc_models/";
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
      $folder_path .= $runset_id . ModelResult::SUB_META_FOLDER_PATH;
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

    /**
     * Deletes the files associated with the model from the front end.
     * Creates a model delete request.
     */
    public static function delete($model_id, $runset_id){
      // delete from frontend
      ModelResult::delete_metafile($model_id, $runset_id);
      ModelResult::delete_files($model_id, $runset_id);
      ComparisonResult::delete_model($model_id, $runset_id);
      EvaluationResult::delete_model($model_id, $runset_id);
      
      // create request
      ModelResult::create_delete_request($model_id, $runset_id);
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
        if (preg_match("/_script$/", $key))
          unset($return_obj[$key]);
      }
      return($return_obj);
    }
    
    /**
     *
     */
    private static function delete_metafile($model_id, $runset_id){
      $runset_folder_path = self::$app->fss->runsets_result_folder_path;
      $runset_folder_path .= $runset_id;
        
      // delete main metafile
      $file_sub_path = sprintf(ModelResult::SUB_FILE_PATH_FRAME, $model_id);
	  ModelResult::delete_deep($runset_folder_path.$file_sub_path);
    }
    
    /**
     *
     */
    private static function delete_files($model_id, $runset_id){
      $runset_folder_path = self::$app->fss->runsets_result_folder_path;
	  $runset_folder_path .= $runset_id;
	  
	  // delete images
      $runset_repr_displayed_folder_path = $runset_folder_path.ModelResult::SUB_REPR_FOLDER_PATH;
	  $runset_repr_displayed_folder_path .= $model_id;
	  ModelResult::delete_folder($runset_repr_displayed_folder_path);
      
      // delete timestamps
	  $runset_ref0_displayed_folder_path = $runset_folder_path.ModelResult::SUB_REF0_FOLDER_PATH;
	  $runset_ref0_displayed_folder_path .= $model_id;
	  ModelResult::delete_folder($runset_ref0_displayed_folder_path);
    }
    
    /**
     *
     */
    private static function create_delete_request($model_id, $runset_id){
      echo("Creates model delete request. ");
    }
	
	/**
	 * Deletes file or folder.
	 * TODO - move to a common place
	 */
	private static function delete_any($path){
	  try{
	    if(is_dir($path)) rmdir($path);
	    if(is_file($path)) unlink($path);
	  } catch (Exception $e) {
        return;
      }
	}
	
	/**
	 * Deletes a file. If it is a symbolic link, deletes also the target file.
	 * TODO - move to a common place
	 */
	private static function delete_deep($path){
      if(is_link($path)){
        $target_path = readlink($path);
		ModelResult::delete_any($path);
      }
	  ModelResult::delete_any($path);
	}
	
	/**
	 *
	 * TODO - move to a common place
	 */
	private static function delete_folder($path){
      if (is_dir($path)) {
        $objects = scandir($path); 
        foreach ($objects as $object) {
          if (($object != ".") && ($object != "..")){
            $sub_path = $path."/".$object;
            if (is_dir($sub_path))
              ModelResult::delete_folder($sub_path);
            else
              ModelResult::delete_deep($sub_path);
          }
        }
        ModelResult::delete_deep($path); 
      }
	}
  }

?>