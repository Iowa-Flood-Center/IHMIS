<?php

  namespace Results;
  
  use Results\DataSource;
  
  class ReferenceResult{
    const ROOT_ATTR = "sc_reference";   // must-have
    public $attr;                       // must-have
    private static $app;                // must-have
	
	const SUB_FOLDER_PATH = "sc_references/";
    const SUB_FILE_PATH_FRAME = "sc_references/%s.json";
	const SUB_FILE_EXT = ".json";
	
	// //////////////////// INTERFACE //////////////////// //
    
    /**
     * List all references from Runset
     */
    public static function all($runset_id){
      // basic check
      if(!isset(self::$app)) return(array());
      
	  if (DataSource::isSourceLocalFilePath(self::$app)){
        $return_array = Array();
      
        $folder_path = self::$app->fss->runsets_result_folder_path;
        $folder_path .= $runset_id."/metafiles/".ReferenceResult::SUB_FOLDER_PATH;
        $all_files = scandir($folder_path);
        foreach($all_files as $cur_file){
          if(($cur_file == ".") || ($cur_file == "..")){ continue; }
          try{
            // $cur_obj = json_decode(file_get_contents($folder_path . $cur_file));
		    $cur_obj = ReferenceResult::withId(basename($cur_file, ModelResult::SUB_FILE_EXT), 
		                                       $runset_id);
		    array_push($return_array, $cur_obj);
          } catch (Exception $e) {
		    echo("Exception: ".$e->getMessage());
            continue;
          }
        }
      } elseif(DataSource::isSourceRemoteFilePath(self::$app)) {
        $return_array = array();
		
		$all_files = \DataAccess::list_metafolder_content(ReferenceResult::SUB_FOLDER_PATH, 
                                                          $runset_id, ModelResult::SUB_FILE_EXT);
		foreach($all_files as $cur_file){
          $cur_id = basename($cur_file, ModelResult::SUB_FILE_EXT);
		  $cur_obj = ReferenceResult::withId($cur_id, $runset_id);
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
    public static function withId($reference_id, $runset_id){
      if (DataSource::isSourceLocalFilePath(self::$app)){
        $folder_path = self::$app->fss->runsets_result_folder_path;
        $file_sub_path = "/metafiles/".sprintf(ReferenceResult::SUB_FILE_PATH_FRAME, $reference_id);
        $file_path = $folder_path.$runset_id.$file_sub_path;
        $return_obj = ReferenceResult::fromFile($file_path);
      } elseif(DataSource::isSourceRemoteFilePath(self::$app)) {
		$file_sub_path = sprintf(ReferenceResult::SUB_FILE_PATH_FRAME, $reference_id);
        $file_content = \DataAccess::get_metafile_content($file_sub_path, $runset_id);
		$return_obj = ReferenceResult::fromFileContent($file_content);
		
      } else {
        $return_obj = Null;
      }
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
      return(ReferenceResult::fromFileContent(file_get_contents($file_path)));
	}
	
	public static function fromFileContent($file_content){
      $return_obj = new self();
	  $return_obj->attr = json_decode($file_content);
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