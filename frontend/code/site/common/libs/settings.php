<?php

  class Settings{
    private static $settings = null;
	const LOG_EXT = ".log";
	
	/**
	 * Gets date time used in log file names
	 * Return: String in format YYYY_MMDD_HHmm
	 */
    public static function get_datelog(){
      return(date("Y_md_Hi"));
    }
  
    /**
	 * Gets base folder path for configuration files
	 */
    public static function get_conf_folder_path(){
      $working_dir = getcwd();
      $slash = DIRECTORY_SEPARATOR;
      $pattern = "#frontend".$slash."code".$slash.".*$#";
      $replace = "frontend".$slash."conf".$slash;
      $file_path = preg_replace($pattern, $replace, getcwd());
      return($file_path);
	}
	
	/**
	 * Reads settings file content and store within internal variable
	 */
	public static function load_settings(){
      $fpath = Settings::get_conf_folder_path();
	  $fpath .= "common".DIRECTORY_SEPARATOR;
	  $fpath .= "settings.json";
	  $json = file_get_contents($fpath);
	  Settings::$settings = json_decode($json, TRUE);
	}
	
	/**
	 * Retrieve key info '$property' from settings file
	 */
	public static function get_property($property){
      if(is_null(Settings::$settings)) Settings::load_settings();
	  return(Settings::$settings[$property]);
	}
	
	/**
	 * An alias for Settings::get_property('raw_data_folder_path')
	 */
	public static function get_raw_folder_path(){
		if(is_null(Settings::$settings)) Settings::load_settings();
		return(Settings::$settings['raw_data_folder_path']);
	}
	
	/**
	 * 
	 * $folder_hierarchy : Array of strings
	 * Return: String for log file
	 */
	public static function get_log_file_path($folder_hierarchy=null){
      $file_path = Settings::get_raw_folder_path();
	  $file_path .= "logs".DIRECTORY_SEPARATOR;
	  $file_path .= Settings::$settings['logs_subfolder'];
	  $datelog = Settings::get_datelog();
	  if(!is_null(($folder_hierarchy))){
	    $file_path .= implode(DIRECTORY_SEPARATOR, $folder_hierarchy);
		$file_path .= DIRECTORY_SEPARATOR;
		$file_path .= end($folder_hierarchy)."_".$datelog.Settings::LOG_EXT;
      } else
        $file_path .= $datelog.Settings::LOG_EXT;
	  return($file_path);
	}
	 
	/**
	 * Write into the end of the log file
	 */
	public static function write_log($text, $log_file_path){
	  // create folder if needed
	  $dir_name = dirname($log_file_path);
	  if(!file_exists($dir_name)){
		$oldmask = umask(0);
		try{
          mkdir($dir_name, 0777, true);
		} catch (Exception $e) {
          //echo('Caught exception: '.$e->getMessage()."\n");
        }
		umask($oldmask);
	  }
	  
	  // write content
	  $oldmask = umask(0);
      file_put_contents($log_file_path, $text, FILE_APPEND);
	  umask($oldmask);
    }
	
    /**
     * Write into the end of the log file and creates a new line
     */
	public static function write_log_ln($text, $log_file_path){
      $wtext = (substr($text, -1) == "\n") ? $text : $text."\n";
      static::write_log($wtext, $log_file_path);
	}
  }
?>
