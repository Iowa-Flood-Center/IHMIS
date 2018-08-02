<?php

  namespace Results;
  
  use Results\ComparisonResult as ComparisonResult;
  use Results\DataSource;
  require_once '../../common/libs/data_access.php';
  
  class ModelResult{
    
    const ROOT_ATTR = "sc_model";   // must-have
    public $attr;                   // must-have
    private static $app;            // must-have
    
	const SUB_REPR_FOLDER_PATH = "/repres_displayed/";
	const SUB_REF0_FOLDER_PATH = "/txts_timestamp_ref0/";
    const SUB_META_FOLDER_PATH = "sc_models/";
    const SUB_FILE_PATH_FRAME = "sc_models/%s.json";
    const SUB_FILE_EXT = ".json";
    
    // //////////////////// INTERFACE //////////////////// //
    
    /**
     * List all models from Runset
     */
    public static function all($runset_id){
      // basic check
      if(!isset(self::$app)) return(array());
      
      $return_array = Array();
      
      if (DataSource::isSourceLocalFilePath(self::$app)){
        $folder_path = self::$app->fss->runsets_result_folder_path;
        $folder_path .= $runset_id."/metafiles/".ModelResult::SUB_META_FOLDER_PATH;
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
      } elseif(DataSource::isSourceRemoteFilePath(self::$app)) {
        $return_array = array();
		
		$all_files = \DataAccess::list_metafolder_content(ModelResult::SUB_META_FOLDER_PATH, 
                                                          $runset_id, ModelResult::SUB_FILE_EXT);
        foreach($all_files as $cur_file){
          $model_id = basename($cur_file, ModelResult::SUB_FILE_EXT);
          $cur_obj = ModelResult::withId($model_id, $runset_id);
		  array_push($return_array, $cur_obj);
		}
		
      } else {
        $return_array = array();
		$return_array["ERROR"] = "Not a source of data available.";
      }
      
      return($return_array);
    }
    
    /**
     * Create an object from the root folder path
     */
    public static function withId($model_id, $runset_id){
      if (DataSource::isSourceLocalFilePath(self::$app)){
        // read main model meta file
	    $folder_path = self::$app->fss->runsets_result_folder_path;
		$file_sub_path = "/metafiles/";
        $file_sub_path .= sprintf(ModelResult::SUB_FILE_PATH_FRAME, $model_id);
        $file_path = $folder_path.$runset_id.$file_sub_path;
	  
	    // add evaluations
	    if(file_exists($file_path)){
          $return_obj = ModelResult::fromFile($file_path);
	      MetaFile::set_app(self::$app);
	      $return_obj["sc_evaluation_set"] = EvaluationMatrixResult::forModel($runset_id, $model_id);
	    }
      } elseif(DataSource::isSourceRemoteFilePath(self::$app)) {
        $file_sub_path = sprintf(ModelResult::SUB_FILE_PATH_FRAME, $model_id);
		if(\DataAccess::check_metafile_exists($file_sub_path, 
                                              $runset_id)){
		  $file_content = \DataAccess::get_metafile_content($file_sub_path, $runset_id);
		  $return_obj = ModelResult::fromFileContent($file_content);
		} else {
          $return_obj = null;
        }
		
	  } else {
        $return_obj = null;
      }
	  
      return($return_obj);
    }
	
	/**
	 *
	 */
	public static function withTitle($model_title, $runset_id){
      $all_files = ModelResult::get_all_model_meta_file_path($runset_id);
	  $model_obj = null;
	  foreach($all_files as $cur_file_path){
        $cur_model_obj = ModelResult::fromFile($cur_file_path);
		if ($cur_model_obj["title"] != $model_title) continue;
		$model_obj = $cur_model_obj;
		break;
      }
	  return($model_obj);
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
      if(!file_exists($file_path)) return(null); 
      $return_obj = new self();
	  return(ModelResult::fromFileContent(file_get_contents($file_path)));
    }
	
	/**
	 *
	 */
	public static function fromFileContent($file_content){
      $return_obj = new self();
      $return_obj->attr = json_decode($file_content);
      $root_attr = self::ROOT_ATTR;
      $return_obj = get_object_vars($return_obj->attr->$root_attr);
	  if(!isset($return_obj['show_main'])){
        $return_obj['show_main'] = false;
      }
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
	
	/**
	 *
	 */
	private static function get_all_model_meta_file_path($runset_id){
      // basic check
      if (!isset(self::$app)) return(null);
	
      $folder_path = self::$app->fss->runsets_result_folder_path;
	  $folder_path .= $runset_id . ModelResult::SUB_META_FOLDER_PATH;
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