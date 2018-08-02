<?php

  namespace Requester;

  use Requester\MetaFilesCreator as MetaFilesCreator;
  use Requester\AuxFilesLib as AuxFilesLib;
  
  // 
  class RunsetRequest{
    public $is_sandbox;              //
    public $runset_id;               // 
    public $runset_title;            //
    public $timestamp_ini;           //
    public $timestamp_end;           //
    public $user_email;              //
	public $contact_option;          //
    public $current_timestamp;       //
    public $asynch_version;          //
    public $server_addr;             //
    public $max_models;              //
    public $what_run;                //
    public $model_requests;          //
    public $globalfile_requests;     //
    public $modelcombmaps;           //
    public $modelcomb_requests;      //
    
    const WAITING_RUN_FILE_EXT = ".tar.gz";
    
    /**
     * Construct function
     */
    function __construct($posts){
      try{
        $this->is_sandbox = $posts["sandbox"];
        $this->current_timestamp = time();
        $this->runset_id = $posts["runset_id"];
        $this->runset_title = $posts["runset_title"];
        $this->timestamp_ini = $posts["timestamp_ini"];
        $this->timestamp_end = $posts["timestamp_end"];
        $this->user_email = $posts["email"];
		$this->contact_option = $posts["contact_option"];
		$this->contact_option = str_replace("how_contact_", "", $this->contact_option);
        $this->max_models = $posts["num_models"];
        $this->what_run = $posts["what_run"];
        $this->what_do = $posts["what_do"];
        $this->asynch_version = $posts["asynch_ver"];
        $this->server_addr = $posts["server_addr"];
        $this->model_requests = null;
        $this->globalfile_requests = null;
        $this->modelcomb_requests = null;
      } catch(Exception $exp) {
        echo("Exception: ".$exp);
        exit();
      }
    }
    
    /**
     * Single function that calls all the others
     * RETURN :
     */
    public function create_all_meta_files($app){
      $this->create_local_temp_dirs();
      $this->create_runset_meta_file($app);
      $this->create_global_files($app);
      $this->create_modelcomb_files($this->current_timestamp);
      // MetaFilesCreator::create_comparison_mtx_meta_json_file($runset_obj, $mdlreq_objs);
      $this->create_comparison_mtx_empty_meta_file($app);
      // MetaFilesCreator::create_evaluation_mtx_meta_json_file($runset_obj, $mdlreq_objs);
      // $this->create_evaluation_mtx_empty_meta_file($app);
      $this->create_evaluation_mtx_meta_file($app);
      MetaFilesCreator::create_email_text_file($this, $this->contact_option);
      MetaFilesCreator::create_metacomb_hydrographpast($this, $this->model_requests);
      MetaFilesCreator::create_metacomb_sequencemaps($this);
	  $this->send_creation_email();
    }
	
	/**
	 * $email_addr : 
	 * $contact_opt : 
	 */
	public function send_creation_email(){
		if($this->contact_option != "all") return;
		mail($this->user_email, "Runset submitted.", "Runset '".$this->runset_title."' (id: ".$this->runset_id.") submitted.");
	}
    
    /**
     *
     * $app:
     * RETURN:
     */
    public function compact_all_metafiles(){
      // compact file
      $tar_fpath = AuxFilesLib::get_local_temp_targz_file_path($this->current_timestamp);
      $the_cmd = "cd /tmp/ && tar -czvf ";
      $the_cmd .= $tar_fpath." ";
      $the_cmd .= $this->current_timestamp."/*";
      exec($the_cmd, $retval);
      
      return($retval);
    }
    
    /**
     *
     *
       */
    public function schedule_files_deletion($delta_minutes){
      // date_default_timezone_set('America/Chicago');
      $delete_timestamp = $this->current_timestamp + ($delta_minutes * 60);
      $minutes = date('i', $delete_timestamp);
      $hours = date('G', $delete_timestamp);
      $day = date('j', $delete_timestamp);
      
      $targz_file_path = AuxFilesLib::get_local_temp_targz_file_path($this->current_timestamp);
      $temp_folder_path = AuxFilesLib::get_local_temp_folder_path($this->current_timestamp);
      
      $cmd01 = "echo \"".$minutes." ".$hours." ".$day." * * rm ".$targz_file_path."\"";
      $cmd02 = "echo \"".$minutes." ".$hours." ".$day." * * rm -r ".$temp_folder_path."\"";
      
      // echo("Deleting '".$targz_file_path."' and '".$temp_folder_path." -r'. ");
      
      shell_exec("crontab -r");
      shell_exec("crontab -l | { cat; ".$cmd01."; } | crontab -");
      shell_exec("crontab -l | { cat; ".$cmd02."; } | crontab -");
    }
    
    /**
     *
     */
    public function dispatch() {
      $return_array = array();
      
      // "don't dispatch" cases
      if((strpos($this->what_run, 'onlygen') !== false)||($this->what_do == 'genonly')){
        $return_array["Dispatched"] = false;
        return($return_array);
      }
      
      // dispatch to waiting room
      if((strpos($this->what_run, 'loginless') !== false)||($this->what_do == 'genrun')){
        // define destination, copy and change permissions
        $runset_waitingroom_targz_file_path = AuxFilesLib::get_local_runset_waitingroom_targz_file_path($this->current_timestamp);
        exec("cp ".AuxFilesLib::get_local_temp_targz_file_path($this->current_timestamp)." ".$runset_waitingroom_targz_file_path);
        exec("chmod ugo+rwx ".$runset_waitingroom_targz_file_path);
        
        $return_array["Dispatched"] = true;
        $return_array["FilePath"] = $runset_waitingroom_targz_file_path;
        return($return_array);
      }
      
      $return_array["Dispatched"] = false;
      $return_array["Exception"] = "Unexpected what_run value: '".$this->what_run."'.";
      return($return_array);
    }
    
    /**
     *
     * RETURN :
     */
    public function create_global_files($app){
      // prepare receiving lists
      $files_to_sent = array();
      $all_model_ids = array();
      $all_model_hlm = array();
      
      // iterates over each model creating its global files objects
      $all_global_files = array();
	  \Settings::write_log_ln("Processing ".sizeof($this->model_requests)." models.", $app->log->file_path);
	  
      foreach($this->model_requests as $cur_model_request){
        $cur_global_files = $cur_model_request->createGlobalFileRequests($this, $app);
        foreach($cur_global_files as $cur_global_file){
          array_push($all_global_files, $cur_global_file);
        }
      }
      
      // create the global files
	  \Settings::write_log_ln("Creating ".sizeof($all_global_files)." global files.", $app->log->file_path);
      foreach($all_global_files as $cur_global_file){
        $cur_global_file->create_files($this, $app);
      }
      
      // add globalfile resquests to the runset object
      $this->globalfile_requests = $all_global_files;
      
      // create central job file
	  \Settings::write_log_ln("Creating central job file.", $app->log->file_path);
      $this->create_central_job_file($app);
    }
    
    /**
     *
     * RETURN :
     */
    public function create_modelcomb_files($cur_timestamp){
      if(!is_null($this->modelcomb_requests) ){ 
        foreach($this->modelcomb_requests as $cur_modelcomb_req){
          $cur_modelcomb_req->create_file($cur_timestamp);
        }
      }
    }
    
    /**
     *
     * RETURN :
     */
    public function create_runset_meta_file($app){
      $json_final_filepath = AuxFilesLib::get_local_metarunset_file_path($this->current_timestamp);
    
      // read template file and separates main line
      $json_final_content = file($app->fss->metarunset_template_filepath);
      $json_final_content[1] = str_replace("RUNSET_ID",
                         $this->runset_id,
                         $json_final_content[1]);
      $json_final_content[2] = str_replace("RUNSET_TITLE", 
                         $this->runset_title, 
                         $json_final_content[2]);
      $json_final_content[3] = str_replace("\"TIMESTAMP_MIN\"", 
                         $this->timestamp_ini,
                         $json_final_content[3]);
      $json_final_content[4] = str_replace("\"TIMESTAMP_MAX\"", 
                         $this->timestamp_end, 
                         $json_final_content[4]);
    
      // write all internal lines
      $fp = fopen($json_final_filepath, 'w');
      foreach ($json_final_content as $value){
        fwrite($fp, $value);
      }
      fclose($fp);
    }
    
    /**
     * Creates temporary folder for the submission or clean it if it already exists.
     * $currtent_time :
     * RETURN :
     */
    public function create_local_temp_dirs(){
      $current_time = $this->current_timestamp;
      $local_folder_path = AuxFilesLib::get_local_temp_folder_path($current_time);
      if (!file_exists($local_folder_path)) {
        mkdir($local_folder_path, 0777, true);  // root folder
        mkdir(AuxFilesLib::get_local_temp_meta_folder_path($current_time));
        mkdir(AuxFilesLib::get_local_temp_meta_folder_path($current_time, 'models'));
        mkdir(AuxFilesLib::get_local_temp_meta_folder_path($current_time, 'matrices'));
        mkdir(AuxFilesLib::get_local_temp_meta_folder_path($current_time, 'modelcomb'));
        mkdir(AuxFilesLib::get_local_temp_meta_folder_path($current_time, 'runset'));
        mkdir(AuxFilesLib::get_local_temp_output_snapshot_folder_path($current_time), 0777, true);
      } else {
        chmod($local_folder_path, 0777);
        array_map('unlink', glob($local_folder_path."*"));
      }
      return($local_folder_path);
    }
    
    /**
     *
     * $all_global_file_paths :
     * RETURN :
     */
    // private function create_central_job_file($all_global_file_paths, $app){
    private function create_central_job_file($app){
      // define job file path
      $job_final_filepath = AuxFilesLib::get_local_temp_folder_path($this->current_timestamp);
      $job_final_filepath .= $this->runset_id.".job";
      
      // define server's ASYNCH binary file location and the number of cores
      $job_cpn = AuxFilesLib::get_cpn($this->server_addr);
      $job_noc = AuxFilesLib::get_noc($this->server_addr);
      // $asynch_call = AuxFilesLib::get_asynch_bin_path($this->server_addr, $this->asynch_version);
      
      // debug
      // echo("Got '".$job_cpn."' and '".$job_noc."' from '".$this->server_addr."'. ");
      
      // read template file and edits its content
      $job_final_content = file($app->fss->job_template_filepath);
      $job_final_content[1] = "#$ -N ".$this->runset_id."\n";                                                 // replace run id
      $job_final_content[2] = "#$ -o ".$app->fss->dest_folder_path;
      $job_final_content[2] .= $this->current_timestamp."/".$this->runset_id."_o.txt\n";                      // replace output log file name
      $job_final_content[3] = "#$ -e ".$app->fss->dest_folder_path;                                           // replace error log file name
      $job_final_content[3] .= $this->current_timestamp."/".$this->runset_id."_e.txt\n";
      $job_final_content[4] = "#$ -pe ".$job_cpn." ".$job_noc."\n";      
      if (trim($this->user_email) != ""){
        $job_final_content[5] = "#$ -m bea\n";                                                              // replace something here
        $job_final_content[6] = "#$ -M ".$this->user_email."\n";                                            // replace contact email
      } else {
        $job_final_content[5] = "\n";                                                                       // replace something here
        $job_final_content[6] = "\n";                                                                       // replace contact email
      }
      $job_final_content[7] = "#$ -q ".AuxFilesLib::get_queue($this->server_addr)."\n";                       // replace server queue
      
      // replace modules import
      // $job_final_content[9] = AuxFilesLib::get_job_modules($this->server_addr);
      
      // add as many calls as apparently necessary
      $folder_path = AuxFilesLib::get_remote_folder_path($this->current_timestamp);
      $all_calls = "";
      $all_deps = array();
	  if (!is_null($this->globalfile_requests)){
        foreach($this->globalfile_requests as $cur_global_file_request){
        
          $call_dep = AuxFilesLib::get_hydrologicalmodel_path_and_dependencies($cur_global_file_request->hillslope_model_id);
        
          $all_deps = array_merge($all_deps, $call_dep['dependencies']);
        
          $asynch_call = $call_dep['path'];
          $all_calls .= "mpirun -np ".$job_noc." ".$asynch_call." ";
          $all_calls .= $folder_path.basename($cur_global_file_request->glb_remote_file_path."\n");
        }
	  }
      
      $job_final_content[9] = implode("\n", array_unique($all_deps))."\n";
      
      $job_final_content[11] = $all_calls;
      
      $job_final_content[13] = str_replace("<DEST_FOLDER_PATH>", 
                                           $app->fss->dest_folder_path, 
                         $job_final_content[13]);
      
      // save edited template into file
      $fp = fopen($job_final_filepath, 'w');
      foreach ($job_final_content as $cur_job_final_line){
        fwrite($fp, $cur_job_final_line);
      }
      fclose($fp);
	  \Settings::write_log_ln("Wrote file '".$job_final_filepath."'.",
	                          $app->log->file_path);
      
      // just return
      return($job_final_filepath);
    }
    
    /**
     * Used as a "gap filling" piece of code, replacement for 'create_comparison_mtx_meta_file()' function.
     * RETURN : none
     */
    public function create_comparison_mtx_empty_meta_file($app){
      
      // defines final file path
      $json_final_filepath = AuxFilesLib::get_local_metacomparisonmtx_file_path($this->current_timestamp);
      
      // read template file and make empty comparisons
      $json_final_content = file($app->fss->metacomparison_template_filepath);
      
      $json_final_content[1] = "";
      
      // write all internal lines
      $fp = fopen($json_final_filepath, 'w');
      foreach ($json_final_content as $value){
        fwrite($fp, $value);
      }
      fclose($fp);
    }
    
    /**
     *
     * RETURN :
     */
    public function create_evaluation_mtx_meta_file($app){
      if(false){
        $this->create_evaluation_mtx_empty_meta_file($app);
      } else {
        $this->create_evaluation_mtx_filled_meta_file($app);
      }
    }
    
    /**
     * Used as a "gap filling" piece of code, replacement for 'create_evaluation_mtx_meta_file()' function.
     * RETURN : none
     */
    public function create_evaluation_mtx_empty_meta_file($app){
      
      // defines final file path
      $json_final_filepath = AuxFilesLib::get_local_metaevaluationmtx_file_path($this->current_timestamp);
    
      $json_final_content = file($app->fss->metaevaluation_template_filepath);
      $json_final_content[1] = "";
      
      // write all internal lines
      $fp = fopen($json_final_filepath, 'w');
      foreach ($json_final_content as $key => $value){
        fwrite($fp, $value);
      }
      fclose($fp);
	  
      return;
    }
    
    /**
     *
     * RETURN :
     */
    public function create_evaluation_mtx_filled_meta_file($app){
      // defines final file path
      $json_final_filepath = AuxFilesLib::get_local_metaevaluationmtx_file_path($this->current_timestamp);
    
      // read template file and make empty evaluations
	  $json_final_content = file($app->fss->metaevaluation_template_filepath);
	  $line_template = $json_final_content[1];
	  
	  // build intermediary inner matrix
      $all_evaluations = [];
	  foreach($this->model_requests as $cur_model_request){
		  if (is_null($cur_model_request->evaluations)) continue;
		  foreach($cur_model_request->evaluations as $cur_evaluation){
			  if (!array_key_exists($cur_evaluation, $all_evaluations)){
				  $all_evaluations[$cur_evaluation] = [];
			  }
			  array_push($all_evaluations[$cur_evaluation], 
			             $cur_model_request->model_id);
		  }
      }
	  
	  // create inner lines
	  $all_lines = [];
	  foreach ($all_evaluations as $cur_evaluation => $cur_models){
		  $cur_line = str_replace('EVALUATIONID_REFERENCEID', $cur_evaluation, $line_template);
		  $cur_line = str_replace('SC_MODEL_IDS', json_encode($cur_models), $cur_line);
		  // $cur_line = str_replace("\n", "", $cur_line);
		  $cur_line = preg_replace('/\s\s+/', ' ', $cur_line);
		  array_push($all_lines, $cur_line);
      }
	  
	  // replace it
      $json_final_content[1] = implode(",\n", $all_lines)."\n";
      
      // write all internal lines
      $fp = fopen($json_final_filepath, 'w');
      foreach ($json_final_content as $key => $value){
        fwrite($fp, $value);
      }
      fclose($fp);
	  
      return;
    }
    
    /**
     * Gets all RunsetRequests in the Waiting Room
     * $app :
     * RETURN : Array of Strings. All file names in Waiting Room.
     */
    public static function in_waiting_room($app){
      $waitingroom_folder_path = $app->fss->waiting_room_folder_path;
      
      $all_files = scandir($waitingroom_folder_path);
      $all_targz_files = array();
      foreach($all_files as $cur_file){
        if (!RunsetRequest::endsWith($cur_file, 
                            RunsetRequest::WAITING_RUN_FILE_EXT)) {
          continue;
        }
        $all_targz_files[] = $cur_file;
      }

      return($all_targz_files);
    }
    
    /**
     * 
     * $app :
     * $runset_request :
     * RETURN : Boolean. True if able to delete file, False otherwise.
     */
    public static function delete_from_waiting_room($app, 
                                                    $runset_request){
      
      // builds filepath
      if(RunsetRequest::endsWith($runset_request, 
                                 RunsetRequest::WAITING_RUN_FILE_EXT)){
        $file_name = $runset_request;
      } else {
        $file_name = $runset_request.RunsetRequest::WAITING_RUN_FILE_EXT;
      }
      
      // if file exists, delete it
      $file_path = $app->fss->waiting_room_folder_path.$file_name;
      if(!file_exists($file_path)){ return(false);}
        
      return(unlink($file_path)); 
    }
    
    /**
     * 
     * TODO - move to some 'utils' library
     * $str :
     * $sub :
     * RETURN :
     */
    private static function endsWith($str, $sub) {
      return (substr($str, strlen($str) - strlen($sub)) === $sub);
    }
    
  }

?>
