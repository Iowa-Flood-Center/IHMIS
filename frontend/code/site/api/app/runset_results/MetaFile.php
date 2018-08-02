<?php

  namespace Results;
  
  use Results\DataSource;
  require_once '../../common/libs/data_access.php';
  
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
      if (DataSource::isSourceLocalFilePath(self::$app)){
        $folder_path = self::$app->fss->runsets_result_folder_path;
        $folder_path .= $runset_id . DIRECTORY_SEPARATOR;
        $folder_path .= MetaFile::META_ROOT_FOLDER_NAME . DIRECTORY_SEPARATOR;
        if (!is_null($sub_folder_name)){
          $folder_path .= $sub_folder_name . DIRECTORY_SEPARATOR;
        }
      } elseif(DataSource::isSourceRemoteFilePath(self::$app)) {
		$folder_path = "";
      } else {
        $folder_path = null;
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
      
	  if (DataSource::isSourceLocalFilePath(self::$app)){
        // define file path
        $folder_path = MetaFile::get_folder_path($runset_id, static::SUB_META_FOLDER_NAME);
        $file_name = static::FILE_BASENAME . MetaFile::FILE_EXT;
        $file_path = $folder_path . $file_name;
      
        // basic check
        if (!file_exists($file_path)) return(array("Error" => "No local file found!"));
      
        // read file content
		$file_obj = static::from_file($file_path);
      } elseif (DataSource::isSourceRemoteFilePath(self::$app)) {

        $file_name = static::FILE_BASENAME . MetaFile::FILE_EXT;
        $file_sub_path = static::SUB_META_FOLDER_NAME . "/" . $file_name;

        if (! \DataAccess::check_metafile_exists($file_sub_path, $runset_id)){
          return(array("Error" => "No remote file found: '".$file_sub_path."'!"));
        }
        
        $file_ctt = \DataAccess::get_metafile_content($file_sub_path, $runset_id);
		$file_obj = static::from_file_content($file_ctt);

	  } else {
        $file_obj = null;
	  }
	  
      return($file_obj);
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
      return(static::from_file_content(file_get_contents($file_path)));
    }
	
	public static function from_file_content($file_content){
      $return_obj = new static();
      $return_obj->attr = json_decode($file_content);
      $root_attr = static::ROOT_ATTR;
      $return_obj = get_object_vars($return_obj->attr->$root_attr);
      return($return_obj);
	}
  }

?>