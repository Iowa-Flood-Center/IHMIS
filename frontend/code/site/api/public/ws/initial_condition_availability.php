<?php

function process_post_request($app){
	
	// define constant
    $asynch_versions = array("1.2", "1.3");                // TODO - should go to a common place
	
	// get arguments - gets all '1d2', '1d3', ...
    $all_arguments = array();
	foreach($asynch_versions as $cur_asynch_ver){
		$cur_asynch_ver_arg = str_replace(".", "d", $cur_asynch_ver);
		if(!isset($_POST[$cur_asynch_ver_arg])) continue;
		$all_arguments[$cur_asynch_ver] = explode(",", $_POST[$cur_asynch_ver_arg]);
	}
	
	// dictionary in form of timestamp => asynch_ver => hl_model_id
	$timestamp_dict = array();
	
	// build content in '$timestamp_dict'
	foreach(array_keys($all_arguments) as $cur_asynch_ver){
		foreach($all_arguments[$cur_asynch_ver] as $cur_file_basename){
			
			// TODO - move this splitting somewhere else
            $file_pre = $app->fss->initialstates_hdf5_file_prefix;
			$file_ext = $app->fss->initialstates_hdf5_file_extens;
            $cur_file_clean = str_replace($file_pre, "", $cur_file_basename);
			$cur_file_clean = str_replace($file_pre, "", $cur_file_clean);
			$cur_file_clean = explode("_", $cur_file_clean);
			$cur_hl_model_id = $cur_file_clean[0];
			$cur_timestamp = $cur_file_clean[1];
			
			// create structure if necessary
			if(!array_key_exists($cur_timestamp, $timestamp_dict)){
				$timestamp_dict[$cur_timestamp] = array();}
			if(!array_key_exists($cur_asynch_ver, $timestamp_dict[$cur_timestamp])){
				$timestamp_dict[$cur_timestamp][$cur_asynch_ver] = array();}
			
			// add data to dictionary
			array_push($timestamp_dict[$cur_timestamp][$cur_asynch_ver], $cur_hl_model_id);
		}
	}
	
	// write text file
	$json_data = json_encode($timestamp_dict);
	file_put_contents(FoldersDefs::INITIALSTATES_HDF5_LIST_FILEPATH, $json_data);
	
	// show simple message
	$return_array = array();
	$return_array["message"] = "Wrote file: '".FoldersDefs::INITIALSTATES_HDF5_LIST_FILEPATH."'.";
	echo(json_encode($return_array));
}

?>