<?php

	include_once("class_AuxFiles.php");
	include_once("class_ModelRequest.php");

	// get arguments
	try{
		$runset_id = $_POST["runset_id"];
		$runset_title = $_POST["runset_title"];
		$timestamp_ini = $_POST["timestamp_ini"];
		$timestamp_end = $_POST["timestamp_end"];
		$server_addr = $_POST["server_addr"];
		$user_hawkid = $_POST["hawk_id"];
		$user_password = $_POST["hawk_pass"];
		$user_email = $_POST["email"];
		$max_models = $_POST["num_models"];
		$what_run = $_POST["what_run"];
		$asynch_version = $_POST["asynch_ver"];
	} catch(Exception $exp) {
		echo("Exception: ".$exp);
		exit();
	}
	
	// definitions
	$run_script_path = "/Dedicated/IFC/back_time_script_git/backend_hpc/back_time_script/run_backtime.sh";
	$log_folder_path = "/Dedicated/IFC/back_time_script_logs/";
	
	// establish the current time of request
	$current_time = time();
	
	// establish a mid time, if needed
	if($what_run == "06p06f_loginless"){
		$timestamp_mid = ($timestamp_ini + $timestamp_end)/2;
	} else {
		$timestamp_mid = null;
	}
	
	// TODO - delete debug
	/*
	echo("RI:".$runset_id."\n");
	echo("TI:".$timestamp_ini."\n");
	echo("TE:".$timestamp_end."\n");
	echo("SA:".$server_addr."\n");
	echo("UI:".$user_hawkid."\n");
	echo("UP:".$user_password."\n");
	echo("MM:".$max_models."\n");
	*/
	
	// creates temporary folder for the submission
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
	
	// for each possible model, generates the respective global, job, referenced files (when necessary) and meta file.
	$files_to_sent = array();
	$all_model_ids = array();
	$all_model_hlm = array();
	for($count_mdl=1; $count_mdl < $max_models + 1; $count_mdl++){
		if(isset($_POST["model_id_".$count_mdl])){
			
			// get most of fields
			$cur_model_id = $_POST["model_id_".$count_mdl];
			$cur_hillslope_model_id = $_POST["hillslope_model_".$count_mdl];
			$cur_precipitation_source_id = $_POST["precipitation_source_".$count_mdl];
			$cur_model_title = $_POST["model_title_".$count_mdl];
			$cur_model_desc = $_POST["model_desc_".$count_mdl];
			$cur_precipitation_source_id = $_POST["precipitation_source_".$count_mdl];
			
			// get parameters
			$cur_par_set = array();
			$count_par = 1;
			while(isset($_POST["model_par_".$count_mdl."_".$count_par])){
				$cur_par_set[] = $_POST["model_par_".$count_mdl."_".$count_par];
				$count_par = $count_par + 1;
			}
			
			// check title and description (fill if left empty)
			if (trim($cur_model_title) == ""){ $cur_model_title = $cur_model_id; }
			if (trim($cur_model_desc) == ""){ $cur_model_desc = $cur_model_title; }
			
			// add to description information of model parameters
			// TODO - eu aqui
			
			// create files for one-shot simulation
			$cur_files = create_files($runset_id, $cur_model_id, $timestamp_ini, $timestamp_end, 
									$cur_hillslope_model_id, $cur_precipitation_source_id, $cur_par_set,
									$cur_model_title, $cur_model_desc,
									$user_hawkid, $user_email, $current_time, $server_addr, $asynch_version);
			if(!is_null($cur_files)){
				$files_to_sent[] = $cur_files;
				$all_model_ids[] = $cur_model_id;
				$all_model_hlm[] = $cur_hillslope_model_id;
			}
			
			$gbl_file_prm = new GlobalFileRequest;
			$gbl_file_prm->runset_id = $runset_id;
			$gbl_file_prm->model_id = $cur_model_id;
			$gbl_file_prm->parameter_set = $cur_par_set;         // [string]: 
			$gbl_file_prm->hillslope_model_id = $cur_hillslope_model_id;    // integer:
			$gbl_file_prm->precip_source_id = $cur_precipitation_source_id; // integer:
			$gbl_file_prm->timestamp_cur = $current_time;        // integer: timestamp in seconds
			$gbl_file_prm->timestamp_ini = $timestamp_mid;       // integer: timestamp in seconds
			$gbl_file_prm->timestamp_end = $timestamp_end;       // integer: timestamp in seconds
			$gbl_file_prm->timestamp_initcond = $timestamp_ini;  // integer: timestamp in seconds
			$gbl_file_prm->asynch_version = $asynch_version;     // string:
			if (!is_null($timestamp_mid)){
				$cur_model_id = $gbl_file_prm->model_id."foreqpf";
				$gbl_file_prm_fore = clone $gbl_file_prm;
				$gbl_file_prm_fore->model_id = $cur_model_id;
				$gbl_file_prm_fore->timestamp_ini = $timestamp_mid;
				$gbl_file_prm_fore->timestamp_end = $timestamp_end;
				$cur_files = create_global($gbl_file_prm_fore);
				if(!is_null($cur_files)){
					echo("NOT NULL FOR '".$cur_model_id."'");
					$files_to_sent[] = $cur_files;
					$all_model_ids[] = $cur_model_id;
					$all_model_hlm[] = $cur_hillslope_model_id;
				} else {
					echo("NULL FOR '".$cur_model_id."'");
				}
			}
		} else {
			// echo("'"."model_id_".$count_mdl."' does not exist.");
		}
	}
	
	// create central .JOB file
	$gbl_filepaths = array();
	for($count_glb = 0; $count_glb < sizeof($files_to_sent); $count_glb++){
		$gbl_filepaths[] = $files_to_sent[$count_glb][0];
	}
	$central_job_path = create_central_job_file($runset_id, $user_hawkid, $user_email, $current_time, $server_addr, $gbl_filepaths, $asynch_version);
	
	// create ComparisonMatrix and Runset metafiles
	create_comparison_meta_json_file($runset_id, $current_time, $all_model_ids, $all_model_hlm);
	create_evaluation_matrix_meta_file($runset_id, $current_time, $all_model_ids, $all_model_hlm);
	create_metacomb_hydrographpast($runset_id, $current_time, $all_model_ids);
	create_runset_meta_json_file($current_time, $runset_id, $runset_title, $timestamp_ini, $timestamp_end);
	create_email_text_file($current_time, $user_email);
	
	// compress all files silently
	exec("cd /tmp/ && tar -czvf ".AuxFiles::get_local_temp_targz_file_path($current_time)." ".$current_time."/*", $retval);
	
	// schedule the removal of all files from web server after 2 minutes
	schedule_files_deletion($current_time, 2);
	
	// 
	//echo("Generated files are available at '".AuxFiles::get_destination_url($user_hawkid)."' ([IIHR-50]".AuxFiles::get_local_folder_path($user_hawkid).").");
	echo("Generated files are at '[IIHR-50]".AuxFiles::get_local_temp_folder_path($current_time)."'.\n");
	
	//**** Will push files to HPC ****//
	
	/* Generate a unique token: */
	$token = md5(uniqid(rand(),1));
	
	/* This file is used for storing tokens. One token per line. */
	$file = "/tmp/md5s.txt";
	if(file_exists($file))
		unlink($file);
	
	if( !($fd = fopen($file,"a")) )
        die("Could not open $file!");

	if( !(flock($fd,LOCK_EX)) )
        die("Could not aquire exclusive lock on $file!");

	if( !(fwrite($fd,$token."\n")) )
        die("Could not write to $file!");

	if( !(flock($fd,LOCK_UN)) )
        die("Could not release lock on $file!");

	if( !(fclose($fd)) )
        die("Could not close file pointer for $file!");

	/* Parse out the current working directory for this script. */
	$cwd = substr($_SERVER['PHP_SELF'],0,strrpos($_SERVER['PHP_SELF'],"/"));
	
	$link = "http://".$_SERVER['HTTP_HOST'].$cwd."/descarca.php?q=$token";
	// echo($link." . ");
	
	// forcing DUO authentication to happen via app
	$last_line = system("export DUO_PASSCODE=push", $retval);
	
	// connect to the remote host
	if(($what_run == "gencall") || ($what_run == "gencall04days")){
		if(!($ssh_con = ssh2_connect($server_addr, 22))){
			echo("Fail: unable to establish connection with SSH server.");
			exit();
		} else {
			// try to authenticate with username root, password secretpassword
			if(!ssh2_auth_password($ssh_con, $user_hawkid, $user_password)) {
				echo("Fail: unable to authenticate.");
				exit();
			} else {
				
				$hpc_arguments = $link." ".$current_time." ".$timestamp_ini." ".$runset_id." ".$user_hawkid." ".$user_password;
				$hpc_arguments_fake = $link." ".$current_time." ".$timestamp_ini." ".$runset_id." ".$user_hawkid." *PASSWORD*";
				
				// DON'T TOUCHE THE NEXT LINE. MY DOG WILL BITE YOU.
				$hpc_command = 'bash /Dedicated/IFC/back_time_script/run_backtime.sh '.$hpc_arguments.' > /Dedicated/IFC/back_time_script/logs.txt';
				$hpc_command_fk = "bash /Dedicated/IFC/back_time_script/run_backtime.sh ".$hpc_arguments_fake." > /Dedicated/IFC/back_time_script/logs.txt";
				
				$hpc_command = 'bash '.$run_script_path.' '.$hpc_arguments.' > '.$log_folder_path.'log_requester.txt';
				$hpc_command_fk = "bash ".$run_script_path." ".$hpc_arguments_fake." > ".$log_folder_path."log_requester.txt";
				
				$output_stream = ssh2_exec($ssh_con, $hpc_command);
				
				echo("Command: '".$hpc_command_fk."'. ");
				echo("Command sent to HPC.");
			}
		}
	} else if ($what_run == "gencall06hloginless") {
		// copy files
		$runset_waitingroom_targz_file_path = AuxFiles::get_local_runset_waitingroom_targz_file_path($current_time);
		exec("cp ".AuxFiles::get_local_temp_targz_file_path($current_time)." ".$runset_waitingroom_targz_file_path);
		exec("chmod ugo+rwx ".$runset_waitingroom_targz_file_path);
		echo("Copied file from '".AuxFiles::get_local_temp_targz_file_path($current_time)."' to '".$runset_waitingroom_targz_file_path."'. ");
	} else {
		echo("No command sent to HPC ('".$what_run."').");
	}
		
	return;
	
	
	/********************************* DEFS ***********************************/
	
	/**
	 * Creates a .glb, a .job and a .json file for specified model.
	 * $runset_id : String. Self-descriptive.
	 * $model_id : String. Self-descriptive.
	 * $timestamp_ini : Integer. Initial timestamp of simulation.
	 * $timestamp_mid : Integer. Intermediate timestamp. If none: single model run.
	 * $timestamp_end : Integer. Final timestamp of simulation.
	 * $hillslope_model_id : Integer. Hillslope model used (190, 254, 262...).
	 * $precipitation_source_id : String. Self-descriptive.
	 * $par_set : Array of strings. Values of all parameters in the proper sequence.
	 * $model_title : String. Title of the model.
	 * $model_desc : String. Description of the model.
	 * $hawk_id : String. Self-descriptive.
	 * $current_timestamp :
	 * $server_addr :
	 * RETURN - Array of strings or null. Filepath of created files if it was successful, null otherwise.
	 */
	function create_files($runset_id, $model_id, $timestamp_ini, $timestamp_end, $hillslope_model_id, $precipitation_source_id, $par_set, 
						  $model_title, $model_desc, $hawk_id, $email, $current_timestamp, $server_addr, $asynch_version){
		
		// basic check
		if (($asynch_version != "1.1")&&($asynch_version != "1.2")) {return(null);}
		
		
			// establish final gbl and job files
			$glb_final_filename = $model_id.".gbl";
			$glb_final_filepath = AuxFiles::get_local_temp_folder_path($current_timestamp).$glb_final_filename;
			$job_final_filepath = AuxFiles::get_local_temp_folder_path($current_timestamp).$model_id.".job";
			$json_final_filepath = AuxFiles::get_local_metamodel_file_path($current_timestamp, $model_id);
			
			// establish initial condition timestamp
			$initcond_timestamp = AuxFiles::get_initcond_timestamp($timestamp_ini);
			
			// /****************** create GBL file ******************/ //
			
			// read template file
			$gbl_final_content = file(AuxFiles::GLB_TEMPLATE_FILEPATH);
			
			// edit template content
			if ($asynch_version == "1.1"){
				$gbl_final_content[1] = $hillslope_model_id." ".(($timestamp_end - $timestamp_ini)/60)."\n";
			} elseif ($asynch_version == "1.2") {
				$datetime_ini = date('Y-m-d H:i', $timestamp_ini);
				$datetime_end = date('Y-m-d H:i', $timestamp_end);
				$gbl_final_content[1] = $hillslope_model_id."\n".$datetime_ini."\n".$datetime_end."\n";
			}
			$gbl_final_content[18] = sizeof($par_set)." ".implode(" ", $par_set)."\n";                               // replace global parameters
			// $gbl_final_content[26] = "1 0 ".AuxFiles::get_remote_topology_file_path($current_timestamp)."\n";        // replace topology source
			$gbl_final_content[29] = "0 ".AuxFiles::get_remote_demparameters_file_path($current_timestamp, 
																					   $hillslope_model_id)."\n";    // replace DEM parameters
			$gbl_final_content[33] = "4 ".AuxFiles::get_remote_initcond_file_path($current_timestamp, 
																				  $hillslope_model_id, 
																				  $initcond_timestamp)."\n";         // replace initial state
			$gbl_final_content[40] = "3 ".AuxFiles::get_remote_raindata_file_path($current_timestamp, 
																				  $precipitation_source_id)."\n";    // replace rain source
			$gbl_final_content[41] = AuxFiles::get_raindbc_raininstances($precipitation_source_id)." ".AuxFiles::get_raindbc_raininterval($precipitation_source_id)." ".$timestamp_ini." ".$timestamp_end."\n";   
																													 // replace rain interval
			$gbl_final_content[44] = "7 ".AuxFiles::get_remote_evaporation_file_path($current_timestamp)."\n";       // replace evapo-transpiration 
			$gbl_final_content[45] = $timestamp_ini." ".AuxFiles::FARAWAY_FUTURE."\n";                               // replace evapo-transpiration interval
			$gbl_final_content[48] = "0\n";                                                                          // replace reservoirs data source
			$gbl_final_content[49] = "\n";                                                                           // replace reservoirs data interval
			$gbl_final_content[54] = "3 ".AuxFiles::get_remote_qvs_file_path($current_timestamp)."\n";               // replace QVS
			$gbl_final_content[57] = "0 \n";                                                                         // replace reservoirs reference
			$gbl_final_content[77] = "4 60 ".AuxFiles::get_remote_output_snapshot_file_path($model_id, 
																							$current_timestamp, 
																							$timestamp_ini,
																							$asynch_version)."\n";   // replace output snapshot
			$gbl_final_content[80] = AuxFiles::get_remote_scratch_file_path($current_timestamp)."\n";                // 

			// save edited template into file
			$fp = fopen($glb_final_filepath, 'w');
			foreach ($gbl_final_content as $key => $value){
				fwrite($fp, $value);
			}
			fclose($fp);
			
			// create folder in which output snapshots are going to be stored in the future
			// echo("Creating folder: '".AuxFiles::get_local_temp_output_snapshot_specific_folder_path($current_timestamp, $model_id)."'.");
			mkdir(AuxFiles::get_local_temp_output_snapshot_specific_folder_path($current_timestamp, $model_id), 0777, true);
			
			// /****************** create JOB file ******************/ //
			
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
			$job_final_content[13] = "\nmpirun -np ".$job_noc." ".$asynch_call." ".$glb_file_path;                    // replace system call command
			
			// save edited template into file
			$fp = fopen($job_final_filepath, 'w');
			foreach ($job_final_content as $key => $value){
				fwrite($fp, $value);
			}
			fclose($fp);
			
			// /************** set up referenced files **************/ //
			
			/*
			AuxFiles::setup_local_topology_file($hawk_id);
			AuxFiles::setup_local_demparameters_file($hawk_id, $hillslope_model_id);
			AuxFiles::setup_local_initcond_file($hawk_id, $hillslope_model_id, $initcond_timestamp);
			AuxFiles::setup_local_raindata_file($hawk_id, $precipitation_source_id);
			AuxFiles::setup_local_evaporation_file($hawk_id);
			AuxFiles::setup_local_qvs_file($hawk_id);
			*/
			
			AuxFiles::setup_local_temp_topology_file($current_timestamp);
			AuxFiles::setup_local_temp_demparameters_file($current_timestamp, $hillslope_model_id);
			AuxFiles::setup_local_temp_initcond_file($current_timestamp, $hillslope_model_id, $initcond_timestamp);
			AuxFiles::setup_local_temp_raindata_file($current_timestamp, $precipitation_source_id);
			AuxFiles::setup_local_temp_evaporation_file($current_timestamp);
			AuxFiles::setup_local_temp_qvs_file($current_timestamp);
			
			// /***************** create JSON file ******************/ //
			
			// read template file and edits its content
			// $metamdl_file_path = AuxFiles::get_remote_metamodel_file_path($current_timestamp, $model_id);
			$json_final_content = file(AuxFiles::METAMODEL_TEMPLATE_FILEPATH);
			$all_prods_id = "\"".implode("\",\"", AuxFiles::get_sc_product_ids($hillslope_model_id))."\"";
			$all_reprs_id = "\"".implode("\",\"", AuxFiles::get_sc_representation_ids($hillslope_model_id))."\"";
			$json_final_content[1] = str_replace("SC_MODEL_ID", $model_id, $json_final_content[1]);   
			$json_final_content[2] = str_replace("MODEL_TITLE", $model_title, $json_final_content[2]);
			$json_final_content[3] = str_replace("MODEL_DESC", $model_desc, $json_final_content[3]);
			$json_final_content[4] = str_replace("SC_PRODUCT_IDS", $all_prods_id, $json_final_content[4]);
			$json_final_content[5] = str_replace("SC_REPRESENTATION_IDS", $all_reprs_id, $json_final_content[5]);
			$json_final_content[6] = str_replace("BINGEN_SING_SCRIPT", AuxFiles::get_sing_script_path($hillslope_model_id), $json_final_content[6]);
			$json_final_content[7] = str_replace("BINGEN_HIST_SCRIPT", AuxFiles::get_hist_script_path($hillslope_model_id), $json_final_content[7]);
			
			// save edited template into file
			$fp = fopen($json_final_filepath, 'w');
			foreach ($json_final_content as $key => $value){
				fwrite($fp, $value);
			}
			fclose($fp);
		
		// /*********************** return **********************/ //
		return(array($glb_final_filepath, $job_final_filepath));
	}
	
	/**
	 *
	 *
	 */
	function create_global($mdl_requester_obj){
		
		// read template file
		$gbl_final_content = file(AuxFiles::GLB_TEMPLATE_FILEPATH);
		
		// establish final gbl and job files
		$glb_final_filename = $mdl_requester_obj->model_id.".gbl";
		$glb_final_filepath = AuxFiles::get_local_temp_folder_path($mdl_requester_obj->timestamp_cur).$glb_final_filename;
		$job_final_filepath = AuxFiles::get_local_temp_folder_path($mdl_requester_obj->timestamp_cur).$mdl_requester_obj->model_id.".job";
		
		// edit template content
		if ($mdl_requester_obj->asynch_version == "1.1"){
			$gbl_final_content[1] = $mdl_requester_obj->hillslope_model_id." ".(($mdl_requester_obj->timestamp_end - $mdl_requester_obj->timestamp_ini)/60)."\n";
		} elseif ($mdl_requester_obj->asynch_version == "1.2") {
			$datetime_ini = date('Y-m-d H:i', $mdl_requester_obj->timestamp_ini);
			$datetime_end = date('Y-m-d H:i', $mdl_requester_obj->timestamp_end);
			$gbl_final_content[1] = $mdl_requester_obj->hillslope_model_id."\n".$datetime_ini."\n".$datetime_end."\n";
		}
		$gbl_final_content[18] = sizeof($mdl_requester_obj->parameter_set)." ".implode(" ", $mdl_requester_obj->parameter_set)."\n";                               // replace global parameters
		// $gbl_final_content[26] = "1 0 ".AuxFiles::get_remote_topology_file_path($current_timestamp)."\n";     // replace topology source
		$gbl_final_content[29] = "0 ".AuxFiles::get_remote_demparameters_file_path($mdl_requester_obj->timestamp_cur, 
																				   $mdl_requester_obj->hillslope_model_id)."\n";
																				                                 // replace DEM parameters
		$gbl_final_content[33] = "4 ".AuxFiles::get_remote_initcond_file_path($mdl_requester_obj->timestamp_cur, 
																			  $mdl_requester_obj->hillslope_model_id, 
																			  $mdl_requester_obj->timestamp_initcond)."\n";
																			                                     // replace initial state
		$gbl_final_content[40] = "3 ".AuxFiles::get_remote_raindata_file_path($mdl_requester_obj->timestamp_cur, 
																			  $mdl_requester_obj->precip_source_id)."\n";
																			                                     // replace rain source
		$gbl_final_content[41] = AuxFiles::get_raindbc_raininstances($mdl_requester_obj->precip_source_id)." ".AuxFiles::get_raindbc_raininterval($mdl_requester_obj->precip_source_id)." ".$mdl_requester_obj->timestamp_ini." ".$mdl_requester_obj->timestamp_end."\n";   
																												 // replace rain interval
		$gbl_final_content[44] = "7 ".AuxFiles::get_remote_evaporation_file_path($mdl_requester_obj->timestamp_cur)."\n";
		                                                                                                         // replace evapo-transpiration 
		$gbl_final_content[45] = $mdl_requester_obj->timestamp_ini." ".AuxFiles::FARAWAY_FUTURE."\n";            // replace evapo-transpiration interval
		$gbl_final_content[48] = "0\n";                                                                          // replace reservoirs data source
		$gbl_final_content[49] = "\n";                                                                           // replace reservoirs data interval
		$gbl_final_content[54] = "3 ".AuxFiles::get_remote_qvs_file_path($mdl_requester_obj->timestamp_cur)."\n";// replace QVS
		$gbl_final_content[57] = "0 \n";                                                                         // replace reservoirs reference
		$gbl_final_content[77] = "4 60 ".AuxFiles::get_remote_output_snapshot_file_path($mdl_requester_obj->model_id, 
																						$mdl_requester_obj->timestamp_cur, 
																						$mdl_requester_obj->timestamp_ini,
																						$mdl_requester_obj->asynch_version)."\n";   // replace output snapshot
		$gbl_final_content[80] = AuxFiles::get_remote_scratch_file_path($mdl_requester_obj->timestamp_cur)."\n"; // 

		// save edited template into file
		$fp = fopen($glb_final_filepath, 'w');
		foreach ($gbl_final_content as $key => $value){
			fwrite($fp, $value);
		}
		fclose($fp);
			
		// create folder in which output snapshots are going to be stored in the future
		// echo("Creating folder: '".AuxFiles::get_local_temp_output_snapshot_specific_folder_path($current_timestamp, $model_id)."'.");
		mkdir(AuxFiles::get_local_temp_output_snapshot_specific_folder_path($mdl_requester_obj->timestamp_cur, 
		                                                                    $mdl_requester_obj->model_id), 0777, true);
																			
		// /*********************** return **********************/ //
		return(array($glb_final_filepath, $job_final_filepath));
	}
	
	/**
	 * Creates a new job file that will run sequentially all .glb files
	 * $runset_id : String. Self-descriptive
	 * $hawk_id : String. Self-descriptive
	 * $server_addr : String. Server address.
	 * $glb_file_names : Array of strings. All .glb file names/paths to be included in the new .job file
	 * RETURN : String or null. Filepath of created file if it was possible, 'null' otherwise.
	 */
	function create_central_job_file($runset_id, $hawk_id, $email, $current_timestamp, $server_addr, $glb_file_names, $asynch_version){
		
		// $job_final_filepath = AuxFiles::get_local_folder_path($hawk_id).$runset_id.".job";
		$job_final_filepath = AuxFiles::get_local_temp_folder_path($current_timestamp).$runset_id.".job";
		
		// define server's ASYNCH binary file location and the number of cores
		$job_cpn = AuxFiles::get_cpn($server_addr);
		$job_noc = AuxFiles::get_noc($server_addr);
		$asynch_call = AuxFiles::get_asynch_bin_path($server_addr, $asynch_version);
		
		// read template file and edits its content
		$job_final_content = file(AuxFiles::JOB_TEMPLATE_FILEPATH);
		$job_final_content[1] = "#$ -N ".$runset_id."\n";                                                          // replace run id
		$job_final_content[2] = "#$ -o /Dedicated/IFC/back_time/".$current_timestamp."/".$runset_id."_o.txt\n";    // replace output log file name
		$job_final_content[3] = "#$ -e /Dedicated/IFC/back_time/".$current_timestamp."/".$runset_id."_e.txt\n";    // replace error log file name
		$job_final_content[4] = "#$ -pe ".$job_cpn." ".$job_noc."\n";      
		if (trim($email) != ""){
			$job_final_content[5] = "#$ -m bea\n";                                                              // replace something here
			$job_final_content[6] = "#$ -M ".$email."\n";                                                       // replace contact email
		} else {
			$job_final_content[5] = "\n";                                                                       // replace something here
			$job_final_content[6] = "\n";                                                                       // replace contact email
		}
		$job_final_content[7] = "#$ -q ".AuxFiles::get_queue($server_addr)."\n";                                // replace server queue
		
		// remove templates call
		// $job_final_content[13] = "";
		
		// add as many calls as apparently necessary
		$folder_path = AuxFiles::get_remote_folder_path($current_timestamp);
		$all_calls = "";
		for($glb_files_count = 0; $glb_files_count < sizeof($glb_file_names); $glb_files_count++){
			// $job_final_content[] = "\nmpirun -np ".$job_noc." ".$asynch_call." ".$folder_path.basename($glb_file_names[$glb_files_count]."\n");
			$all_calls .= "mpirun -np ".$job_noc." ".$asynch_call." ".$folder_path.basename($glb_file_names[$glb_files_count]."\n");
		}
		$job_final_content[13] = $all_calls;
		
		// save edited template into file
		$fp = fopen($job_final_filepath, 'w');
		foreach ($job_final_content as $key => $value){
			fwrite($fp, $value);
		}
		fclose($fp);
		
		// just return
		return($job_final_filepath);
	}
	
	/**
	 * Creates a new comparison meta file
	 * $runset_id : String. Self-descriptive
	 * $glb_file_names : Array of strings. All .glb file names/paths to be included in the new .job file
	 * RETURN - String or null. Filepath of created file if it was possible, 'null' otherwise.
	 */
	function create_comparison_meta_json_file($runset_id, $current_timestamp, $model_ids, $model_hlm){
		// $json_final_filepath = AuxFiles::get_local_temp_folder_path($current_timestamp)."Comparison_matrix.json";
		$json_final_filepath = AuxFiles::get_local_metacomparisonmtx_file_path($current_timestamp);
		
		// read template file and separates main line
		$json_final_content = file(AuxFiles::METACOMPARISON_TEMPLATE_FILEPATH);
		$template_line = $json_final_content[1];
		
		// generates all internal lines
		$comp_lines = array();
		foreach($model_ids as $key_1 => $model_id1){
			foreach($model_ids as $key_2 => $model_id2){
				if($key_1 != $key_2){
					// echo("Replacing 'MODELID01' in '".$template_line."'");
					$cur_line = str_replace("MODELID01", $model_id1, $template_line);
					$cur_line = str_replace("MODELID02", $model_id2, $cur_line);
					$repr_ids = AuxFiles::get_sc_comparison_product_ids($model_hlm[$key_1], $model_hlm[$key_2]);
					$cur_line = str_replace("SC_PRODUCT_IDS", "\"".implode("\",\"", $repr_ids)."\"", $cur_line);
					$comp_lines[] = $cur_line;
				}
			}
		}
		$json_final_content[1] = implode("		,\n", $comp_lines);
		
		// write all internal lines
		$fp = fopen($json_final_filepath, 'w');
		foreach ($json_final_content as $key => $value){
			fwrite($fp, $value);
		}
		fclose($fp);
	}
	
	/**
	 *
	 * $runset_id : 
	 * $current_timestamp :
	 * $model_ids :
	 * RETURN - 
	 */
	function create_evaluation_matrix_meta_file($runset_id, $current_timestamp, $model_ids){
		
		// reads all possible evaluations
		$json_final_filepath = AuxFiles::get_local_metaevaluationmtx_file_path($current_timestamp);
		
		// read template file and separates main line
		$json_final_content = file(AuxFiles::METAEVALUATION_TEMPLATE_FILEPATH);
		$template_line = $json_final_content[1];
		
		// reads reference 
		$possible_eval_str = file_get_contents(AuxFiles::EVALUATIONS_POSSIBLE_FILEPATH);
		$possible_eval_obj = json_decode($possible_eval_str);
		$possible_eval_list = $possible_eval_obj->evaluation_matrix_options;
		
		// generates all internal lines
		$comp_lines = array();
		foreach($possible_eval_list as $key_1 => $possible_eval_id){
			$cur_models_id = array();  // could have an specific step here
			foreach ($model_ids as $cur_idx => $cur_model_id) {
				$cur_models_id[$cur_idx] = "\"".$cur_model_id."\"";
			}
			
			$cur_models_id_str = "[".implode(",",$cur_models_id)."]";
			
			$cur_line = "		".str_replace("EVALUATIONID_REFERENCEID", $possible_eval_id, trim($template_line));
			$cur_line = str_replace("SC_MODEL_IDS", $cur_models_id_str, $cur_line);
			$comp_lines[] = $cur_line;
		}
		
		// replace template line in template
		$json_final_content[1] = implode(",\n", $comp_lines)."\n";
		
		// write all internal lines
		$fp = fopen($json_final_filepath, 'w');
		foreach ($json_final_content as $key => $value){
			fwrite($fp, $value);
		}
		fclose($fp);
	}
	
	/**
	 *
	 * $runset_id :
	 * $current_timestamp :
	 * $model_ids :
	 * RETURN : 
	 */
	function create_metacomb_hydrographpast($runset_id, $current_timestamp, $model_ids){
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
	}
	
	/**
	 *
	 * $current_timestamp : 
	 * $runset_id : 
	 * $runset_title : 
	 * RETURN : 
	 */
	function create_runset_meta_json_file($current_timestamp, $runset_id, $runset_title, $ini_timestamp, $end_timestamp){
		$json_final_filepath = AuxFiles::get_local_metarunset_file_path($current_timestamp);
		
		// read template file and separates main line
		$json_final_content = file(AuxFiles::METARUNSET_TEMPLATE_FILEPATH);
		// echo("Replacing 'RUNSET_ID' in ".$json_final_content[1]);
		$json_final_content[1] = str_replace("RUNSET_ID", $runset_id, $json_final_content[1]);
		// echo("Replacing 'RUNSET_TITLE' in ".$json_final_content[2]);
		$json_final_content[2] = str_replace("RUNSET_TITLE", $runset_title, $json_final_content[2]);
		$json_final_content[3] = str_replace("\"TIMESTAMP_MIN\"", $ini_timestamp, $json_final_content[3]);
		$json_final_content[4] = str_replace("\"TIMESTAMP_MAX\"", $end_timestamp, $json_final_content[4]);
		
		// write all internal lines
		$fp = fopen($json_final_filepath, 'w');
		foreach ($json_final_content as $key => $value){
			fwrite($fp, $value);
		}
		fclose($fp);
	}
	
	/**
	 * Creates a simple text file containing only an email address
	 * $current_time : 
	 * $user_email : 
	 * RETURN :
	 */
	function create_email_text_file($current_timestamp, $user_email){
		// defines file path
		$text_filepath = AuxFiles::get_local_emailtext_file_path($current_timestamp);
		
		// create file
		$fp = fopen($text_filepath, 'w');
		fwrite($fp, $user_email);
		fclose($fp);
	}
	
	/**
	 *
	 * $current_timestamp :
	 * $delta_minutes :
	 * RETURN : None. Changes are performed in crontab
	 */
	function schedule_files_deletion($current_timestamp, $delta_minutes){
		date_default_timezone_set('America/Chicago');
		$delete_timestamp = $current_timestamp + ($delta_minutes * 60);
		$minutes = date('i', $delete_timestamp);
		$hours = date('G', $delete_timestamp);
		$day = date('j', $delete_timestamp);
		
		$cmd01 = "echo \"".$minutes." ".$hours." ".$day." * * rm ".AuxFiles::get_local_temp_targz_file_path($current_timestamp)."\"";
		$cmd02 = "echo \"".$minutes." ".$hours." ".$day." * * rm -r ".AuxFiles::get_local_temp_folder_path($current_timestamp)."\"";
		
		shell_exec("crontab -r");
		shell_exec("crontab -l | { cat; ".$cmd01."; } | crontab -");
		shell_exec("crontab -l | { cat; ".$cmd02."; } | crontab -");
		
		// echo("Executting '".$cmd01."' and '".$cmd02."'");
	}
?>
