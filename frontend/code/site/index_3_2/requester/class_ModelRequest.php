<?php
	include_once("class_AuxFiles.php");
	include_once("../common/class_FoldersDefs.php");

	//
	class GlobalFileRequest{
		
		const snapshot_save_none = 0;
		const snapshot_save_all = 1;
		const snapshot_save_last = 2;
		
		public $runset_id;               // string:
		public $model_id;                // string:
		public $model_title;             // string: null (if not to generate metafile)
		public $model_desc;              // string: null (if not to generate metafile)
		public $parameter_set;           // [string]: 
		public $hillslope_model_id;      // integer:
		public $precip_source_id;        // integer:
		public $reservoir_include;       // boolean:
		public $timestamp_cur;           // integer: timestamp in seconds
		public $timestamp_ini;           // integer: timestamp in seconds
		public $timestamp_end;           // integer: timestamp in seconds
		public $initcond_source;         // string: a model id (model output) or null (repository)
		public $show_main;               // boolean: True if the model is expected to be shown in the main menu, False otherwise.
		public $snapshot_save;           // integer: GlobalFileRequest::snapshot_save_* expected
		
		/**
		 *
		 * RETURN :
		 */
		public function get_show_main_string(){
			return( ($this->show_main ? "true" : "false"));
		}
		
		/**
		 *
		 *
		 * RETURN :
		 */
		public function set_snapshot_save($new_snapshot_save){
			$this->snapshot_save = $new_snapshot_save;
		}
		
		/**
		 *
		 * $model_request_obj :
		 * RETURN :
		 */
		public function fill_with_model_req($model_request_obj){
			$this->model_id = $model_request_obj->model_id;                         // string  : 
			$this->parameter_set = $model_request_obj->gbl_parameters;              // [string]: 
			$this->hillslope_model_id = $model_request_obj->hillslope_model_id;     // integer : 
			$this->precip_source_id = $model_request_obj->precipitation_source_id;  // integer : 
			$this->reservoir_include = $model_request_obj->reservoir_include;       // boolean : 
		}
		
		/**
		 *
		 * $runset_request_obj :
		 * RETURN :
		 */
		public function fill_with_runset_req($runset_request_obj){
			$this->runset_id = $runset_request_obj->runset_id;
		}
		
		/**
		 * Creates both global, job and meta files
		 * RETURN :
		 */
		public function create_files($runsetRequest){
			
			// TODO - move it into a common place
			$all_asynch_versions = array("1.1", "1.2", "1.3");
			
			// basic check - Asynch version
			if(!in_array($runsetRequest->asynch_version, $all_asynch_versions)){
				echo("Invalid asynch version: '".$runsetRequest->asynch_version."'.");
				return(null);
			}
			
			// basic check - Asynch version
			// TODO - remove it
			/*
			if (($runsetRequest->asynch_version != "1.1")&&($runsetRequest->asynch_version != "1.2")) {
				echo("Invalid asynch version: '".$runsetRequest->asynch_version."'.");
				return(null);
			}
			*/
			
			// create files effectively
			$gbl_file_path = $this->create_gbl_file($runsetRequest);
			$this->create_referenced_files($runsetRequest);
			// $this->create_job_file();
			$this->create_model_meta_file();
			
			// establish final gbl and job files
			$job_final_filepath = AuxFiles::get_local_temp_folder_path($this->timestamp_cur).$this->model_id.".job";
			$json_final_filepath = AuxFiles::get_local_metamodel_file_path($this->timestamp_cur, $this->model_id);
			
			return($gbl_file_path);
		}
		
		/**
		 *
		 * $runset_request_obj : 
		 * RETURN : String - final global file path
		 */
		private function create_gbl_file($runset_request_obj){
			
			$current_timestamp = $runset_request_obj->current_timestamp;
			$asynch_version = $runset_request_obj->asynch_version;
			
			// define gbl file name and path
			$glb_final_filename = $this->model_id.".gbl";
			$glb_final_filepath = AuxFiles::get_local_temp_folder_path($runset_request_obj->current_timestamp);
			$glb_final_filepath .= $glb_final_filename;
			
			// read template file
			$gbl_final_content = file(FoldersDefs::GLB_TEMPLATE_FILEPATH);
			
			// edit template content
			if ($asynch_version == "1.1"){
				$gbl_final_content[1] = $this->hillslope_model_id." ";
				$gbl_final_content[1] .= (($this->timestamp_end - $this->timestamp_ini)/60)."\n";
			} elseif (in_array($asynch_version, array("1.2", "1.3"))) {
				$datetime_ini = date('Y-m-d H:i', $this->timestamp_ini);
				$datetime_end = date('Y-m-d H:i', $this->timestamp_end);
				$gbl_final_content[1] = $this->hillslope_model_id."\n";
				$gbl_final_content[1] .= $datetime_ini."\n";
				$gbl_final_content[1] .= $datetime_end."\n";
			}
			$gbl_final_content[18] = sizeof($this->parameter_set)." ".implode(" ", $this->parameter_set)."\n";       // replace global parameters
			// $gbl_final_content[26] = "1 0 ".AuxFiles::get_remote_topology_file_path($current_timestamp)."\n";        // replace topology source
			$gbl_final_content[29] = "0 ".AuxFiles::get_remote_demparameters_file_path($this->timestamp_cur, 
																					   $this->hillslope_model_id);   // replace DEM parameters
			$gbl_final_content[29] .= "\n";
			$gbl_final_content[33] = "4 ".AuxFiles::get_remote_initcond_mod_file_path($this->timestamp_cur, 
																					  $this->hillslope_model_id, 
																					  $this->timestamp_ini, 
																					  $this->model_id, 
																					  $asynch_version)."\n";
			/*
			$gbl_final_content[40] = "3 ".AuxFiles::get_remote_raindata_file_path($current_timestamp, 
																				  $this->precip_source_id)."\n";     // replace rain source
			$gbl_final_content[41] = AuxFiles::get_raindbc_raininstances($this->precip_source_id)." ";
			$gbl_final_content[41] .= AuxFiles::get_raindbc_raininterval($this->precip_source_id)." ";
			$gbl_final_content[41] .= $this->timestamp_ini." ".$this->timestamp_end."\n";                            // replace rain interval
			*/
			$gbl_final_content[40] = $this->define_precipitation_source_line_1();
			$gbl_final_content[41] = $this->define_precipitation_source_line_2();
			$gbl_final_content[44] = "7 ".AuxFiles::get_remote_evaporation_file_path($this->timestamp_cur)."\n";     // replace evapo-transpiration 
			$gbl_final_content[45] = $this->timestamp_ini." ".AuxFiles::FARAWAY_FUTURE."\n";                         // replace evapo-transpiration interval
			$gbl_final_content[48] = $this->define_reservoir_source_line_1();                                        // replace reservoirs data source
			$gbl_final_content[49] = $this->define_reservoir_source_line_2();                                        // replace reservoirs data interval
			$gbl_final_content[54] = "3 ".AuxFiles::get_remote_qvs_file_path($this->timestamp_cur)."\n";             // replace QVS
			$gbl_final_content[57] = $this->define_reservoir_links_line();                                           // replace reservoirs reference
			if (!is_null($this->initcond_source)) {
				$gbl_final_content[77] = "4 60 ".AuxFiles::get_remote_output_snapshot_file_path($this->model_id, 
																								$this->timestamp_cur, 
																								$this->timestamp_ini,
																								$asynch_version,
																								false)."\n";   // replace output snapshot
			} else {
				$gbl_final_content[77] = "3 ".AuxFiles::get_remote_output_snapshot_file_path($this->model_id, 
																							 $this->timestamp_cur, 
																							 $this->timestamp_end,
																							 $asynch_version,
																							 true)."\n";   // replace output snapshot
			}
			$gbl_final_content[80] = AuxFiles::get_remote_scratch_file_path($this->timestamp_cur)."\n";              // 

			// save edited template into file
			$fp = fopen($glb_final_filepath, 'w');
			foreach ($gbl_final_content as $key => $value){
				fwrite($fp, $value);
			}
			fclose($fp);
			
			// create folder in which output snapshots are going to be stored in the future
			$np = AuxFiles::get_local_temp_output_snapshot_specific_folder_path($this->timestamp_cur, 
																			    $this->model_id);
			mkdir($np, 0777, true);
			
			return($glb_final_filepath);
		}
		
		/**
		 *
		 * $current_timestamp :
		 * $precip_source_id :
		 * RETURN :
		 */
		private function define_precipitation_source_line_1(){
			$ret_str = "";
			if(!is_null($this->precip_source_id)){
				$ret_str .= "3 ".AuxFiles::get_remote_raindata_file_path($this->timestamp_cur, 
																		 $this->precip_source_id)."\n";
			} else {
				$ret_str .= "0 \n";
			}
			return($ret_str);
		}
		
		/**
		 *
		 * RETURN :
		 */
		private function define_precipitation_source_line_2(){
			$ret_str = "";
			if (!is_null($this->precip_source_id)){
				$ret_str .= AuxFiles::get_raindbc_raininstances($this->precip_source_id)." ";
				$ret_str .= AuxFiles::get_raindbc_raininterval($this->precip_source_id)." ";
				$ret_str .= $this->timestamp_ini." ".$this->timestamp_end."\n"; 
			} else {
				$ret_str .= "";
			}
			return($ret_str);
		}
		
		/**
		 *
		 * RETURN :
		 */
		private function define_reservoir_source_line_1(){
			if($this->reservoir_include == 'true'){
				$fiepath = AuxFiles::get_remote_folder_path($this->timestamp_cur);
				$fiepath .= AuxFiles::get_rsvdbc_file_name();
				return("3 ".$fiepath."\n");
			} else {
				return("0\n");
			}
		}
		
		/**
		 *
		 * RETURN :
		 */
		private function define_reservoir_source_line_2(){
			if($this->reservoir_include == 'true'){
				return("1 30 ".$this->timestamp_ini." ".$this->timestamp_end."\n");
			} else {
				return("");
			}
		}
		
		/**
		 *
		 * RETURN :
		 */
		private function define_reservoir_links_line(){
			if ($this->reservoir_include == 'true'){
				$filepath = AuxFiles::get_remote_folder_path($this->timestamp_cur);
				$filepath .= AuxFiles::get_rsv_file_name();
				return("1 ".$filepath." 2\n");
			} else {
				return("0\n");
			}
		}
		
		/**
		 *
		 * $runset_request_obj :
		 * RETURN :
		 */
		private function create_referenced_files($runset_request_obj){
			$current_timestamp = $runset_request_obj->current_timestamp;
			
			AuxFiles::setup_local_temp_topology_file($current_timestamp);
			AuxFiles::setup_local_temp_demparameters_file($current_timestamp, 
														  $this->hillslope_model_id);
			/*
			// TODO - remove this copy of initial condition file
			if (($this->hillslope_model_id) && (is_null($this->initcond_source))){
				echo("Going for '".$current_timestamp."', '".$this->hillslope_model_id."', '".$this->timestamp_ini."'. ");
				AuxFiles::setup_local_temp_initcond_file($current_timestamp, 
														 $this->hillslope_model_id, 
														 $this->timestamp_ini);
			}
			*/
			if (!is_null($this->precip_source_id)){
				AuxFiles::setup_local_temp_raindata_file($current_timestamp, 
														 $this->precip_source_id);
			}
			AuxFiles::setup_local_temp_evaporation_file($current_timestamp);
			AuxFiles::setup_local_temp_qvs_file($current_timestamp);
			
			if ($this->reservoir_include == 'true'){
				AuxFiles::setup_local_temp_reservoir_files($current_timestamp);
			}
		}
		
		/**
		 * 
		 * >-+ IMPORTANT +-< It was just copy-and-pasted. Need to be worked on.
		 * $runset_request_obj : 
		 * RETURN : String - final job file path
		 */
		private function create_job_file(){
			// read template file and edits its content
			$glb_file_path = AuxFiles::get_remote_global_file_path($current_timestamp, $model_id);
			$job_final_content = file(AuxFiles::JOB_TEMPLATE_FILEPATH);
			$job_cpn = AuxFiles::get_cpn($server_addr);
			$job_noc = AuxFiles::get_noc($server_addr);
			$asynch_call = AuxFiles::get_asynch_bin_path($server_addr, $asynch_version);
			$job_final_content[1] = "#$ -N ".$model_id."\n";                                                        // replace run id
			$job_final_content[2] = "#$ -o /Dedicated/IFC/back_time/".$current_timestamp."/".$model_id."_o.txt\n";  // replace output log file name
			$job_final_content[3] = "#$ -e /Dedicated/IFC/back_time/".$current_timestamp."/".$model_id."_e.txt\n";  // replace error log file name
			$job_final_content[4] = "#$ -pe ".$job_cpn." ".$job_noc."\n";                                           // replace number of cores
			if (trim($email) != ""){
				$job_final_content[5] = "#$ -m bea\n";                                                              // replace something here
				$job_final_content[6] = "#$ -M ".$email."\n";                                                       // replace contact email
			} else {
				$job_final_content[5] = "\n";                                                                       // replace something here
				$job_final_content[6] = "\n";                                                                       // replace contact email
			}
			$job_final_content[7] = "#$ -q ".AuxFiles::get_queue($server_addr )."\n";                               // replace server queue
			$job_final_content[13] = "\nmpirun -np ".$job_noc." ".$asynch_call." ".$glb_file_path;                  // replace system call command
			
			// save edited template into file
			$fp = fopen($job_final_filepath, 'w');
			foreach ($job_final_content as $key => $value){
				fwrite($fp, $value);
			}
			fclose($fp);
		}
		
		/**
		 * 
		 * RETURN :
		 */
		private function create_model_meta_file(){
			
			$timestamp_cur = $this->timestamp_cur;
			$model_id = $this->model_id;
			$json_final_filepath = AuxFiles::get_local_metamodel_file_path($timestamp_cur, $model_id);
			
			// read template file and edits its content
			$json_final_content = file(FoldersDefs::METAMODEL_TEMPLATE_FILEPATH);
			$all_prods_id = "\"".implode("\",\"", AuxFiles::get_sc_product_ids($this->hillslope_model_id))."\"";
			$all_reprs_id = "\"".implode("\",\"", AuxFiles::get_sc_representation_ids($this->hillslope_model_id))."\"";
			$json_final_content[1] = str_replace("SC_MODEL_ID", $this->model_id, $json_final_content[1]);   
			$json_final_content[2] = str_replace("MODEL_TITLE", $this->model_title, $json_final_content[2]);
			$json_final_content[3] = str_replace("MODEL_DESC", $this->model_desc, $json_final_content[3]);
			$json_final_content[4] = str_replace("MODEL_SHOW", $this->get_show_main_string(), $json_final_content[4]);
			$json_final_content[5] = str_replace("SC_PRODUCT_IDS", $all_prods_id, $json_final_content[5]);
			$json_final_content[6] = str_replace("SC_REPRESENTATION_IDS", $all_reprs_id, $json_final_content[6]);
			$json_final_content[7] = str_replace("BINGEN_SING_SCRIPT", 
			                                     AuxFiles::get_sing_script_path($this->hillslope_model_id), 
												 $json_final_content[7]);
			$json_final_content[8] = str_replace("BINGEN_HIST_SCRIPT", 
												 AuxFiles::get_hist_script_path($this->hillslope_model_id), 
												 $json_final_content[8]);
			
			// save edited template into file
			$fp = fopen($json_final_filepath, 'w');
			foreach ($json_final_content as $key => $value){
				fwrite($fp, $value);
			}
			fclose($fp);
		}
	}

	// 
	class RunsetRequest{
		public $runset_id;               // 
		public $runset_title;            //
		public $timestamp_ini;           //
		public $timestamp_end;           //
		public $user_email;              //
		public $current_timestamp;       //
		public $asynch_version;          //
		public $server_addr;             //
		public $max_models;              //
		public $what_run;                //
		public $model_requests;          //
		public $globalfile_requests;     //
		public $modelcombmaps;           //
		
		/**
		 * Construct function
		 */
		function __construct($posts){
			try{
				$this->current_timestamp = time();
				$this->runset_id = $posts["runset_id"];
				$this->runset_title = $posts["runset_title"];
				$this->timestamp_ini = $posts["timestamp_ini"];
				$this->timestamp_end = $posts["timestamp_end"];
				$this->user_email = $posts["email"];
				$this->max_models = $posts["num_models"];
				$this->what_run = $posts["what_run"];
				$this->asynch_version = $posts["asynch_ver"];
				$this->server_addr = $posts["server_addr"];
				$this->model_requests = null;
				$this->globalfile_requests = null;
			} catch(Exception $exp) {
				echo("Exception: ".$exp);
				exit();
			}
		}
		
		/**
		 *
		 * $model_requests :
		 * RETURN :
		 */
		public function create_global_files($model_requests){
			// prepare receiving lists
			$files_to_sent = array();
			$all_model_ids = array();
			$all_model_hlm = array();
			
			// iterates over each model creating its global files objects
			$all_global_files = array();
			foreach($model_requests as $cur_model_request){
				$cur_global_files = $cur_model_request->createGlobalFileRequests($this);
				foreach($cur_global_files as $cur_global_file){
					array_push($all_global_files, $cur_global_file);
				}
			}
			
			// create the global files
			$all_gbl_file_paths = array();
			foreach($all_global_files as $cur_global_files){
				$cur_gbl_file_path = $cur_global_files->create_files($this);
				if(!(is_null($cur_gbl_file_path))){
					array_push($all_gbl_file_paths, $cur_gbl_file_path);
				}
			}
			
			// create central job file
			$this->create_central_job_file($all_gbl_file_paths);
			
			// add model and globalfile resquests to the runset object
			$this->model_requests = $model_requests;
			$this->globalfile_requests = $all_global_files;
		}
		
		
		
		/**
		 *
		 * RETURN :
		 */
		public function create_runset_meta_file(){
			$json_final_filepath = AuxFiles::get_local_metarunset_file_path($this->current_timestamp);
		
			// read template file and separates main line
			$json_final_content = file(FoldersDefs::METARUNSET_TEMPLATE_FILEPATH);
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
			$local_folder_path = AuxFiles::get_local_temp_folder_path($current_time);
			if (!file_exists($local_folder_path)) {
				mkdir($local_folder_path, 0777, true);  // root folder
				mkdir(AuxFiles::get_local_temp_meta_folder_path($current_time));
				mkdir(AuxFiles::get_local_temp_meta_folder_path($current_time, 'models'));
				mkdir(AuxFiles::get_local_temp_meta_folder_path($current_time, 'matrices'));
				mkdir(AuxFiles::get_local_temp_meta_folder_path($current_time, 'modelcomb'));
				mkdir(AuxFiles::get_local_temp_meta_folder_path($current_time, 'runset'));
				mkdir(AuxFiles::get_local_temp_output_snapshot_folder_path($current_time), 0777, true);
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
		private function create_central_job_file($all_global_file_paths){
			// basic check
			if ((is_null($all_global_file_paths)) || (sizeof($all_global_file_paths) == 0)){ return(null); }
			
			// define job file path
			$job_final_filepath = AuxFiles::get_local_temp_folder_path($this->current_timestamp);
			$job_final_filepath .= $this->runset_id.".job";
			
			// define server's ASYNCH binary file location and the number of cores
			$job_cpn = AuxFiles::get_cpn($this->server_addr);
			$job_noc = AuxFiles::get_noc($this->server_addr);
			$asynch_call = AuxFiles::get_asynch_bin_path($this->server_addr, $this->asynch_version);
			
			// debug
			// echo("Got '".$job_cpn."' and '".$job_noc."' from '".$this->server_addr."'. ");
			
			// read template file and edits its content
			$job_final_content = file(FoldersDefs::JOB_TEMPLATE_FILEPATH);
			$job_final_content[1] = "#$ -N ".$this->runset_id."\n";                                                 // replace run id
			$job_final_content[2] = "#$ -o /Dedicated/IFC/back_time/";
			$job_final_content[2] .= $this->current_timestamp."/".$this->runset_id."_o.txt\n";                      // replace output log file name
			$job_final_content[3] = "#$ -e /Dedicated/IFC/back_time/";                                              // replace error log file name
			$job_final_content[3] .= $this->current_timestamp."/".$this->runset_id."_e.txt\n";
			$job_final_content[4] = "#$ -pe ".$job_cpn." ".$job_noc."\n";      
			if (trim($this->user_email) != ""){
				$job_final_content[5] = "#$ -m bea\n";                                                              // replace something here
				$job_final_content[6] = "#$ -M ".$this->user_email."\n";                                            // replace contact email
			} else {
				$job_final_content[5] = "\n";                                                                       // replace something here
				$job_final_content[6] = "\n";                                                                       // replace contact email
			}
			$job_final_content[7] = "#$ -q ".AuxFiles::get_queue($this->server_addr)."\n";                          // replace server queue
			
			// replace modules import
			$job_final_content[9] = AuxFiles::get_job_modules($this->server_addr);
			
			// add as many calls as apparently necessary
			$folder_path = AuxFiles::get_remote_folder_path($this->current_timestamp);
			$all_calls = "";
			foreach($all_global_file_paths as $cur_global_file_path){
				$all_calls .= "mpirun -np ".$job_noc." ".$asynch_call." ";
				$all_calls .= $folder_path.basename($cur_global_file_path."\n");
			}
			$job_final_content[11] = $all_calls;
			
			// save edited template into file
			$fp = fopen($job_final_filepath, 'w');
			foreach ($job_final_content as $cur_job_final_line){
				fwrite($fp, $cur_job_final_line);
			}
			fclose($fp);
			
			// just return
			return($job_final_filepath);
		}
		
		/**
		 * Used as a "gap filling" piece of code, replacement for 'create_comparison_mtx_meta_file()' function.
		 * RETURN : none
		 */
		public function create_comparison_mtx_empty_meta_file(){
			
			// defines final file path
			$json_final_filepath = AuxFiles::get_local_metacomparisonmtx_file_path($this->current_timestamp);
			
			// read template file and make empty comparisons
			$json_final_content = file(FoldersDefs::METACOMPARISON_TEMPLATE_FILEPATH);
			$json_final_content[1] = "";
			
			// write all internal lines
			$fp = fopen($json_final_filepath, 'w');
			foreach ($json_final_content as $value){
				fwrite($fp, $value);
			}
			fclose($fp);
		}
		
		/**
		 * Used as a "gap filling" piece of code, replacement for 'create_evaluation_mtx_meta_file()' function.
		 * RETURN : none
		 */
		public function create_evaluation_mtx_empty_meta_file(){
			
			// defines final file path
			$json_final_filepath = AuxFiles::get_local_metaevaluationmtx_file_path($this->current_timestamp);
		
			// read template file and make empty evaluations
			$json_final_content = file(FoldersDefs::METAEVALUATION_TEMPLATE_FILEPATH);
			$json_final_content[1] = "";
			
			// write all internal lines
			$fp = fopen($json_final_filepath, 'w');
			foreach ($json_final_content as $key => $value){
				fwrite($fp, $value);
			}
			fclose($fp);
			
			return;
		}
	}
	
	// 
	class ModelRequest{
		public $model_id;                 //
		public $hillslope_model_id;       //
		public $precipitation_source_id;  //
		public $reservoir_include;        //
		public $model_title;              //
		public $model_desc;               //
		public $gbl_parameters;           //
		public $modelseq_reprs;           //
		public $what_run;                 //
		public $globalfile_requests;      //
		
		/**
		 *
		 * $runsetRequest :
		 * RETURN : Array of GlobalFileRequest objects
		 */
		public function createGlobalFileRequests($runsetRequest){
			
			// establish the current time of request and create temporary folders
			$current_time = $runsetRequest->current_timestamp;
			// $local_folder_path = $this->create_local_temp_dirs();
			
			$gbl_flies_request = array();
			
			//
			switch($runsetRequest->what_run){
				case "06p06f_loginless":
				case "10p10f_loginless":
				
					// define other timestamps
					$timestamp_initcond = AuxFiles::get_initcond_timestamp($runsetRequest->timestamp_ini);
					$timestamp_mid = ($runsetRequest->timestamp_ini + $runsetRequest->timestamp_end)/2;
					
					// echo("All timestamps: [".$timestamp_initcond.", ".$runsetRequest->timestamp_ini.", ".$timestamp_mid.", ".$runsetRequest->timestamp_end."]. ");
					
					// create base global file object
					$base_gbl_file_req = new GlobalFileRequest();
					$base_gbl_file_req->fill_with_model_req($this);
					$base_gbl_file_req->fill_with_runset_req($runsetRequest);
					$base_gbl_file_req->timestamp_cur = $current_time;
					
					// create prev
					$prev_gbl_file_req = clone $base_gbl_file_req;
					$prev_gbl_file_req->model_id = $this->model_id."prevqpe";
					$prev_gbl_file_req->model_title = $this->model_title."(prev.)";
					$prev_gbl_file_req->timestamp_ini = $timestamp_initcond;
					$prev_gbl_file_req->timestamp_end = $runsetRequest->timestamp_ini;
					$prev_gbl_file_req->initcond_source = null;
					$prev_gbl_file_req->show_main = False;
					array_push($gbl_flies_request, $prev_gbl_file_req);
					
					// create past
					$past_gbl_file_req = clone $base_gbl_file_req;
					$past_gbl_file_req->model_id = $this->model_id."pastqpe";
					$past_gbl_file_req->model_title = $this->model_title."(past)";
					$past_gbl_file_req->timestamp_ini = $runsetRequest->timestamp_ini;
					$past_gbl_file_req->timestamp_end = $timestamp_mid;
					$past_gbl_file_req->initcond_source = $prev_gbl_file_req->model_id;
					$past_gbl_file_req->show_main = True;
					array_push($gbl_flies_request, $past_gbl_file_req);
					
					// create fore - rain
					$fore_gbl_file_req_qpe = clone $base_gbl_file_req;
					$fore_gbl_file_req_qpe->model_id = $this->model_id."foreqpe";
					$fore_gbl_file_req_qpe->model_title = $this->model_title."(fore. qpe)";
					$fore_gbl_file_req_qpe->timestamp_ini = $timestamp_mid;
					$fore_gbl_file_req_qpe->timestamp_end = $runsetRequest->timestamp_end;
					$fore_gbl_file_req_qpe->initcond_source = $prev_gbl_file_req->model_id;
					$fore_gbl_file_req_qpe->show_main = True;
					array_push($gbl_flies_request, $fore_gbl_file_req_qpe);
					
					// create fore - no rain
					$fore_gbl_file_req_non = clone $base_gbl_file_req;
					$fore_gbl_file_req_non->model_id = $this->model_id."forenon";
					$fore_gbl_file_req_non->model_title = $this->model_title."(fore. non)";
					$fore_gbl_file_req_non->timestamp_ini = $timestamp_mid;
					$fore_gbl_file_req_non->timestamp_end = $runsetRequest->timestamp_end;
					$fore_gbl_file_req_non->initcond_source = $prev_gbl_file_req->model_id;
					$fore_gbl_file_req_non->precip_source_id = null;
					$fore_gbl_file_req_non->show_main = True;
					array_push($gbl_flies_request, $fore_gbl_file_req_non);
					
					break;
				default:
				
					// create base global file object
					$the_gbl_file_req = new GlobalFileRequest();
					$the_gbl_file_req->fill_with_model_req($this);
					$the_gbl_file_req->fill_with_runset_req($runsetRequest);
					$the_gbl_file_req->timestamp_cur = $current_time;
				
					// TODO - implement for general case
					
					// add to list
					array_push($gbl_flies_request, $the_gbl_file_req);
				
					$timestamp_mid = null;
					break;
			}
			
			$this->globalfile_requests = $gbl_flies_request;
			
			return($gbl_flies_request);
		}
	}
	
	// 
	class ModelCombinationSequenceMap{
		// TODO - remove it, it is not being used. Silly idea?
		
		private $model_id_past;
		private $model_id_fore;
		private $model_comb_id;
		private $model_comb_title;
		public $representations_ids;
		
		function set_model_ids($model_id_past, $model_id_fore){
			$this->model_id_past = $model_id_past;
			$this->model_id_fore = $model_id_fore;
			
			$past_id_splitted = explode("past", $model_id_past);
			$fore_id_splitted = explode("fore", $model_id_fore);
			if (($past_id_splitted == $fore_id_splitted)&&(sizeof($past_id_splitted) == 2)&&(sizeof($fore_id_splitted) == 2)){
				return($past_id_splitted[0].$past_id_splitted[1].$fore_id_splitted[1]);
			} else {
				return($past_id_splitted[0].$past_id_splitted[1].$fore_id_splitted[1]);
			}
		}
		
		function __construct(){
			$this->representations_ids = array();
		}
	}
	
	//
	abstract class ModelRequestFactory{
		
		public static function getModelRequest($posts, $count_model){
			
			// basic check
			if(!isset($posts["model_id_".$count_model])){ 
				return(null);
			}
			
			// get most of fields
			$return_obj = new ModelRequest();
			$return_obj->model_id = $posts["model_id_".$count_model];
			$return_obj->model_title = $posts["model_title_".$count_model];
			$return_obj->model_desc = $posts["model_desc_".$count_model];
			$return_obj->hillslope_model_id = $posts["hillslope_model_".$count_model];
			$return_obj->precipitation_source_id = $posts["precipitation_source_".$count_model];
			$return_obj->reservoir_include = $posts["reservoir_include_".$count_model];
			
			echo("Part 1: Reservoir for model '".$return_obj->model_id."': ".$return_obj->reservoir_include.". ");
			
			// get parameters
			$parameter_set = array();
			$count_pars = 1;
			while(isset($posts["model_par_".$count_model."_".$count_pars])){
				$parameter_set[] = $posts["model_par_".$count_model."_".$count_pars];
				$count_pars = $count_pars + 1;
			}
			echo("Setting gbl_parameters as: '".$parameter_set."' (size ".sizeof($parameter_set)."). ");
			$return_obj->gbl_parameters = $parameter_set;
			
			// get model representations
			// TODO
			
			// get model comb representations
			if(isset($posts["modelseq_repr_".$count_model])){
				$return_obj->modelseq_reprs = explode(",", $posts["modelseq_repr_".$count_model]);
			} else {
				$return_obj->modelseq_reprs = null;
			}
			
			// check title and description (fill if left empty)
			if (trim($return_obj->model_title) == ""){ $return_obj->model_title = $return_obj->model_id; }
			if (trim($return_obj->model_desc) == ""){ $return_obj->model_desc = $cur_model_title; }
			
			return($return_obj);
		}
		
	}
	
	abstract class MetaFilesCreator{
		
		/**
		 *
		 * $runset_request : 
		 * $model_requests :
		 * RETURN :
		 */
		public static function create_comparison_mtx_meta_json_file($runset_request, $model_requests){
			
			switch($runset_request->what_run){
				case "06p06f_loginless":
				case "10p10f_loginless":
					// focus on model combination comparison
					MetaFilesCreator::create_comb_comparison_meta_json_file($runset_request, 
																			$model_requests);
					break;
					
				default:
					// focus on model comparison
					MetaFilesCreator::create_simp_comparison_meta_json_file($runset_request, 
																			$model_requests);
					break;
			}
		}
		
		/**
		 *
		 * $runset_request : 
		 * $model_requests : 
		 * RETURN :
		 */
		public static function create_evaluation_mtx_meta_file($runset_request, $model_requests){
			switch($runset_request->what_run){
				case "06p06f_loginless":
				case "10p10f_loginless":
					break;
				default:
					break;
			}
		}
		
		/**
		 *
		 * $runset_request :
		 * RETURN :
		 */
		public static function create_email_text_file($runset_request){
			// defines file path
			$text_filepath = AuxFiles::get_local_emailtext_file_path($runset_request->current_timestamp);
			
			// create file
			$fp = fopen($text_filepath, 'w');
			fwrite($fp, $runset_request->user_email);
			fclose($fp);
		}
		
		/**
		 *
		 * >-+ IMPORTANT +-< It was just copy-and-pasted. Need to be uncommented and worked on.
		 * $runset_request : 
		 * $model_requests : 
		 * RETURN :
		 */
		public static function create_metacomb_hydrographpast($runset_request, $model_requests){
			
			/*
			$line_replacement = '"MODELID":"modelpaststg"';
			
			// basic check - only creates the file if there is more than one model
			if(sizeof($model_ids) < 2){ return;	}
			
			$json_final_filepath = AuxFiles::get_local_metacomb_hydrographpast_file_path($current_timestamp);
			
			// build file content
			$models_array = array();
			for($i = 0; $i < sizeof($model_ids); $i++){
				$models_array[] = "\"".$model_ids[$i]."\":\"modelpaststg\"";
			}
			
			// read template file and replace its content
			$json_final_content = file_get_contents(AuxFiles::METAMODELCOMB_HYDROGRAPHSPAST_TEMPLATE_FILEPATH);
			$json_final_content = str_replace($line_replacement, implode(",", $models_array), $json_final_content);
			$json_final_content = str_replace("REFERENCEID", "usgsgagesdischarge",$json_final_content);
			
			// write all internal lines
			echo("Writing into '".$json_final_filepath."' ");
			file_put_contents($json_final_filepath, $json_final_content);
			*/
		}
		
		/**
		 *
		 * $runset_request : 
		 * $model_requests : 
		 * RETURN :
		 */
		public static function create_metacomb_sequencemaps($runset_request){
			
			/*
			$possible_forecasts_suffix = array('forenon', 'foreqpe');
			$only_possible_prefix = "pastqpe";
			
			// basic check
			if ((is_null($runset_request)) || 
					(is_null($runset_request->globalfile_requests)) || 
					(sizeof($runset_request->globalfile_requests) == 0)){
				return;
			}
			
			// all pairs
			$all_model_pairs = array();
			
			// find connections
			foreach($runset_request->globalfile_requests as $cur_globalfile_request){
				$cur_model_id = $cur_globalfile_request->model_id;
				
				foreach($possible_forecasts_suffix as $cur_pos_forecast_suffix){
					if (strpos($cur_model_id, $cur_pos_forecast_suffix) !== false){
						$cur_past_model_id = str_replace($cur_pos_forecast_suffix, $only_possible_prefix, $cur_model_id);
						foreach($runset_request->globalfile_requests as $cur_globalfile_request_2){
							$cur_model_id_2 = $cur_globalfile_request_2->model_id;
							if($cur_model_id == $cur_model_id_2){
								$cur_pair = array($cur_past_model_id, $cur_model_id);
								array_push($all_model_pairs, $cur_pair);
							}
						}
					}
				}
			}
			
			// basic check
			if(sizeof($all_model_pairs) == 0){
				echo("No matches found for sequencemaps in ".sizeof($all_model_pairs)." global file requests.");
				return;
			}
			
			// create files
			foreach($all_model_pairs as $cur_pair){
				MetaFilesCreator::create_metacomb_sequencemap($cur_pair[0], $cur_pair[1], $cur_pair[1]."seq", 
															  "SequenceMap(TODO)", 
															  $runset_request->current_timestamp,
															  null);
			}
			*/
			
			///////////////////////////////// SECOND APPROACH /////////////////////////////////
			
			echo("Iterating over ".sizeof($runset_request->model_requests)." model requests on '".$runset_request->runset_id."'... ");
			foreach($runset_request->model_requests as $cur_model_request){
				if((!is_null($cur_model_request->modelseq_reprs)) && (sizeof($cur_model_request->globalfile_requests)>2)){
					
					for($cur_fore_idx = 2; $cur_fore_idx < sizeof($cur_model_request->globalfile_requests); $cur_fore_idx++){
						
						$cur_model_fore_id = $cur_model_request->globalfile_requests[$cur_fore_idx]->model_id;
						
						// define title
						if (strpos($cur_model_fore_id, "forenon") !== false){
							$cur_model_seq_title = $cur_model_request->model_title." Seq. (Non Rain)";
						} elseif (strpos($cur_model_fore_id, "foreqpe") !== false) {
							$cur_model_seq_title = $cur_model_request->model_title." Seq. (QPE)";
						} elseif (strpos($cur_model_fore_id, "fore2in") !== false) {
							$cur_model_seq_title = $cur_model_request->model_title." Seq. (2 in)";
						} else {
							continue;
						}
						
						// TODO - make this step a loop for all forecasts
						$cur_modelseqs_id = $cur_model_fore_id."seqsrepr";
						$cur_modelpast_id = $cur_model_request->globalfile_requests[1]->model_id;
						$cur_modelfore_id = $cur_model_fore_id;
						MetaFilesCreator::create_metacomb_sequencemap($cur_modelpast_id, $cur_modelfore_id, 
																	  $cur_modelseqs_id, $cur_model_seq_title, 
																	  $runset_request->current_timestamp,
																	  $cur_model_request->modelseq_reprs);

					}
				} else if (is_null($cur_model_request->modelseq_reprs)) {
					echo("modelseq_reprs of '".$cur_model_request->modelseq_reprs."' is null. ");
				} else if (sizeof($cur_model_request->globalfile_requests)<=2){
					echo("size of globalfile_requests of '".$cur_model_request->modelseq_reprs."' is ".sizeof($cur_model_request->globalfile_requests).". ");
				} else {
					echo("??!!?? ");
				}
				
			}
		}
		
		/**
		 *
		 * $model_past_id : 
		 * $model_fore_id : 
		 * $model_id :
		 * $model_title :
		 * $current_timestamp : 
		 * $representations :
		 * RETURN : 
		 */
		private static function create_metacomb_sequencemap($model_past_id, $model_fore_id, $model_id, $model_title, 
															$current_timestamp, $representation_ids){
			
			// read template file and replace its content
			$json_final_content = file_get_contents(FoldersDefs::METAMODELCOMB_SEQUENCEMAPS_TEMPLATE_FILEPATH);
			$json_final_content = str_replace("RAWMODELID", $model_id, $json_final_content);
			$json_final_content = str_replace("RAWMODELTITLE", $model_title, $json_final_content);
			$json_final_content = str_replace("MODELIDPAST", $model_past_id, $json_final_content);
			$json_final_content = str_replace("MODELIDFORE", $model_fore_id, $json_final_content);
			
			// TODO: make the following line dynamic
			if (is_null($representation_ids)){
				$json_final_content = str_replace("REPRIDS", '', $json_final_content);
			} else {
				$all_repr_ids_tagged = array();
				foreach($representation_ids as $cur_repr_id){
					array_push($all_repr_ids_tagged, '"'.$cur_repr_id.'"');
				}
				$json_final_content = str_replace("REPRIDS", 
												  implode(",", $all_repr_ids_tagged), 
												  $json_final_content);
			}
			
			// define new meta file path and save it
			$json_final_filepath = AuxFiles::get_local_metacomb_hydrographpast_file_path($current_timestamp,
																						 $model_id);
			file_put_contents($json_final_filepath, $json_final_content);
		}
		
		/**
		 *
		 * $runset_request : 
		 * $model_requests : 
		 * RETURN :
		 */
		private static function create_simp_comparison_meta_json_file($runset_request, $model_requests){
			
			$json_final_filepath = AuxFiles::get_local_metacomparisonmtx_file_path($runset_request->current_timestamp);
			
			// read template file and separates main line
			$json_final_content = file(AuxFiles::METACOMPARISON_TEMPLATE_FILEPATH);
			$template_line = $json_final_content[1];
			
			// generates all internal lines
			$comp_lines = array();
			foreach($model_requests as $key_1 => $model_req1){
				foreach($model_requests as $key_2 => $model_req2){
					if($key_1 != $key_2){
						$cur_line = str_replace("MODELID01", $model_req1->model_id, $template_line);
						$cur_line = str_replace("MODELID02", $model_req2->model_id, $cur_line);
						$repr_ids = AuxFiles::get_sc_comparison_product_ids($model_req1->hillslope_model_id, 
																			$model_req2->hillslope_model_id);
						$cur_line = str_replace("SC_PRODUCT_IDS", "\"".implode("\",\"", $repr_ids)."\"", $cur_line);
						$comp_lines[] = $cur_line;
					}
				}
			}
			$json_final_content[1] = implode("		,\n", $comp_lines);
			
			// write all internal lines
			$fp = fopen($json_final_filepath, 'w');
			foreach ($json_final_content as $value){
				fwrite($fp, $value);
			}
			fclose($fp);
		}
		
		/**
		 *
		 * $runset_request :
		 * $model_requests :
		 * RETURN :
		 */
		private static function create_comb_comparison_meta_json_file($runset_request, $model_requests){
			// TODO
			return;
		}
	}
?>