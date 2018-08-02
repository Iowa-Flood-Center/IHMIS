<?php
  
  namespace Results;
  
  use Results\MetaFile as MetaFile;
  use Results\DataSource;
  
  class EvaluationResult extends MetaFile{
      
    const ROOT_ATTR = "sc_evaluation";             // must-have
    const SUB_META_FOLDER_NAME = "sc_evaluations"; // must-have
    
    // //////////////////// INTERFACE //////////////////// //
    
    /**
     * List all models from Runset
     */
    public static function all($runset_id){
      // basic check
      if(!isset(MetaFile::$app)) return(array("Error" => "No app set."));
      
      $return_array = Array();
      
	  if (DataSource::isSourceLocalFilePath(MetaFile::$app)){
        $folder_path = MetaFile::get_folder_path($runset_id, EvaluationResult::SUB_META_FOLDER_NAME);
        $all_files = scandir($folder_path);
      } elseif(DataSource::isSourceRemoteFilePath(MetaFile::$app)) {
        $all_files = \DataAccess::list_metafolder_content(EvaluationResult::SUB_META_FOLDER_NAME, 
                                                          $runset_id, 
														  ModelResult::SUB_FILE_EXT);
      }

      foreach($all_files as $cur_file){
        if(($cur_file == ".") || ($cur_file == "..")){ continue; }
        try{
          $cur_eval_id = basename($cur_file, ModelResult::SUB_FILE_EXT);
          $cur_obj = EvaluationResult::withId($cur_eval_id, $runset_id);
          array_push($return_array, $cur_obj);
        } catch (Exception $e) {
          
        }
      }
      return($return_array);
    }
    
    /**
     * Create an object from the root folder path
     */
    public static function withId($evaluation_id, $runset_id){
      $file_name = $evaluation_id . MetaFile::FILE_EXT;
	  
	  if (DataSource::isSourceLocalFilePath(MetaFile::$app)){
        // define file path
        $folder_path = MetaFile::get_folder_path($runset_id, EvaluationResult::SUB_META_FOLDER_NAME);
        $file_path = $folder_path.$file_name;
      
        // read file content
        $return_obj = EvaluationResult::from_file($file_path);
      } elseif(DataSource::isSourceRemoteFilePath(MetaFile::$app)) {
		$file_sub_path = static::SUB_META_FOLDER_NAME."/".$file_name;
        $file_content = \DataAccess::get_metafile_content($file_sub_path, 
		                                                  $runset_id);
		$return_obj = static::from_file_content($file_content);
      } else {
        $return_obj = null;
	  }
      return($return_obj);
    }
    
    /**
     * Deletes all files from a comparison
     * TODO - should this be here?
     */
    public static function delete_model($model_id, $runset_id){
      // TODO
    }
  }
  
?>