<?php

  namespace Results;
  
  class RunsetResult{
    
	const ROOT_ATTR = "sc_runset";  // must-have
	public $attr;                   // must-have
	private static $app;            // must-have
	
	const SUB_FILE_PATH = "/metafiles/sc_runset/Runset.json";
	
	// //////////////////// INTERFACE //////////////////// //
	
	/**
	 * List all files
	 */
	public static function all(){
      // basic check
	  if(!isset(self::$app)) return(array());
		
      // list all files and create a new object for each
	  $folder_path = self::$app->fss->runsets_result_folder_path;
	  $all_files = scandir($folder_path);
	  $all_return = array();
	  foreach($all_files as $cur_file){
        if(($cur_file == ".") || ($cur_file == "..")){ continue; }
		$cur_file_path = $folder_path.$cur_file;
		$cur_object = RunsetResult::fromFolder($cur_file_path);
		if(!is_null($cur_object)){array_push($all_return, $cur_object);}
	  }
	  
	  return($all_return);
	}
	
	/**
	 * Create an object from the root folder path
	 */
	public static function fromFolder($folder_path){
      $file_path = $folder_path.RunsetResult::SUB_FILE_PATH;
      $return_obj = RunsetResult::fromFile($file_path);
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
	public function toArray(){ return($this->attr); }
	
	/**
	 *
	 */
	public static function fromFile($file_path){
      if(!file_exists($file_path)){return(null);}
      $return_obj = new self();
	  $return_obj->attr = json_decode(file_get_contents($file_path));
	  $root_attr = self::ROOT_ATTR;
	  $return_obj->attr = get_object_vars($return_obj->attr->$root_attr);
	  return($return_obj);
	}
	
	/**
	 *
	 */
	public static function where($attribute, $value){	  
	  $all_objects = self::all();
	  $all_return = array();
	  foreach($all_objects as $cur_object){
        if(!isset($cur_object->attr[$attribute])){ continue; }
        if($cur_object->attr[$attribute] == $value){
          array_push($all_return, $cur_object);
		}
	  }
	  return($all_return);
	}
	
  }

?>