<?php
	header('Content-type: application/json');
	include_once("class_AuxFiles.php");
	include_once("../common/class_FoldersDefs.php");

	// //////////////////////////////////////// CONS //////////////////////////////////////// //
	
	$asynch_versions = array("1.2", "1.3");  // TODO - should go to a common place
	
	
	// //////////////////////////////////////// ARGS //////////////////////////////////////// //
	
	// read arguments
	$all_arguments = array();
	foreach($asynch_versions as $cur_asynch_ver){
		$cur_asynch_ver_arg = str_replace(".", "d", $cur_asynch_ver);
		if(!isset($_POST[$cur_asynch_ver_arg])){
			echo("No POST for '".$cur_asynch_ver."'.\n");
			continue;
		} else {
			echo("Got POST for '".$cur_asynch_ver."'.\n");
		}
		$all_arguments[$cur_asynch_ver] = explode(",", $_POST[$cur_asynch_ver_arg]);
	}
	
	
	// //////////////////////////////////////// CALL //////////////////////////////////////// //
	
	// dictionary in form of timestamp => asynch_ver => hl_model_id
	$timestamp_dict = array();
	
	// build content in '$timestamp_dict'
	foreach(array_keys($all_arguments) as $cur_asynch_ver){
		foreach($all_arguments[$cur_asynch_ver] as $cur_file_basename){
			$cur_hl_model_id = AuxFiles::extract_hlmodel_from_initialcondition_file_name($cur_file_basename);
			$cur_timestamp = AuxFiles::extract_timestamp_from_initialcondition_file_name($cur_file_basename);
			
			if(!array_key_exists($cur_timestamp, $timestamp_dict)){
				$timestamp_dict[$cur_timestamp] = array();
			}
			
			if(!array_key_exists($cur_asynch_ver, $timestamp_dict[$cur_timestamp])){
				$timestamp_dict[$cur_timestamp][$cur_asynch_ver] = array();
			}
			
			echo("Pushed '".$cur_hl_model_id."' into '".$cur_timestamp."' > '".$cur_asynch_ver."'.");
			array_push($timestamp_dict[$cur_timestamp][$cur_asynch_ver], $cur_hl_model_id);
		}
	}
	
	// write text file
	$json_data = json_encode($timestamp_dict);
	file_put_contents(FoldersDefs::INITIALSTATES_HDF5_LIST_FILEPATH, $json_data);
	
	echo("Wrote file '".FoldersDefs::INITIALSTATES_HDF5_LIST_FILEPATH."'.");
?>