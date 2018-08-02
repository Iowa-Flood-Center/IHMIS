<?php

  namespace Results;
  
  use Results\MetaFile as MetaFile;
  
  class Menu extends MetaFile{
    
    const ROOT_ATTR = "web_menu";            // must-have
    const SUB_META_FOLDER_NAME = "sc_menu";  // must-have
    const FILE_BASENAME = "Menu";
    
    /**
     *
     */
	/*
    public static function get($runset_id){

      // basic check
      if(!isset(MetaFile::$app)) return(array("Error" => "No app set."));
      
      // define file path
      $folder_path = MetaFile::get_folder_path($runset_id, Menu::SUB_META_FOLDER_NAME);
      $file_name = Menu::FILE_BASENAME . MetaFile::FILE_EXT;
      $file_path = $folder_path . $file_name;
      
	  // basic check
	  if (!file_exists($file_path)) return(array("Error" => "No file found!!!"));
	  
	  echo("**".$file_path."**");
	  
      // read file content
      return(Menu::from_file($file_path));
    }
	*/

  }

?>