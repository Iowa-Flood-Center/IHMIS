<?php

	include_once("../common/class_FoldersDefs.php");

	class AuxFiles{
		
		const INITCOND_FILE_EXT = ".h5";
		const INITCOND_FILE_PREFIX = "state";
		
		const FARAWAY_FUTURE = "1588291200";
		
		const TOPOLOGY_FILE_NAME = "all_iowa.rvr";
		
		const METAFILES_FOLDER_NAME = "metafiles_sandbox";
		const METAFILES_MODELS_FOLDER_NAME = "sc_models";
		const METAFILES_MODELSCOMB_FOLDER_NAME = "sc_modelcombinations";
		const METAFILES_MATRICES_FOLDER_NAME = "cross_matrices";
		const METAFILES_RUNSET_FOLDER_NAME = "sc_runset";
		
		// /****************** get specific data ****************/ //
		
		/**
		 *
		 * $precipitation_source_id :
		 * RETURN :
		 */
		public static function get_raindbc_raininterval($precipitation_source_id){
			switch($precipitation_source_id){
				case "st4":
					return(60);
				case "mrms":
					return(60);
				case "ifc":
					return(5);
				default:
					return(null);
			}
		}
		
		/**
		 *
		 * $precipitation_source_id :
		 * RETURN :
		 */
		public static function get_raindbc_raininstances($precipitation_source_id){
			switch($precipitation_source_id){
				case "st4":
					return(1);
				case "mrms":
					return(1);
				case "ifc":
					return(12);
				default:
					return(null);
			}
		}
		
		/**
		 *
		 * $hillslope_model_id : 
		 * RETURN : Array of Strings with sc_product_ids.
		 */
		public static function get_sc_product_ids($hillslope_model_id){
			switch($hillslope_model_id){
				case 190:
					return(null);
				case 254:
					return (array('idq', 'ids_p', 'ids_l', 'ids_s', 'idv_p', 'idv_r'));
				case 262:
					return(null);
				default:
					return(null);
			}
		}
		
		/**
		 *
		 * $hillslope_model_id : 
		 * RETURN : Array of Strings with sc_product_ids.
		 */
		public static function get_sc_representation_ids($hillslope_model_id){
			switch($hillslope_model_id){
				case 190:
					return(null);
				case 254:
					return (array("runacchil24hh", "runacchil12hh", "runacchil06hh", "runacchil03hh",
								  "preacchil24hh", "preacchil12hh", "preacchil06hh", "preacchil03hh",
								  "preacchildayh", "soimoi20ih", "soiwac20ih", "disclausgsih",
								  "fldidxusgsih", "pah03hdcuih", "dcufldicuih", "pa03hdflicih"));
				case 262:
					return(null);
				default:
					return(null);
			}
		}
		
		/**
		 * 
		 * $hillslope_model_id_a : Integer.
		 * $hillslope_model_id_b : Integer.
		 * RETURN :
		 */
		public static function get_sc_comparison_product_ids($hillslope_model_id_a, $hillslope_model_id_b){
			
			if (($hillslope_model_id_a == 254) && ($hillslope_model_id_b == 254)){
				return(array("runacchil24hh", "runacchil12hh", "runacchil06hh", "runacchil03hh", 
							 "preacchil24hh", "preacchil12hh", "preacchil06hh", "preacchil03hh", 
							 "soimoi20ih", "soiwac20ih", "disclausgsih", "fldidxusgsih"));
			} else {
				return(null);
			}
		}
		
		/**
		 * 
		 * $hillslope_model_id : 
		 * RETURN : 
		 */
		public static function get_sing_script_path($hillslope_model_id){
			return ("python /groups/asynch/ModelPlus/backend/model_3_0_scripts/python/libs/bingen_states_asynchmodel".$hillslope_model_id."_hdf5.py");
		}
		
		/**
		 * 
		 * $hillslope_model_id : 
		 * RETURN : 
		 */
		public static function get_hist_script_path($hillslope_model_id){
			return ("python /groups/asynch/ModelPlus/backend/model_3_0_scripts/python/libs/bingen_states_hist_asynchmodel".$hillslope_model_id."_hdf5.py");
		}
		
		/**
		 *
		 * $server_address : String.
		 * $asynch_version : String.
		 * RETURN :
		 */
		public static function get_asynch_bin_path($server_address, $asynch_version){
			$folder_name = null;
			$bin_name = null;
			
			// define server compilation
			switch($server_address){
				case "neon.hpc.uiowa.edu":
					$folder_name = ".neon";
					break;
				case "argon.hpc.uiowa.edu":
					$folder_name = ".argon";
					break;
				default:
					break;
			}
			
			// define bin file name
			switch($asynch_version){
				case "1.1":
					$bin_name = "asynch-1.0.1";
					break;
				case "1.2":
					$bin_name = "asynch-1.2.1";
					break;
				case "1.3":
					$bin_name = "asynch-1.3.0";
					break;
				default:
					break;
			}
			
			// basic test
			if ((is_null($folder_name))||(is_null($bin_name))){
				return("__INVALID_PARAMETERS_".$server_address."+".$asynch_version);
			}
			
			// return
			return("/Dedicated/IFC/".$folder_name."/bin/".$bin_name);
		}
		
		/**
		 *
		 * $server_address :
		 * RETURN :
		 */
		public static function get_cpn($server_address){
			switch($server_address){
				case "argon.hpc.uiowa.edu":
					return("56cpn");
				case "neon.hpc.uiowa.edu":
					return("16cpn");
				case "helium.hpc.uiowa.edu":
					return("8cpn");
				default:
					return(null);
			}
		}
		
		/**
		 *
		 * $server_address :
		 * RETURN :
		 */
		public static function get_noc($server_address){
			switch($server_address){
				case "argon.hpc.uiowa.edu":
					return(56);
				case "neon.hpc.uiowa.edu":
					return(16);
				case "helium.hpc.uiowa.edu":
					return(16);
				default:
					return(null);
			}
		}
		
		/**
		 *
		 * $server_address :
		 * RETURN :
		 */
		public static function get_queue($server_address){
			switch($server_address){
				case "argon.hpc.uiowa.edu":
					return("IFC");
				case "neon.hpc.uiowa.edu":
					return("all.q");
				case "helium.hpc.uiowa.edu":
					return("IFC");
				default:
					return(null);
			}
		}
		
		/**
		 *
		 * $server_address :
		 * RETURN :
		 */
		public static function get_job_modules($server_address){
			$ret_str = "";
			switch($server_address){
				case "argon.hpc.uiowa.edu":
					$ret_str .= "export PATH=\$PATH:\$HOME/.local/bin:/Dedicated/IFC/.argon/bin"."\n";
					$ret_str .= "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/Dedicated/IFC/.argon/lib"."\n";
					$ret_str .= "module load zlib/1.2.11_parallel_studio-2017.1"."\n";
					$ret_str .= "module load hdf5/1.8.18_parallel_studio-2017.1"."\n";
					$ret_str .= "module load openmpi/2.0.1_parallel_studio-2017.1"."\n";
					return($ret_str);
				case "neon.hpc.uiowa.edu":
					$ret_str .= "module load intel/2015.3.187"."\n";
					$ret_str .= "module load openmpi/intel-composer_xe_2015.3.187-1.8.8"."\n";
					$ret_str .= "module load hdf5/1.8.17"."\n";
					return($ret_str);
				case "helium.hpc.uiowa.edu":
					return(null);
				default:
					return(null);
			}
		}
		
		/**
		 * Establishes the initial condition timestamp to be used used by the simulation
		 * $runset_ini_timestamp : Initial timestamp of the simulation
		 * RETURN : Integer - Timestamp of the initial condition
		 */
		public static function get_initcond_timestamp($runset_ini_timestamp){
			
			// TODO: implement it properly
			date_default_timezone_set('America/Chicago');
			$the_date = getdate($runset_ini_timestamp);
			$prev_day = $the_date['mday'];
			
			// debug
			// echo("From ".$the_date['mon']."/".$the_date['mday']."/".$the_date['year']." ");
			// echo("(".$runset_ini_timestamp.") ");
			
			if($prev_day < 10){
				$the_date['mday'] = 1;
			} else if ($prev_day < 20){
				$the_date['mday'] = 11;
			} else {
				$the_date['mday'] = 21;
			}
			
			date_default_timezone_set('GMT');
			$return_timestamp = mktime(0, 0, 0, $the_date['mon'], $the_date['mday'], $the_date['year']);
			
			// debug
			// echo("To ".$the_date['mon']."/".$the_date['mday']."/".$the_date['year']." ");
			// echo("(".$return_timestamp.").\n ");
			
			return($return_timestamp);
		}
		
		/**
		 *
		 * $hawkid :
		 * RETURN : String.
		 */
		public static function get_destination_url($hawkid){
			return(AuxFiles::DEST_BASE_URL.$hawkid."/");
		}
		
		// /******************* get file names ******************/ //
		
		/**
		 *
		 * RETURN :
		 */
		public static function get_topology_file_name(){
			return("all_iowa.rvr");
		}
		
		/**
		 *
		 * $hillslope_model_id :
		 * RETURN :
		 */
		public static function get_dempars_file_name($hillslope_model_id){
			return("params54_".$hillslope_model_id.".dbc");
		}
		
		/**
		 *
		 * NOTE 1: Inverse method of 'AuxFiles::extract_hlmodel_from_initialcondition_file_name()'.
		 * NOTE 2: Inverse method of 'AuxFiles::extract_timestamp_from_initialcondition_file_name()'.
		 * $hillslope_model_id :
		 * $initcond_timestamp :
		 * RETURN : String
		 */
		public static function get_initialcondition_file_name($hillslope_model_id, $initcond_timestamp){
			return("state".$hillslope_model_id."_".$initcond_timestamp.AuxFiles::INITCOND_FILE_EXT);
		}
		
		/**
		 *
		 * $precipitation_source_id :
		 * RETURN :
		 */
		public static function get_raindata_file_name($precipitation_source_id){
			return("forcing_rain54_".$precipitation_source_id.".dbc");
		}
		
		/**
		 *
		 * RETURN :
		 */
		public static function get_evaporation_file_name(){
			return("evap.mon");
		}
		
		/**
		 *
		 * RETURN :
		 */
		public static function get_qvs_file_name(){
			return("qvs_54.dbc");
		}
		
		/**
		 *
		 * RETURN :
		 */
		public static function get_rsvdbc_file_name(){
			return("reservoirs_54.dbc");
		}
		
		/**
		 *
		 * RETURN :
		 */
		public static function get_rsv_file_name(){
			return("reservoirs.rsv");
		}
		
		/**
		 *
		 * $init_timestamp : Integer. Timestamp of the beginning of the simulation.
		 * $asynch_version : String. Expected values like '1.1' or '1.2'.
		 * RETURN : String
		 */
		public static function get_output_snapshot_file_name($out_timestamp, $asynch_version, $force_timestamp){
			if (($asynch_version == "1.1")||($force_timestamp == true)){
				return("snapshot_".$out_timestamp.".h5");
			} elseif (in_array($asynch_version, array("1.2", "1.3"))) {
				return("snapshot.h5");
			} else {
				return(null);
			}
		}
		
		/**
		 *
		 * $current_time :
		 * RETURN : String
		 */
		public static function get_input_targz_file_name($current_time){
			return($current_time.".tar.gz");
		}
		
		// /******************* process file names ******************/ //
		
		/**
		 *
		 * NOTE : Inverse method of 'AuxFiles::get_initialcondition_file_name()'.
		 * $initcond_timestamp_filename :
		 * RETURN : Integer
		 */
		public static function extract_hlmodel_from_initialcondition_file_name($initcond_filename){
			// basic check
			if(is_null($initcond_filename)){ return(null); }
			
			// process string
			$basename = str_replace(AuxFiles::INITCOND_FILE_EXT, "", $initcond_filename);
			$basename = str_replace(AuxFiles::INITCOND_FILE_PREFIX, "", $basename);
			$exploded = explode("_", $basename);
			
			// basic check and return
			if(is_numeric($exploded[0])){
				return(intval($exploded[0]));
			} else {
				return(null);
			}
		}
		
		/**
		 *
		 * NOTE : Inverse method of 'AuxFiles::get_initialcondition_file_name()'.
		 * $initcond_timestamp_filename :
		 * RETURN : Integer
		 */
		public static function extract_timestamp_from_initialcondition_file_name($initcond_filename){
			// basic check
			if(is_null($initcond_filename)){ return(null); }
			
			// process string
			$basename = str_replace(AuxFiles::INITCOND_FILE_EXT, "", $initcond_filename);
			$basename = str_replace(AuxFiles::INITCOND_FILE_PREFIX, "", $basename);
			$exploded = explode("_", $basename);
			
			// basic check and return
			if((sizeof($exploded) == 2) && (is_numeric($exploded[1]))){
				return(intval($exploded[1]));
			} else {
				return(null);
			}
		}
		
		// /************** get template/repository file paths **************/ //
		
		/**
		 *
		 * RETURN : String
		 */
		public static function get_topology_template_file_path(){
			$topo_file_name = AuxFiles::get_topology_file_name();
			return(FoldersDefs::TEMPLATE_FILES_FOLDER_PATH.AuxFiles::TOPOLOGY_FILE_NAME);
		}
		
		/**
		 *
		 * $hillslope_model_id : Like '190', '254', '262'
		 * RETURN : String
		 */
		public static function get_demparameters_template_file_path($hillslope_model_id){
			$demparameters_file_name = "param54_".$hillslope_model_id."_const.dbc";
			return(FoldersDefs::TEMPLATE_FILES_FOLDER_PATH.$demparameters_file_name);
		}
		
		/**
		 * 
		 * $hillslope_model_id :
		 * $initcond_timestamp :
		 * RETURN : String
		 */
		public static function get_initcond_repo_file_path($hillslope_model_id, $initcond_timestamp){
			$initcond_filename = AuxFiles::get_initialcondition_file_name($hillslope_model_id, $initcond_timestamp);
			return(FoldersDefs::INITIALSTATES_HDF5_FOLDERPATH.$hillslope_model_id.DIRECTORY_SEPARATOR.$initcond_filename);
		}
		
		/**
		 *
		 * $precipitation_source_id :
		 * RETURN : String
		 */
		public static function get_raindata_template_file_path($precipitation_source_id){
			$forcingprecip_file_name = "forcing_rain_".$precipitation_source_id.".dbc";
			return(FoldersDefs::TEMPLATE_FILES_FOLDER_PATH.$forcingprecip_file_name);
		}
		
		/**
		 * As the source of evapotranspiration may also be a variable in the future, let's start using good practices from now.
		 * RETURN : String
		 */
		public static function get_evaporation_template_file_path(){
			$evapotranspiration_file_name = "evap.mon";
			return(FoldersDefs::TEMPLATE_FILES_FOLDER_PATH.$evapotranspiration_file_name);
		}
		
		/**
		 * As the source of dam's discharge (QVS) may also be a variable in the future, let's start using good practices from now.
		 * RETURN : String
		 */
		public static function get_qvs_template_file_path(){
			return(FoldersDefs::TEMPLATE_FILES_FOLDER_PATH . AuxFiles::get_qvs_file_name());
		}
		
		/**
		 * 
		 * RETURN : String
		 */
		public static function get_rsvdbc_template_file_path(){
			return(FoldersDefs::TEMPLATE_FILES_FOLDER_PATH . AuxFiles::get_rsvdbc_file_name());
		}
		
		/**
		 * 
		 * RETURN : String
		 */
		public static function get_rsv_template_file_path(){
			return(FoldersDefs::TEMPLATE_FILES_FOLDER_PATH . AuxFiles::get_rsv_file_name());
		}
		
		// /*************** get local file paths ****************/ //
		
		/**
		 *
		 * $hawk_id :
		 * RETURN :
		 */
		public static function get_local_folder_path($hawk_id){
			return(FoldersDefs::TEMP_FOLDERPATH.$hawk_id."/");
		}
		
		/**
		 *
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function get_local_temp_folder_path($current_timestamp){
			return(FoldersDefs::TEMP_FOLDERPATH.$current_timestamp."/");
		}
		
		/**
		 *
		 * $hawk_id :
		 * RETURN :
		 */
		public static function get_local_topology_file_path($hawk_id){
			return(AuxFiles::get_local_folder_path($hawk_id).AuxFiles::TOPOLOGY_FILE_NAME);
		}
		
		/**
		 *
		 * $hawk_id :
		 * RETURN :
		 */
		public static function get_local_temp_topology_file_path($current_timestamp){
			return(AuxFiles::get_local_temp_folder_path($current_timestamp).AuxFiles::TOPOLOGY_FILE_NAME);
		}
		
		/**
		 *
		 * $current_timestamp :
		 * $subfolder : Expected 'models', 'matrices' or not provided.
		 * RETURN : String. Path for the root folder of metafiles if $subfolder is not provided, path for the subfolder if provided.
		 */
		public static function get_local_temp_meta_folder_path($current_timestamp, $subfolder=false){
			if(!$subfolder){
				return(AuxFiles::get_local_temp_folder_path($current_timestamp).AuxFiles::METAFILES_FOLDER_NAME."/");
			} else {
				if ($subfolder == "models"){
					return(AuxFiles::get_local_temp_folder_path($current_timestamp).AuxFiles::METAFILES_FOLDER_NAME."/".AuxFiles::METAFILES_MODELS_FOLDER_NAME."/");
				} elseif ($subfolder == "matrices") {
					return(AuxFiles::get_local_temp_folder_path($current_timestamp).AuxFiles::METAFILES_FOLDER_NAME."/".AuxFiles::METAFILES_MATRICES_FOLDER_NAME."/");
				} elseif ($subfolder == "runset") {
					return(AuxFiles::get_local_temp_folder_path($current_timestamp).AuxFiles::METAFILES_FOLDER_NAME."/".AuxFiles::METAFILES_RUNSET_FOLDER_NAME."/");
				} elseif ($subfolder == "modelcomb"){
					return(AuxFiles::get_local_temp_folder_path($current_timestamp).AuxFiles::METAFILES_FOLDER_NAME."/".AuxFiles::METAFILES_MODELSCOMB_FOLDER_NAME."/");
				} else {
					return(null);
				}
			}
		}
		
		/**
		 *
		 * $hawk_id :
		 * $hillslope_model_id :
		 * RETURN :
		 */
		public static function get_local_dempars_file_path($hawk_id, $hillslope_model_id){
			return(AuxFiles::get_local_folder_path($hawk_id).AuxFiles::get_dempars_file_name($hillslope_model_id));
		}
		
		/**
		 *
		 * $current_timestamp : 
		 * $hillslope_model_id : 
		 * RETURN :
		 */
		public static function get_local_temp_dempars_file_path($current_timestamp, $hillslope_model_id){
			return(AuxFiles::get_local_folder_path($current_timestamp).AuxFiles::get_dempars_file_name($hillslope_model_id));
		}
		
		/**
		 *
		 * $hawk_id :
		 * $hillslope_model_id : 
		 * $initcond_timestamp :
		 * RETURN :
		 */
		public static function get_local_initcondition_file_path($hawk_id, $hillslope_model_id, $initcond_timestamp){
			$initcond_filename = AuxFiles::get_initialcondition_file_name($hillslope_model_id, $initcond_timestamp);
			return(AuxFiles::get_local_folder_path($hawk_id).$initcond_filename);
		}
		
		/**
		 *
		 * $current_timestamp : 
		 * $hillslope_model_id : 
		 * $initcond_timestamp : 
		 * RETURN :
		 */
		public static function get_local_temp_initcondition_file_path($current_timestamp, $hillslope_model_id, $initcond_timestamp){
			$initcond_filename = AuxFiles::get_initialcondition_file_name($hillslope_model_id, $initcond_timestamp);
			return(AuxFiles::get_local_temp_folder_path($current_timestamp).$initcond_filename);
		}
		
		/**
		 *
		 * $hawk_id :
		 * $precipitation_source_id :
		 * RETURN :
		 */
		public static function get_local_raindata_file_path($hawk_id, $precipitation_source_id){
			$raindata_filename = AuxFiles::get_raindata_file_name($precipitation_source_id);
			return(AuxFiles::get_local_folder_path($hawk_id).$raindata_filename);
		}
		
		/**
		 *
		 * $current_timestamp :
		 * $precipitation_source_id :
		 * RETURN :
		 */
		public static function get_local_temp_raindata_file_path($current_timestamp, $precipitation_source_id){
			$raindata_filename = AuxFiles::get_raindata_file_name($precipitation_source_id);
			return(AuxFiles::get_local_temp_folder_path($current_timestamp).$raindata_filename);
		}
		
		/**
		 *
		 * $hawkid :
		 * RETURN :
		 */
		public static function get_local_qvs_file_path($hawkid){
			return(AuxFiles::get_local_folder_path($hawkid).AuxFiles::get_qvs_file_name());
		}
		
		/**
		 * 
		 * $current_timestamp : 
		 * RETURN : 
		 */
		public static function get_local_temp_qvs_file_path($current_timestamp){
			return(AuxFiles::get_local_temp_folder_path($current_timestamp).AuxFiles::get_qvs_file_name());
		}
		
		/**
		 * $current_timestamp : 
		 * RETURN :
		 */
		public static function get_local_temp_rsvdbc_file_path($current_timestamp){
			return(AuxFiles::get_local_temp_folder_path($current_timestamp).AuxFiles::get_rsvdbc_file_name());
		}
		
		/**
		 * $current_timestamp : 
		 * RETURN :
		 */
		public static function get_local_temp_rsv_file_path($current_timestamp){
			return(AuxFiles::get_local_temp_folder_path($current_timestamp).AuxFiles::get_rsv_file_name());
		}
		
		/**
		 *
		 * $hawkid :
		 * RETURN :
		 */
		public static function get_local_evaporation_file_path($hawkid){
			return(AuxFiles::get_local_folder_path($hawkid).AuxFiles::get_evaporation_file_name());
		}
		
		/**
		 * 
		 * $current_timestamp : 
		 * RETURN : 
		 */
		public static function get_local_temp_evaporation_file_path($current_timestamp){
			return(AuxFiles::get_local_temp_folder_path($current_timestamp).AuxFiles::get_evaporation_file_name());
		}
		
		/**
		 *
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function get_local_temp_targz_file_path($current_timestamp){
			return("/tmp/".AuxFiles::get_input_targz_file_name($current_timestamp));
		}
		
		/**
		 *
		 * $current_timestamp :
		 * $model_id :
		 * RETURN : String.
		 */
		public static function get_local_metamodel_file_path($current_timestamp, $model_id){
			return(AuxFiles::get_local_temp_meta_folder_path($current_timestamp, "models").$model_id.".json");
		}
		
		/**
		 * 
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function get_local_metacomparisonmtx_file_path($current_timestamp){
			return(AuxFiles::get_local_temp_meta_folder_path($current_timestamp, "matrices")."Comparison_matrix.json");
		}
		
		/**
		 * 
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function get_local_metaevaluationmtx_file_path($current_timestamp){
			return(AuxFiles::get_local_temp_meta_folder_path($current_timestamp, "matrices")."Evaluation_matrix.json");
		}
		
		/**
		 * 
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function get_local_metarunset_file_path($current_timestamp){
			return(AuxFiles::get_local_temp_meta_folder_path($current_timestamp, "runset")."Runset.json");
		}
		
		/**
		 *
		 * $current_timestamp :
		 * $modelcomb_id :
		 * RETURN :
		 */
		public static function get_local_metacomb_hydrographpast_file_path($current_timestamp, $modelcomb_id){
			if (is_null($modelcomb_id)){
				return(AuxFiles::get_local_temp_meta_folder_path($current_timestamp, "modelcomb")."hydrogcomb.json");
			} else {
				return(AuxFiles::get_local_temp_meta_folder_path($current_timestamp, "modelcomb").$modelcomb_id.".json");
			}
		}
		
		/**
		 *
		 * $current_timestamp :
		 * $model_id :
		 * RETURN :
		 */
		public static function get_local_temp_output_snapshot_folder_path($current_timestamp){
			return(AuxFiles::get_local_temp_folder_path($current_timestamp)."outputs/");
		}
		
		/**
		 *
		 * $current_timestamp :
		 * $model_id :
		 * RETURN :
		 */
		public static function get_local_temp_output_snapshot_specific_folder_path($current_timestamp, $model_id){
			return(AuxFiles::get_local_temp_output_snapshot_folder_path($current_timestamp).$model_id."/");
		}
		
		/**
		 *
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function get_local_emailtext_file_path($current_timestamp){
			return(AuxFiles::get_local_temp_folder_path($current_timestamp)."email.txt");
		}
		
		/**
		 *
		 * RETURN : String
		 */
		public static function get_local_runset_waitingroom_folder_path(){
			return(FoldersDefs::WAITING_ROOM_FOLDER_PATH);
		}
		
		/**
		 * 
		 * $current_timestamp :
		 * RETURN : String
		 */
		public static function get_local_runset_waitingroom_targz_file_path($current_timestamp){
			return(FoldersDefs::WAITING_ROOM_FOLDER_PATH . AuxFiles::get_input_targz_file_name($current_timestamp));
		}
		
		// /*************** get remote file paths ***************/ //
		
		/**
		 *
		 * RETURN :
		 */
		public static function get_remote_central_folder_path(){
			return(FoldersDefs::DEST_CENTRAL_FOLDER_NAME);
		}
		
		/**
		 *
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function get_remote_folder_path($current_timestamp){
			// return("/Users/".$hawkid."/ifis_model_backtime/");
			return(FoldersDefs::DEST_FOLDER_PATH.$current_timestamp."/" );
		}
		
		/**
		 *
		 * $hillslope_model_id :
		 * $asynch_version :
		 * RETURN :
		 */
		public static function get_remote_initialcondition_repo_folder_path($hillslope_model_id, $asynch_version){
			return(FoldersDefs::DEST_INITCOND_REPO_FOLDER_PATH.$hillslope_model_id."/".$asynch_version."/");
		}
		
		/**
		 *
		 * $current_timestamp :
		 * $model_id :
		 * RETURN :
		 */
		public static function get_remote_output_snapshot_folder_path($current_timestamp, $model_id){
			return(FoldersDefs::DEST_FOLDER_PATH.$current_timestamp."/outputs/".$model_id."/");
		}
		
		/**
		 *
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function get_remote_topology_file_path(){
			echo("GOT -".AuxFiles::get_remote_central_folder_path()."-".AuxFiles::get_topology_file_name()."-.");
			return(AuxFiles::get_remote_central_folder_path().AuxFiles::get_topology_file_name()."777");
		}
		
		/**
		 *
		 * $current_timestamp :
		 * $hillslope_model_id :
		 * RETURN :
		 */
		public static function get_remote_demparameters_file_path($current_timestamp, $hillslope_model_id){
			if (($hillslope_model_id == 190)||($hillslope_model_id == 254)){
				return(AuxFiles::get_remote_central_folder_path()."all_iowa_190_254.prm");                 // TODO - make it properly
			} else {
				return(AuxFiles::get_remote_central_folder_path()."all_iowa_".$hillslope_model_id.".prm"); // TODO - make it properly
			}
			/*
			$remote_folder_path = AuxFiles::get_remote_folder_path($current_timestamp);
			$dempar_file_path = AuxFiles::get_dempars_file_name($hillslope_model_id);
			return($remote_folder_path.$dempar_file_path);
			*/
		}
		
		/**
		 * Gets the initial condition from snapshot retrieved from historical archive
		 * $current_timestamp : 
		 * $hillslope_model_id : 
		 * $initcond_timestamp : 
		 * RETURN : 
		 */
		public static function get_remote_initcond_raw_file_path($current_timestamp, $hillslope_model_id, $initcond_timestamp, $asynch_version){
			$remote_folder_path = AuxFiles::get_remote_initialcondition_repo_folder_path($hillslope_model_id, 
			                                                                             $asynch_version);
			$initcond_file_name = AuxFiles::get_initialcondition_file_name($hillslope_model_id, 
			                                                               $initcond_timestamp);
			return($remote_folder_path.$initcond_file_name);
		}
		
		/**
		 * Gets the initial condition from snapshot generated by other model from the same runset
		 * $current_timestamp :
		 * $hillslope_model_id :
		 * $initcond_timestamp :
		 * $model_id : Id of the model to which the initial condition will be set up
		 */
		public static function get_remote_initcond_mod_file_path($current_timestamp, $hillslope_model_id, $initcond_timestamp, $model_id, $asynch_version){
			$remote_folder_path = AuxFiles::get_remote_folder_path($current_timestamp);
			$initcond_file_name = AuxFiles::get_initialcondition_file_name($hillslope_model_id, $initcond_timestamp);  // TODO - check if it works
			
			// TODO - delete this debug
			// echo("Got Asynch Version '".$asynch_version."'.");
			
			// define source model id
			if(strpos($model_id, 'past') !== false){
				$source_model_id = str_replace("past", "prev", $model_id);
			} elseif(strpos($model_id, 'fore') !== false){
				$source_model_id = str_replace("fore", "past", $model_id);
				$source_model_id = str_replace("pastnon", "pastqpe", $source_model_id);
			} elseif(strpos($model_id, 'prev') !== false){
				return(AuxFiles::get_remote_initcond_raw_file_path($current_timestamp, $hillslope_model_id, $initcond_timestamp, $asynch_version));
			} else {
				return(null);
			}
			
			return(AuxFiles::get_remote_output_snapshot_file_path($source_model_id, $current_timestamp, $initcond_timestamp, 
																  $asynch_version, true));
		}
		
		/**
		 *
		 * $current_timestamp : 
		 * $precipitation_source_id :
		 * RETURN :
		 */
		public static function get_remote_raindata_file_path($current_timestamp, $precipitation_source_id){
			$remote_folder_path = AuxFiles::get_remote_folder_path($current_timestamp);
			$precipdata_file_name = AuxFiles::get_raindata_file_name($precipitation_source_id);
			return($remote_folder_path.$precipdata_file_name);
		}
		
		/**
		 *
		 * $current_timestamp : 
		 * RETURN :
		 */
		public static function get_remote_evaporation_file_path($current_timestamp){
			return(AuxFiles::get_remote_folder_path($current_timestamp).AuxFiles::get_evaporation_file_name());
		}
		
		/**
		 *
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function get_remote_qvs_file_path($current_timestamp){
			return(AuxFiles::get_remote_folder_path($current_timestamp).AuxFiles::get_qvs_file_name());
		}
		
		/**
		 *
		 * $model_id :
		 * $current_timestamp :
		 * $init_timestamp :
		 * $asynch_version :
		 * $force_snapshot :
		 * RETURN :
		 */
		public static function get_remote_output_snapshot_file_path($model_id, $current_timestamp, $init_timestamp, $asynch_version, $force_snapshot){
			$snapshot_file_name = AuxFiles::get_output_snapshot_file_name($init_timestamp, $asynch_version, $force_snapshot);
			if (!is_null($snapshot_file_name)){
				$temp_folder_path = AuxFiles::get_remote_output_snapshot_folder_path($current_timestamp, $model_id);
				return($temp_folder_path.$snapshot_file_name);
			} else {
				return(null);
			}
		}
		
		/**
		 * 
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function get_remote_scratch_file_path($current_timestamp){
			return(AuxFiles::get_remote_folder_path($current_timestamp)."tmp");
		}
		
		/**
		 *
		 * $current_timestamp :
		 * $model_id :
		 * RETURN : String.
		 */
		public static function get_remote_global_file_path($current_timestamp, $model_id){
			return(AuxFiles::get_remote_folder_path($current_timestamp).$model_id.".gbl");
		}
		
		/**
		 *
		 * $current_timestamp :
		 * $model_id :
		 * RETURN : String.
		 */
		public static function get_remote_metamodel_file_path($current_timestamp, $model_id){
			return(AuxFiles::get_remote_folder_path($current_timestamp).$model_id.".json");
		}
		
		// /****************** setup ref files ******************/ //
		
		/**
		 *
		 * $hawk_id :
		 * RETURN : None. Changes are performed in file system
		 */
		public static function setup_local_topology_file($hawk_id){
			// check if file already exists. If exists, go home
			$local_topology_file_path = AuxFiles::get_local_topology_file_path($hawk_id);
			if(file_exists($local_topology_file_path)){
				return;
			}
			// file does not exist. Create it.
			$template_topology_file_path = AuxFiles::get_topology_template_file_path();
			copy($template_topology_file_path, $local_topology_file_path);
			return;
		}
		
		/**
		 *
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function setup_local_temp_topology_file($current_timestamp){
			// check if file already exists. If exists, go home
			$local_topology_file_path = AuxFiles::get_local_temp_topology_file_path($current_timestamp);
			if(file_exists($local_topology_file_path)){
				return;
			}
			// file does not exist. Create it.
			$template_topology_file_path = AuxFiles::get_topology_template_file_path();
			copy($template_topology_file_path, $local_topology_file_path);
			return;
		}
		
		/**
		 * 
		 * $hawkid : 
		 * $hillslope_model_id : 
		 * RETURN : None. Changes are performed in file system
		 */
		public static function setup_local_demparameters_file($hawkid, $hillslope_model_id){
			// check if file already exists. If exists, go home
			$local_demparameters_file_path = AuxFiles::get_local_dempars_file_path($hawkid, $hillslope_model_id);
			if(file_exists($local_demparameters_file_path)){
				return;
			}
			// file does not exist. Create it.
			$template_demparameters_file_path = AuxFiles::get_demparameters_template_file_path($hillslope_model_id);
			copy($template_demparameters_file_path, $local_demparameters_file_path);
			return;
		}
		
		/**
		 *
		 * $current_timestamp :
		 * $hillslope_model_id :
		 * RETURN :
		 */
		public static function setup_local_temp_demparameters_file($current_timestamp, $hillslope_model_id){
			// check if file already exists. If exists, go home
			$local_demparameters_file_path = AuxFiles::get_local_temp_dempars_file_path($current_timestamp, $hillslope_model_id);
			if(file_exists($local_demparameters_file_path)){
				return;
			}
			// file does not exist. Create it.
			$template_demparameters_file_path = AuxFiles::get_demparameters_template_file_path($hillslope_model_id);
			copy($template_demparameters_file_path, $local_demparameters_file_path);
			return;
		}
		
		/**
		 * Discontinued function. Replaced by 'setup_local_temp_initcond_file()';
		 * TODO - Delete it.
		 * $hawkid : 
		 * $hillslope_model_id : 
		 * $initcond_timestamp : 
		 * RETURN : True if file is set up in the end, False otherwise
		 */
		/*
		public static function setup_local_initcond_file($hawkid, $hillslope_model_id, $initcond_timestamp){
			// define file name
			$initcond_filename = AuxFiles::get_initialcondition_file_name($hillslope_model_id, $initcond_timestamp);
			
			// define destination file and check if it already exists
			$initcond_temp_filepath = AuxFiles::get_local_initcondition_file_path($hawkid, $hillslope_model_id, $initcond_timestamp);
			if(file_exists($initcond_temp_filepath)){
				return(True);
			}
			
			// define source file and check it
			$initcond_repo_filepath = AuxFiles::get_initcond_repo_file_path($hillslope_model_id, $initcond_timestamp);
			if(!file_exists($initcond_repo_filepath)){
				echo("File '".$initcond_repo_filepath."' does not exist!");
				return(False);
			}
			
			// just copy from repository to temp folder
			return copy($initcond_repo_filepath, $initcond_temp_filepath);
		}
		*/
		
		/**
		 * Discontinued function. Copies a file from repository folder to the temporary folder
		 * TODO - Delete it.
		 * $current_timestamp  :
		 * $hillslope_model_id :
		 * $initcond_timestamp :
		 * RETURN : Boolean - TRUE if file was copied, FALSE otherwise.
		 */
		/*
		public static function setup_local_temp_initcond_file($current_timestamp, $hillslope_model_id, $initcond_timestamp){
			// define file name
			$initcond_filename = AuxFiles::get_initialcondition_file_name($hillslope_model_id, $initcond_timestamp);
			
			// define destination file and check if it already exists
			$initcond_temp_filepath = AuxFiles::get_local_temp_initcondition_file_path($current_timestamp, $hillslope_model_id, $initcond_timestamp);
			if(file_exists($initcond_temp_filepath)){
				return(True);
			}
			
			// define source file and check it
			$initcond_repo_filepath = AuxFiles::get_initcond_repo_file_path($hillslope_model_id, $initcond_timestamp);
			if(!file_exists($initcond_repo_filepath)){
				echo("File '".$initcond_repo_filepath."' does not exist...");
				return(False);
			}
			
			// just copy from repository to temp folder
			return copy($initcond_repo_filepath, $initcond_temp_filepath);
		}
		*/
		
		/**
		 *
		 * $hawkid :
		 * $precipitation_source_id :
		 * RETURN :
		 */
		public static function setup_local_raindata_file($hawkid, $precipitation_source_id){
			$raindata_template_filepath = AuxFiles::get_raindata_template_file_path($precipitation_source_id);
			$raindata_temp_filepath = AuxFiles::get_local_raindata_file_path($hawkid, $precipitation_source_id);
			if(!file_exists($raindata_temp_filepath)){
				copy($raindata_template_filepath, $raindata_temp_filepath);
			}
		}
		
		/**
		 *
		 * $current_timestamp : 
		 * $precipitation_source_id :
		 * RETURN :
		 */
		public static function setup_local_temp_raindata_file($current_timestamp, $precipitation_source_id){
			$raindata_template_filepath = AuxFiles::get_raindata_template_file_path($precipitation_source_id);
			$raindata_temp_filepath = AuxFiles::get_local_temp_raindata_file_path($current_timestamp, $precipitation_source_id);
			if(!file_exists($raindata_temp_filepath)){
				copy($raindata_template_filepath, $raindata_temp_filepath);
			}
		}
		
		/**
		 *
		 * $hawkid :
		 * RETURN :
		 */
		public static function setup_local_evaporation_file($hawkid){
			$evapot_template_filepath = AuxFiles::get_evaporation_template_file_path();
			$evapot_temp_filepath = AuxFiles::get_local_evaporation_file_path($hawkid);
			if(!file_exists($evapot_temp_filepath)){
				copy($evapot_template_filepath, $evapot_temp_filepath);
			}
		}
		
		/**
		 *
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function setup_local_temp_evaporation_file($current_timestamp){
			$evapot_template_filepath = AuxFiles::get_evaporation_template_file_path();
			$evapot_temp_filepath = AuxFiles::get_local_temp_evaporation_file_path($current_timestamp);
			if(!file_exists($evapot_temp_filepath)){
				copy($evapot_template_filepath, $evapot_temp_filepath);
			}
		}
		
		/**
		 *
		 * $hawkid :
		 * RETURN : None. Changes are performed in file system
		 */
		public static function setup_local_qvs_file($hawkid){
			$qvs_template_filepath = AuxFiles::get_qvs_template_file_path();
			$qvs_temp_filepath = AuxFiles::get_local_qvs_file_path($hawkid);
			if(!file_exists($qvs_temp_filepath)){
				copy($qvs_template_filepath, $qvs_temp_filepath);
			}
		}
		
		/**
		 *
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function setup_local_temp_qvs_file($current_timestamp){
			$qvs_template_filepath = AuxFiles::get_qvs_template_file_path();
			$qvs_temp_filepath = AuxFiles::get_local_temp_qvs_file_path($current_timestamp);
			if(!file_exists($qvs_temp_filepath)){
				copy($qvs_template_filepath, $qvs_temp_filepath);
			}
		}
		
		/**
		 *
		 * $current_timestamp :
		 * RETURN :
		 */
		public static function setup_local_temp_reservoir_files($current_timestamp){
			// copy dbc file
			$dbc_template_filepath = AuxFiles::get_rsvdbc_template_file_path();
			$dbc_temp_filepath = AuxFiles::get_local_temp_rsvdbc_file_path($current_timestamp);
			if(!file_exists($dbc_temp_filepath)){
				copy($dbc_template_filepath, $dbc_temp_filepath);
			}
			
			// copy rsv file
			$rsv_template_filepath = AuxFiles::get_rsv_template_file_path();
			$rsv_temp_filepath = AuxFiles::get_local_temp_rsv_file_path($current_timestamp);
			if(!file_exists($rsv_temp_filepath)){
				copy($rsv_template_filepath, $rsv_temp_filepath);
			}
		}
	}

?>
