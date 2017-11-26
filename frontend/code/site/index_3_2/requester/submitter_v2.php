<?php
	include_once("../common/class_FoldersDefs.php");
	include_once("class_AuxFiles.php");
	include_once("class_ModelRequest.php");

	// get arguments
	try{
		$runset_obj = new RunsetRequest($_POST);
		$mdlreq_objs = array();
		for($count_mdl=1; $count_mdl < $runset_obj->max_models + 1; $count_mdl++){
			// read form and basic check it
			$cur_mdl_request = ModelRequestFactory::getModelRequest($_POST, $count_mdl);
			if (is_null($cur_mdl_request)) {
				continue; 
			} else {
				array_push($mdlreq_objs, $cur_mdl_request); 
			}
		}
		
	} catch(Exception $exp) {
		echo("Exception: ".$exp);
		exit();
	}
	
	// definitions
	// TODO - remove it from here
	$run_script_path = "/Dedicated/IFC/back_time_script_git/backend_hpc/back_time_script/run_backtime.sh";
	$log_folder_path = FoldersDefs::LOG_FOLDER_PATH;
	
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
	
	// create all global files, general runset file and ancillary meta files
	$runset_obj->create_local_temp_dirs();
	$runset_obj->create_global_files($mdlreq_objs);
	$runset_obj->create_runset_meta_file();
	// MetaFilesCreator::create_comparison_mtx_meta_json_file($runset_obj, $mdlreq_objs);
	$runset_obj->create_comparison_mtx_empty_meta_file();
	// MetaFilesCreator::create_evaluation_mtx_meta_json_file($runset_obj, $mdlreq_objs);
	$runset_obj->create_evaluation_mtx_empty_meta_file();
	MetaFilesCreator::create_email_text_file($runset_obj);
	MetaFilesCreator::create_metacomb_hydrographpast($runset_obj, $mdlreq_objs);
	MetaFilesCreator::create_metacomb_sequencemaps($runset_obj);
	
	// compress all files silently
	$tar_fpath = AuxFiles::get_local_temp_targz_file_path($runset_obj->current_timestamp);
	$the_cmd = "cd /tmp/ && tar -czvf ";
	$the_cmd .= $tar_fpath." ";
	$the_cmd .= $runset_obj->current_timestamp."/*";
	exec($the_cmd, $retval);
	
	echo("Targzipping into '". $tar_fpath ."' from '". $runset_obj->current_timestamp ."'. ");
	
	// schedule the removal of all files from web server after 2 minutes
	schedule_files_deletion($runset_obj->current_timestamp, 2);
	
	// output message
	//echo("Generated files are available at '".AuxFiles::get_destination_url($user_hawkid)."' ([IIHR-50]".AuxFiles::get_local_folder_path($user_hawkid).").");
	echo("Generated files are at '[IIHR-50]".AuxFiles::get_local_temp_folder_path($runset_obj->current_timestamp)."'.\n");
	
	//**** Will push files to HPC ****//
	
	if(($runset_obj->what_run == "gencall") || ($runset_obj->what_run == "gencall04days")){
		// connect to the remote host and send them
		
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
	} else if (($runset_obj->what_run == "gencall06hloginless")||
	           ($runset_obj->what_run == "06p06f_loginless")||
			   ($runset_obj->what_run == "10p10f_loginless")) {
		// copy files to the waiting room
		
		// define destination, copy and change permissions
		$runset_waitingroom_targz_file_path = AuxFiles::get_local_runset_waitingroom_targz_file_path($runset_obj->current_timestamp);
		exec("cp ".AuxFiles::get_local_temp_targz_file_path($runset_obj->current_timestamp)." ".$runset_waitingroom_targz_file_path);
		exec("chmod ugo+rwx ".$runset_waitingroom_targz_file_path);
		
		// displaying message
		echo("Copied file from '".AuxFiles::get_local_temp_targz_file_path($runset_obj->current_timestamp));
		echo("' to '".$runset_waitingroom_targz_file_path."'. ");
		
	} else {
		echo("No command sent to HPC ('".$what_run."').");
	}
		
	return;
	
	
	/********************************* DEFS ***********************************/
	
	
	/**
	 * Creates a new comparison meta file
	 * $runset_id : String. Self-descriptive
	 * $glb_file_names : Array of strings. All .glb file names/paths to be included in the new .job file
	 * RETURN - String or null. Filepath of created file if it was possible, 'null' otherwise.
	 */
	function create_comparison_meta_json_file($runset_id, $current_timestamp, $model_ids, $model_hlm){
		// bellow: moved
		
		/*
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
		*/
	}
	
	/**
	 *
	 * $runset_id : 
	 * $current_timestamp :
	 * $model_ids :
	 * RETURN - 
	 */
	function create_evaluation_matrix_meta_file($runset_id, $current_timestamp, $model_ids){
		
		// defines final file path
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
		// bellow - moved
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
	 * $current_timestamp : 
	 * $runset_id : 
	 * $runset_title : 
	 * RETURN : 
	 */
	function create_runset_meta_json_file($current_timestamp, $runset_id, $runset_title, $ini_timestamp, $end_timestamp){
		// bellow - moved
		/*
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
		*/
	}
	
	/**
	 * Creates a simple text file containing only an email address
	 * $current_time : 
	 * $user_email : 
	 * RETURN :
	 */
	function create_email_text_file($current_timestamp, $user_email){
		// bellow - moved
		/*
		// defines file path
		$text_filepath = AuxFiles::get_local_emailtext_file_path($current_timestamp);
		
		// create file
		$fp = fopen($text_filepath, 'w');
		fwrite($fp, $user_email);
		fclose($fp);
		*/
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
