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
      $return_obj = new self();
      $return_obj->attr = json_decode(file_get_contents($file_path));
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
     * Fill the content of the object
     */
    private function fill_object(){
      error_reporting(E_ALL);
      ini_set('display_errors', 1);
    
      // read sc_models
      ModelResult::setApp(RunsetResult::$app);
      $this->attr['sc_model'] = ModelResult::all($this->attr['id']);
    
      // read sc_model_combinations
      $this->attr['sc_model_combination'] = array("TODO"=>"TODO");
    
      // read sc_references
      ReferenceResult::setApp(RunsetResult::$app);
      $this->attr['sc_reference'] = ReferenceResult::all($this->attr['id']);
    
      $this->attr['sc_evaluation'] = array("TODO"=>"TODO");
      $this->attr['comp_mtx'] = array("TODO"=>"TODO");
      $this->attr['web_menu'] = array("TODO"=>"TODO");
    }

  }

?>