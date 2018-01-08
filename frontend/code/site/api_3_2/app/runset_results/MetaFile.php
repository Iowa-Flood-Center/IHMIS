<?php

  namespace Results;
  
  class MetaFile{
      
      public $attr;
      protected static $app;
      
      const META_ROOT_FOLDER_NAME = "metafiles";
      const FILE_EXT = ".json";
      
      const ROOT_ATTR = null;             // must be overwrite
      const SUB_META_FOLDER_NAME = null;  // must be overwrite
      
    /**
     * Defines app attribute
     */
    public static function set_app($app) { 
      self::$app = $app;
    }
    
    /**
     *
     * RETURN : String. Absolute file path for folder.
     */
    protected static function get_folder_path($runset_id, $sub_folder_name = null){
      $folder_path = self::$app->fss->runsets_result_folder_path;
      $folder_path .= $runset_id . DIRECTORY_SEPARATOR;
      $folder_path .= MetaFile::META_ROOT_FOLDER_NAME . DIRECTORY_SEPARATOR;
      if (!is_null($sub_folder_name)){
        $folder_path .= $sub_folder_name . DIRECTORY_SEPARATOR;
      }
      return($folder_path);
    }
    
    /**
     * Gets unique file for a Runset
     */
    public static function get_base($runset_id){

      // basic check
      if(is_null(static::FILE_BASENAME)){
        // echo("** not set root **");
        return(null);
      }
    
      // basic check
      if(!isset(MetaFile::$app)) return(array("Error" => "No app set."));
      
      // define file path
      $folder_path = MetaFile::get_folder_path($runset_id, static::SUB_META_FOLDER_NAME);
      $file_name = static::FILE_BASENAME . MetaFile::FILE_EXT;
      $file_path = $folder_path . $file_name;
      
      // basic check
      if (!file_exists($file_path)) return(array("Error" => "No file found."));
      
      // read file content
      return(static::from_file($file_path));
    }
    
    /**
     *
     * RETURN : Object of the child type.
     */
    public static function from_file($file_path){
      // basic check
      if(is_null(static::ROOT_ATTR)){
        // echo("** not set root **");
        return(null);
      }
      
      // basic check
      if(!file_exists($file_path)){
        // echo("** not found ".$file_path." **");
        return(null);
      }
      
      // read content
      $return_obj = new static();
      $return_obj->attr = json_decode(file_get_contents($file_path));
      $root_attr = static::ROOT_ATTR;
      $return_obj = get_object_vars($return_obj->attr->$root_attr);
      return($return_obj);
    }
  }

?>