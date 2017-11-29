<?php

    namespace Requester;

    use DbModels\ForcingSource;
    use DbModels\ForcingFormat;
    use Requester\AuxFilesLib as AuxFilesLib;
    use Requester\MetaFilesCreator as MetaFilesCreator;
    
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
        public $glb_remote_file_path;    // string: filepath for created Globalfile in the HPC
        public $has_reservoir;           // boolean:
        public $model_reprs;             // [string]: array of SC-Representation IDs
        
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
            $this->model_id = $model_request_obj->model_id;                            // string  : 
            $this->parameter_set = $model_request_obj->gbl_parameters;                 // [string]: 
            $this->hillslope_model_id = $model_request_obj->hillslope_model_id;        // integer : 
            // $this->precip_source_id = $model_request_obj->precipitation_source_id;  // integer : 
            // $this->reservoir_include = $model_request_obj->reservoir_include;       // boolean : 
            $this->forcings_dict = $model_request_obj->forcings_dict;                  //
            $this->model_reprs = $model_request_obj->model_reprs;                      //
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
        public function create_files($runsetRequest, $app){
            
            // create files effectively
            $gbl_file_path = $this->create_gbl_file($runsetRequest, $app);
            
            $this->create_referenced_files($runsetRequest);
            MetaFilesCreator::create_model_meta_file($this, $app);  // strange place for this
            
            // establish final gbl and job files
            $job_final_filepath = AuxFilesLib::get_local_temp_folder_path($this->timestamp_cur).$this->model_id.".job";
            $json_final_filepath = AuxFilesLib::get_local_metamodel_file_path($this->timestamp_cur, $this->model_id);
            
            return($gbl_file_path);
        }
        
        /**
         *
         * $runset_request_obj : 
         * RETURN : String - final global file path
         */
        private function create_gbl_file($runset_request_obj, $app){
            
            //ini_set('error_reporting', E_ALL);
            // error_reporting(E_ALL);
            
            
            $current_timestamp = $runset_request_obj->current_timestamp;
            $asynch_version = $runset_request_obj->asynch_version;
            
            // define gbl file name and path
            $glb_final_filename = $this->model_id.".gbl";
            $glb_final_filepath = AuxFilesLib::get_local_temp_folder_path($runset_request_obj->current_timestamp);
            $glb_final_filepath .= $glb_final_filename;
            
            // read template file
            // $gbl_final_content = file($app->fss->glb_template_filepath);
            $gbl_final_content = file_get_contents($app->fss->glb_template_filepath);
            
            // set hlm-model id
            $gbl_final_content = str_replace("<HILLSLOPE_MODEL_ID>", 
                                             $this->hillslope_model_id, 
                                             $gbl_final_content);
            
            // set simulation time
            if ($asynch_version == "1.1"){
                $max_time = ($this->timestamp_end - $this->timestamp_ini)/60; 
                $datetime_ini = "";
                $datetime_end = "";
            } elseif (in_array($asynch_version, array("1.2", "1.3"))) {
                $max_time = "";
                $datetime_ini = date('Y-m-d H:i', $this->timestamp_ini);
                $datetime_end = date('Y-m-d H:i', $this->timestamp_end);
            }
            $gbl_final_content = str_replace("<MAX_TIME>", $max_time, $gbl_final_content);
            $gbl_final_content = str_replace("<INI_DATETIME>", $datetime_ini, $gbl_final_content);
            $gbl_final_content = str_replace("<END_DATETIME>", $datetime_end, $gbl_final_content);
            
            // set global parameters
            $gbl_final_content = str_replace("<GLOBAL_PARAMETERS>",
                                             sizeof($this->parameter_set)." ".implode(" ", $this->parameter_set),
                                             $gbl_final_content);

            // set topology
            $topo_file_path = AuxFilesLib::get_remote_topology_file_path($current_timestamp);
            $gbl_final_content = str_replace("<TOPOLOGY_FILE_PATH>", 
                                             $topo_file_path, 
                                             $gbl_final_content);
                                             
            // set DEM parameters
            $prms_file_path = AuxFilesLib::get_remote_demparameters_file_path($this->timestamp_cur, 
                                                                              $this->hillslope_model_id);
            $gbl_final_content = str_replace("<DEM_PARAMETERS_FILE_PATH>",
                                             $prms_file_path,
                                             $gbl_final_content);
            
            // set initial condition
            $init_file_path = AuxFilesLib::get_remote_initcond_mod_file_path($this->timestamp_cur, 
                                                                             $this->hillslope_model_id, 
                                                                             $this->timestamp_ini, 
                                                                             $this->model_id, 
                                                                             $asynch_version);
            $gbl_final_content = str_replace("<INICOND_FILEPATH> <INICOND_TIMESTAMP>",
                                             $init_file_path,
                                             $gbl_final_content);
            
            // set total number of forcings
            $gbl_final_content = str_replace("<FORCINGS_NUMBER>",
                                             sizeof($this->forcings_dict),
                                             $gbl_final_content);

            // set all forcings
            $all_forcings = "";
            foreach($this->forcings_dict as $cur_idx => $cur_forcing_source){
                $cur_forcing_lines = $this->define_forcing_source_lines($cur_forcing_source, $cur_idx, $app);
                $all_forcings .= $cur_forcing_lines[0]."\n";
                $all_forcings .= $cur_forcing_lines[1]."\n";
                $all_forcings .= $cur_forcing_lines[2]."\n\n";
            }
            $gbl_final_content = str_replace("<ALL_FORCINGS>",
                                             $all_forcings,
                                             $gbl_final_content);
            
            // set QVS
            /*
            $qvs_file_path = AuxFilesLib::get_remote_qvs_file_path($this->timestamp_cur);
            $gbl_final_content = str_replace("<QVS_FILEPATH>",
                                             $qvs_file_path,
                                             $gbl_final_content);
            */
            
            // set reservoirs
            $rsv_line = $this->define_reservoir_links_line($app);
            $gbl_final_content = str_replace("<RESERVOIRS_LINE>",
                                             $rsv_line,
                                             $gbl_final_content);
            
            // set output snapshots
            if (!is_null($this->initcond_source)) {
                $snapshot_line = "4 60 ".AuxFilesLib::get_remote_output_snapshot_file_path($this->model_id, 
                                                                                              $this->timestamp_cur, 
                                                                                           $this->timestamp_ini,
                                                                                           $asynch_version,
                                                                                           false)."\n";   // replace output snapshot
            } else {
                $snapshot_line = "3 ".AuxFilesLib::get_remote_output_snapshot_file_path($this->model_id, 
                                                                                        $this->timestamp_cur, 
                                                                                        $this->timestamp_end,
                                                                                        $asynch_version,
                                                                                        true)."\n";   // replace output snapshot
            }
            $gbl_final_content = str_replace("<OUT_SNAPSHOT_LINE>",
                                             $snapshot_line,
                                             $gbl_final_content);
            
            // set scratch file
            $snapshot_line = AuxFilesLib::get_remote_scratch_file_path($this->timestamp_cur)."\n";
            $gbl_final_content = str_replace("<SCRATCH_FILE>",
                                             $snapshot_line,
                                             $gbl_final_content);
            
            // save edited template into file
            try {
              $fp = fopen($glb_final_filepath, 'w');
              fwrite($fp, $gbl_final_content);
              fclose($fp);
            } catch (Exception $e) {
              echo 'Caught exception: ',  $e->getMessage(), "\n";
            }
            
            // create folder in which output snapshots are going to be stored in the future
            $np = AuxFilesLib::get_local_temp_output_snapshot_specific_folder_path($this->timestamp_cur, 
                                                                                   $this->model_id);
            mkdir($np, 0777, true);
            
            $this->glb_remote_file_path = $glb_final_filepath;
            
            return($glb_final_filepath);
            
        }
        
        /**
         *
         * $forcing_source_id:
         * RETURN : Array of size 3, each element is a line
         */
        private function define_forcing_source_lines($forcing_source_id, $forcing_index, $app){
            if($forcing_source_id == -1){
                // TODO - find a way to check if a reservoir info is coming
                $return_array = array();
                $return_array[] = "-1  % user-provided file not implemented yet";
                $return_array[] = "";
                $return_array[] = "";
            } else if ($forcing_source_id == 0) {
                $return_array = array();
                $return_array[] = "0  % no-forcing choosen";
                $return_array[] = "";
                $return_array[] = "";
            } else {
                $return_array = $this->retrieve_forcing_source_lines_from_db($forcing_source_id,
                                                                             $forcing_index,
                                                                             $app);
            }
            
            return($return_array);
        }
        
        /**
         *
         * $forcing_source_id :
         * RETURN :
         */
        private function retrieve_forcing_source_lines_from_db($forcing_source_id, 
                                                               $forcing_index,
                                                               $app){
            $return_array = array();
            $force_source = ForcingSource::where('id', (int)$forcing_source_id)->first();
            $force_format = ForcingFormat::where('id', $force_source->forcingformat_id)->first();
            
            // 1st line
            $return_array[] = "% forcing: '".$force_source->title."'";
            
            // 2nd and 3rd lines
            $lines = $force_format->glb_file_line;
            $lines = str_replace("<ANCILLARY_FOLDER_PATH>", $app->fss->dest_central_folder_path, $lines);
            $lines = str_replace("<FILE_NAME>", $force_source->ancillary_file_name, $lines);
            $lines = str_replace("<TIME_STEP>", $force_source->time_resolution, $lines);
            $lines = str_replace("<TIMESTAMP_INI>", $this->timestamp_ini, $lines);
            $lines = str_replace("<TIMESTAMP_END>", $this->timestamp_end, $lines);
            
            // separate in the array
            $splitted = explode("\\n", $lines);
            $return_array[] = $splitted[0];
            $return_array[] = sizeof($splitted) >= 2 ? $splitted[1] : "";
            
            // TODO - remove this following dirty movement
            if($force_source->forcingtype_id == 3){
                $this->reservoir_rsv = str_replace(".dbc", ".rsv", 
                                                   $force_source->ancillary_file_name);
                $this->reservoir_idx = $forcing_index;
            }
            
            return($return_array);
        }
        
        /**
         *
         * RETURN :
         */
        private function define_reservoir_links_line($app){
            if(is_null($this->reservoir_rsv) || is_null($this->reservoir_idx)){
                return("0\n");
            } else {
                $file_path = $app->fss->dest_central_folder_path.$this->reservoir_rsv;
                return("1 ".$file_path." ".$this->reservoir_idx."\n");
            }
        }
        
        /**
         *
         * $runset_request_obj :
         * RETURN :
         */
        private function create_referenced_files($runset_request_obj){
            $current_timestamp = $runset_request_obj->current_timestamp;
            
            /*
            AuxFilesLib::setup_local_temp_topology_file($current_timestamp);
            AuxFilesLib::setup_local_temp_demparameters_file($current_timestamp, 
                                                          $this->hillslope_model_id);
            */
            /*
            // TODO - remove this copy of initial condition file
            if (($this->hillslope_model_id) && (is_null($this->initcond_source))){
                echo("Going for '".$current_timestamp."', '".$this->hillslope_model_id."', '".$this->timestamp_ini."'. ");
                AuxFilesLib::setup_local_temp_initcond_file($current_timestamp, 
                                                         $this->hillslope_model_id, 
                                                         $this->timestamp_ini);
            }
            */
            if (!is_null($this->precip_source_id)){
                AuxFilesLib::setup_local_temp_raindata_file($current_timestamp, 
                                                         $this->precip_source_id);
            }
            AuxFilesLib::setup_local_temp_evaporation_file($current_timestamp);
            AuxFilesLib::setup_local_temp_qvs_file($current_timestamp);
            
            if ($this->reservoir_include == 'true'){
                AuxFilesLib::setup_local_temp_reservoir_files($current_timestamp);
            }
        }
        
        /**
         * 
         * >-+ IMPORTANT +-< It was just copy-and-pasted. Need to be worked on.
         * $runset_request_obj : 
         * RETURN : String - final job file path
         */
        private function create_job_file($app){
            $dst_folder_path = $app->fss->dest_folder_path;
            
            // read template file and edits its content
            $glb_file_path = AuxFilesLib::get_remote_global_file_path($current_timestamp, $model_id);
            $job_final_content = file(AuxFilesLib::JOB_TEMPLATE_FILEPATH);
            $job_cpn = AuxFilesLib::get_cpn($server_addr);
            $job_noc = AuxFilesLib::get_noc($server_addr);
            $asynch_call = AuxFilesLib::get_asynch_bin_path($server_addr, $asynch_version);
            $job_final_content[1] = "#$ -N ".$model_id."\n";                                                // replace run id
            $job_final_content[2] = "#$ -o ".$dst_folder_path.$current_timestamp."/".$model_id."_o.txt\n";  // replace output log file name
            $job_final_content[3] = "#$ -e ".$dst_folder_path.$current_timestamp."/".$model_id."_e.txt\n";  // replace error log file name
            $job_final_content[4] = "#$ -pe ".$job_cpn." ".$job_noc."\n";                                   // replace number of cores
            if (trim($email) != ""){
                $job_final_content[5] = "#$ -m bea\n";                                                      // replace something here
                $job_final_content[6] = "#$ -M ".$email."\n";                                               // replace contact email
            } else {
                $job_final_content[5] = "\n";                                                               // replace something here
                $job_final_content[6] = "\n";                                                               // replace contact email
            }
            $job_final_content[7] = "#$ -q ".AuxFilesLib::get_queue($server_addr )."\n";                    // replace server queue
            $job_final_content[13] = "\nmpirun -np ".$job_noc." ".$asynch_call." ".$glb_file_path;          // replace system call command
            $job_final_content[15] = str_replace("<DEST_FOLDER_PATH>", $dst_folder_path, 
                                                 $job_final_content[15]);
            
            // save edited template into file
            $fp = fopen($job_final_filepath, 'w');
            foreach ($job_final_content as $key => $value){
                fwrite($fp, $value);
            }
            fclose($fp);
        }
        
        /**
         * TODO - this should not be here...
         * RETURN :
         */
        /*
        private function create_model_meta_file($app){
            
            $timestamp_cur = $this->timestamp_cur;
            $model_id = $this->model_id;
            $json_final_filepath = AuxFilesLib::get_local_metamodel_file_path($timestamp_cur, $model_id);
            
            // read template file and edits its content
            $json_final_content = file($app->fss->metamodel_template_filepath);
            $all_prods_id = "\"".implode("\",\"", AuxFilesLib::get_sc_product_ids($this->hillslope_model_id))."\"";
            $all_reprs_id = "\"".implode("\",\"", AuxFilesLib::get_sc_representation_ids($this->hillslope_model_id))."\"";
            $json_final_content[1] = str_replace("SC_MODEL_ID", $this->model_id, $json_final_content[1]);   
            $json_final_content[2] = str_replace("MODEL_TITLE", $this->model_title, $json_final_content[2]);
            $json_final_content[3] = str_replace("MODEL_DESC", $this->model_desc, $json_final_content[3]);
            $json_final_content[4] = str_replace("MODEL_SHOW", $this->get_show_main_string(), $json_final_content[4]);
            $json_final_content[5] = str_replace("SC_PRODUCT_IDS", $all_prods_id, $json_final_content[5]);
            $json_final_content[6] = str_replace("SC_REPRESENTATION_IDS", $all_reprs_id, $json_final_content[6]);
            $json_final_content[7] = str_replace("BINGEN_SING_SCRIPT", 
                                                 AuxFilesLib::get_sing_script_path($this->hillslope_model_id), 
                                                 $json_final_content[7]);
            $json_final_content[8] = str_replace("BINGEN_HIST_SCRIPT", 
                                                 AuxFilesLib::get_hist_script_path($this->hillslope_model_id), 
                                                 $json_final_content[8]);
            
            // save edited template into file
            $fp = fopen($json_final_filepath, 'w');
            foreach ($json_final_content as $key => $value){
                fwrite($fp, $value);
            }
            fclose($fp);
        }
        */
    }

?>