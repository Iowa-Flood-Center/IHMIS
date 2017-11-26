<?php
	header('Content-type: application/json');
	include_once("class_AuxFiles.php");
	include_once("../common/class_FoldersDefs.php");
	include_once("class_DatabaseMethods.php");

	// from a given timestamp, shows which rain products and hillslopes are available to be used 
	//                                                                           (in JSON FORMAT)

	// //////////////////////////////////////// CONS //////////////////////////////////////// //
	
	$default_asynch_version = "1.3";
	
	// //////////////////////////////////////// OUTP //////////////////////////////////////// //
	$output_json = array(
		"rainprod_ids" => array(),
		"hillslope_ids" => array(),
		"reservoir_link_ids" => array());
	
	// //////////////////////////////////////// ARGS //////////////////////////////////////// //
	
	// basic check - argument
	if ((!isset($_GET["timestamp_ini"])) || (!isset($_GET["timestamp_end"]))){
		$json_obj = json_encode($output_json);
		echo($json_obj);
		exit();
	}
	
	// get arguments
	$ini_timestamp = $_GET["timestamp_ini"];
	$end_timestamp = $_GET["timestamp_end"];
	if (!isset($_GET["asynch_version"])){
		$asynch_version = $default_asynch_version;
	} else {
		$asynch_version = $_GET["asynch_version"];
	}
	
	// //////////////////////////////////////// CLAS //////////////////////////////////////// //
	
	/**
	 *
	 * $timestamp_ini :
	 * $asynch_vers :
	 * $output_json :
	 * RETURN : 
	 */
	function fill_hillslope_model($timestamp_ini, $asynch_vers){
		global $output_json;           // this is dirt and makes me fell bad
		
		// define "10 days" initial condition timestamp
		$initcond_timestamp = AuxFiles::get_initcond_timestamp($timestamp_ini);
		
		// read content in initial conditions catalogue file
		$json_str = file_get_contents(FoldersDefs::INITIALSTATES_HDF5_LIST_FILEPATH);
		$json_data = json_decode($json_str, true);
		
		// check if it exists in the dictionary
		if (!array_key_exists($initcond_timestamp, $json_data)){
			return;
		}
		
		// check if version is present
		if (!array_key_exists($asynch_vers, $json_data[$initcond_timestamp])){
			return;
		}
		
		// push push
		$all_files = $json_data[$initcond_timestamp][$asynch_vers];
		foreach($all_files as $cur_file){
			array_push($output_json["hillslope_ids"], $cur_file);
		}
		
		if(true){ return; }
		
		
		// list all hillslope models
		// $sub_dirs = glob(FoldersDefs::INITIALSTATES_HDF5_FOLDERPATH . '/*' , GLOB_ONLYDIR);
		
		foreach($sub_dirs as $cur_sub_dir){
			
			// building folder path and separating the hillslope model id
			$cur_sub_dir_correct = str_replace("//", "/", $cur_sub_dir)."/";
			$splited_path = explode("/", $cur_sub_dir_correct);
			$cur_hillslope_model_id = $splited_path[sizeof($splited_path) - 2];
			
			// define "10 days" initial condition timestamp and check if file exists
			$initcond_timestamp = AuxFiles::get_initcond_timestamp($timestamp_ini);
			$initcond_repofile_path = AuxFiles::get_initcond_repo_file_path($cur_hillslope_model_id,
																			$initcond_timestamp);
			if (file_exists($initcond_repofile_path)){
				array_push($output_json["hillslope_ids"], $cur_hillslope_model_id);
			} // else{ echo("Not found:".$initcond_repofile_path." (from ".$timestamp_ini.")\n"); }
			
			// echo($cur_sub_dir_correct." -> ".$cur_hillslope_model_id."\n");
		}
	}
	
	/**
	 *
	 * $timestamp : 
	 * $output_json :
	 * RETURN :
	 */
	function fill_precipitation_products($timestamp_ini, $timestamp_end){
		global $output_json;  // this is dirt and makes me fell bad
		
		$precip_ids = array("st4", "mrms", "ifc");
		
		// open db connection
		$db_conn = DatabaseMethods::open_db_connection(DatabaseMethods::DB_PREC_FLAG);
		
		foreach($precip_ids as $cur_precip_id){
			// echo("Testing '".$cur_precip_id."'. ");
			if (DatabaseMethods::is_interval_available($cur_precip_id, $timestamp_ini, 
												   $timestamp_end, $db_conn)){
				array_push($output_json["rainprod_ids"], $cur_precip_id);
			}
		}
		
		// close db connection
		pg_close($db_conn);
	}
	
	/**
	 *
	 * $ini_timestamp : 
	 * $end_timestamp : 
	 * RETURN : 
	 */
	function fill_reservoirs_data($timestamp_ini, $timestamp_end){
		global $output_json;  // this is dirt and makes me fell bad
		
		// open db connection
		$db_conn = DatabaseMethods::open_db_connection(DatabaseMethods::DB_RSRV_FLAG);
		
		$available_link_ids = DatabaseMethods::get_available_reservoirs($timestamp_ini,
																		$timestamp_end, 
																		$db_conn);
		
		if(sizeof($available_link_ids) > 0){
			foreach($available_link_ids as $cur_link_id){
				array_push($output_json["reservoir_link_ids"], intval($cur_link_id));
			}
		}
		
		// close db connection
		pg_close($db_conn);
	}
	
	// //////////////////////////////////////// CALL //////////////////////////////////////// //
	
	// fill and print
	fill_hillslope_model($ini_timestamp, $asynch_version);
	fill_precipitation_products($ini_timestamp, $end_timestamp);
	fill_reservoirs_data($ini_timestamp, $end_timestamp);
	$json_obj = json_encode($output_json);
	echo($json_obj);
	
?>
