<?php

  namespace Results;
  use Exception;
  use Results\DataSource;
  require_once '../../common/libs/data_access.php';
  
  class RunsetResult{
    
	const REALTIME_RUNSET_ID = "realtime"; // TODO - send to the config.
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

	  if (DataSource::isSourceLocalFilePath(self::$app)){
        // case 1: from local file system
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
	  } elseif(DataSource::isSourceRemoteFilePath(self::$app)) {
        $all_return = array();
        $all_runset_ids = \DataAccess::list_rootfolder_content("\/");
        $fi_path = "sc_runset/Runset.json";
        foreach($all_runset_ids as $cur_runset_id){
          $fi_ctt=\DataAccess::get_metafile_content($fi_path, $cur_runset_id);
		  $fi_obj = RunsetResult::fromFileContent($fi_ctt);
          array_push($all_return, $fi_obj);
        }
      } else {
        $all_return = array();
		$all_return["ERROR"] = "Not a source of data available.";
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
    
    /**
     * Save current object into the file system path
     */
    public static function create($attributes){
      $runset_id = $attributes['id'];
      $folder_path = self::$app->fss->runsets_result_folder_path;
      $new_path = $folder_path . $runset_id;
      $made = mkdir($new_path);
      if ($made){
        $old = umask(0); 
        chmod($new_path, 0777);
        umask($old);
      }
      return($made);
    }
    
    /**
     * Save realtime status as an snapshot
	 * $attributes: Dictionary with 
     */
    public static function saveRealtimeSnapshot($attributes){
      
      $runset_id = $attributes['id'];
	  $root_l_folder_path = self::$app->fss->runsets_result_folder_path;
	  $root_t_folder_path = self::$app->fss->runsets_result_target_folder_path;
	  
	  // define folders
	  $source_folder_path = $root_t_folder_path.self::REALTIME_RUNSET_ID;
      $destin_folder_path = $root_l_folder_path.$runset_id;
	  
	  /*
	  // check if destination folder already exists
      if (file_exists($destin_folder_path))
        exec("rm -r ".$destin_folder_path);
	    // throw new Exception('Folder '.$destin_folder_path.' already exists.');
		// throw new Exception('Runset '.$runset_id.' already exists.');
	  
	  // copy entire folder
	  exec("cp -r ".$source_folder_path." ".$destin_folder_path);
	  */
	  exec("chmod -R ugo+wrx ".$destin_folder_path);
	  
	  //echo("Copyied '".$source_folder_path."' to '".$destin_folder_path."'.");
	  
	  // read, change and save runset file content
	  $destin_runset_file_path = $root_t_folder_path.$runset_id;
	  $destin_runset_file_path .= RunsetResult::SUB_FILE_PATH;
	  $json_content = json_decode(file_get_contents($destin_runset_file_path));
	  $json_content->sc_runset->id = $runset_id;
	  $json_content->sc_runset->title = $attributes['name'];
	  $json_content->sc_runset->description = $attributes['about'];
	  $json_content->sc_runset->timestamp_ini = $attributes['timestamp_ini'];
	  $json_content->sc_runset->timestamp_end = $attributes['timestamp_end'];
	  $json_content = json_encode($json_content);
	  $written = @file_put_contents($destin_runset_file_path, $json_content);
	  if(!$written)
        throw new Exception("Unable to write file '$destin_runset_file_path'.");

	  return(true);
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
     * Builds an RunsetResult from a filepath
     */
    public static function fromFile($file_path){
      if(!file_exists($file_path)){return(null);}
      return(RunsetResult::fromFileContent(file_get_contents($file_path)));
    }
	
	/**
	 *
	 */
	public static function fromFileContent($file_content){
      $return_obj = new self();
      $return_obj->attr = json_decode($file_content);
      $root_attr = self::ROOT_ATTR;
      $return_obj->attr = get_object_vars($return_obj->attr->$root_attr);
      if (!array_key_exists("show_main", $return_obj->attr)){
        $return_obj->attr['show_main'] = "T";
      }
      return($return_obj);
	}
    
    /**
     * Select a single Runset Result based on a given attribute
     */
    public static function where($attribute, $value){      
      $all_objects = self::all();
      $all_return = array();
      foreach($all_objects as $cur_object){
        if(!isset($cur_object->attr[$attribute])){ continue; }
        if($cur_object->attr[$attribute] == $value){
          $cur_object->fill_object();
          array_push($all_return, $cur_object);
        }
      }
      return($all_return);
    }
  
    /**
     * Select all Runsets that represents the same time interval than another one
     */
    public static function concurrentlyTo($runset_id){
      $TIME_INI = "timestamp_ini";
      $TIME_END = "timestamp_end";
      
      // retrieve initial and final timestamps
      $reference_runset = RunsetResult::where("id", $runset_id);
      if(count($reference_runset) == 0) return(array());
      $timestamp_ini = $reference_runset[0]->attr[$TIME_INI];
      $timestamp_end = $reference_runset[0]->attr[$TIME_END];
    
      // select other equivalent runsets
      $all_objects = self::all();
      $all_return = array();
      foreach($all_objects as $cur_object){
        if(!isset($cur_object->attr[$TIME_INI])){ continue; }
        if(!isset($cur_object->attr[$TIME_END])){ continue; }
        if($cur_object->attr["id"] == $runset_id){ continue; }
        if (($cur_object->attr[$TIME_INI] == $timestamp_ini) && 
            ($cur_object->attr[$TIME_END] == $timestamp_end)){
          $cur_object->fill_object();
          array_push($all_return, $cur_object);
        }
      }
      return($all_return);
    }
  
    // ///////////////////// SPECIFIC //////////////////// //
  
    /**
     * 
     * $scopes : Array of strings. Expected values like 'main', 'sandbox'
     * RETURN : TRUE if able to update, FALSE otherwise
     */
    public function show_main($scopes){
      // basic check
      if(!is_array($scopes)) return(false);
      
      if (($this->attr['show_main'] == "T")||(is_null($this->attr['show_main']))){
        $this->attr['show_main'] = array("main", "sandbox");
      }
      
      $this->attr['show_main'] = array_merge($this->attr['show_main'], 
                                             $scopes);
      $this->attr['show_main'] = array_unique($this->attr['show_main']);
      $this->update_runset_file();
    }
    
    /**
     * 
     * $scopes : Array of strings. Expected values like 'main', 'sandbox'
     */
    public function hide_main($scopes){
      // basic check
      if(!is_array($scopes)) return(false);
      
      if ($this->attr['show_main'] == "T"){
        $this->attr['show_main'] = array("main", "sandbox");
      }
      
      $this->attr['show_main'] = array_diff($this->attr['show_main'],
                                            $scopes);
      $this->update_runset_file();
    }
  
    /**
     * Fill the content of the object
     */
    private function fill_object(){
      error_reporting(E_ALL);
      ini_set('display_errors', 1);

      $runset_id = $this->attr['id'];
    
      // read sc_models
      ModelResult::setApp(RunsetResult::$app);
      $this->attr['sc_model'] = ModelResult::all($runset_id);
    
      // read sc_references
      ReferenceResult::setApp(RunsetResult::$app);
      $this->attr['sc_reference'] = ReferenceResult::all($runset_id);
    
      // read sc_evaluation
      MetaFile::set_app(RunsetResult::$app);
      $this->attr['sc_representation'] = RepresentationResult::all($runset_id);
      $this->attr['sc_model_combination'] = ModelCombinationResult::all($runset_id);
      $this->attr['sc_evaluation'] = EvaluationResult::all($runset_id);
      $this->attr['forecast_set'] = ForecastSet::get_base($runset_id);
      $this->attr['comp_mtx'] = ComparisonResult::get_base($runset_id);
      $this->attr['web_menu'] = Menu::get_base($runset_id);
    }
    
    /**
     * 
     */
    private function update_runset_file(){
      
      // filter data
      $new_obj = array();
      $copied_keys = array("id", "title", "description", "timestamp_ini", 
                           "timestamp_end", "show_main");
      foreach($copied_keys as $cur_key){
        if(array_key_exists($cur_key, $this->attr)){
          $new_obj[$cur_key] = $this->attr[$cur_key];
        }
      }
      $new_obj = array("sc_runset" => $new_obj);
      $out_json = json_encode($new_obj, JSON_PRETTY_PRINT);
      
      // define main file
      $out_path = self::$app->fss->runsets_result_folder_path;
      $out_path .= $this->attr['id'] . RunsetResult::SUB_FILE_PATH;
      
      // write it
      file_put_contents($out_path, $out_json);
    }
  }

?>