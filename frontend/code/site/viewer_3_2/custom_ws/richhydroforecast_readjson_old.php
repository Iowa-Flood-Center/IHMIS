<?php
	header("Content-Type: application/json");
	date_default_timezone_set('America/Chicago');
	
	/*********************************************** ARGS **********************************************/

	// read sc_runset_id
	if(isset($_GET['sc_runset_id'])){
		$sc_runset_id = $_GET['sc_runset_id'];
	} else {
		echo('{"ERROR":"Missing \'sc_runset_id\' argument."}');
		exit();
	}
	
	// read sc_model_id
	if(isset($_GET['sc_model_id'])){
		$sc_model_id = $_GET['sc_model_id'];
	} else {
		echo('{"ERROR":"Missing \'sc_model_id\' argument."}');
		exit();
	}
	
	// read link_id
	if(isset($_GET['link_id'])){
		$link_id = $_GET['link_id'];
	} else {
		echo('{"ERROR":"Missing \'link_id\' argument."}');
		exit();
	}
	
	// read lead_timestamp
	$lead_timestamp = null;
	if(isset($_GET['lead_timestamp'])){
		$lead_timestamp = intval($_GET['lead_timestamp']);
	}
	
	// read refresh
	if ((isset($_GET['refresh'])) && (($_GET['refresh'] == 't'))||($_GET['refresh'] == 'T')) {
		$is_refresh = true;
	} else {
		$is_refresh = false;
	}
	
	/*********************************************** CONS **********************************************/
	
	$sc_represcomb_id = "richhydroforecast";
	$meta_model_file_frame = "/local/iihr/andre/model_3_1/%s/metafiles/sc_models/%s.json";   // % runset model
	$root_folder_frame = "/local/iihr/andre/model_3_1/%s/repres_displayed/%s/%s/";
	$root_folder_path = sprintf($root_folder_frame, $sc_runset_id, $sc_model_id, $sc_represcomb_id);
	$common_folder_path = $root_folder_path."common/";
	$modelforestg_folder_path = $root_folder_path."modelforestg/";
	$stageref_folder_path = $root_folder_path."stageref/";
	
	$before_timestamp_interval = 60*60;  // one hour gap
	$after_days = 10;
	$before_days = 10;
	
	/*********************************************** DEFS **********************************************/

	/**
	 * Return String if possible or NULL otherwise
	 */
    function get_model_name($runset_id, $model_id){
		global $meta_model_file_frame;
		try{
			$file_path = sprintf($meta_model_file_frame, $runset_id, $model_id);
			$file_content = json_decode(file_get_contents($file_path), true);
			if(isset($file_content["sc_model"]["forecast_title"])){
				return($file_content["sc_model"]["forecast_title"]);
			} else if(isset($file_content["sc_model"]["title"])){
				return($file_content["sc_model"]["title"]);
			} else {
				return($file_content["sc_model"]["id"]);
			}
		} catch (Exception $e) {
			echo($e);  // TODO - remove it
			return(null);
		}
	}
	
	/**
	 * No return. Changes resume object.
	 */
	function fill_resume_with_forecast(&$resume_obj, $modelforestg_folder_path, $lead_timestamp, 
	                                   $timestamp_cur, $link_id, $runset_id, $is_refresh){
		global $before_timestamp_interval;
		
		// define time interval
		if (is_null($lead_timestamp)){
			$max_timestamp = $timestamp_cur;
		} else {
			$max_timestamp = $lead_timestamp;
		}
		$min_timestamp = $max_timestamp - $before_timestamp_interval;
		
		// find models
		$model_ids = define_stagefore_models($modelforestg_folder_path);
		
		// fill timeseries
		foreach($model_ids as $cur_model_id){
			// find matching files
			$cur_folder_path = $modelforestg_folder_path.$cur_model_id.DIRECTORY_SEPARATOR;
			$scanned_files = array_diff(scandir($cur_folder_path), array('..', '.'));
			$prefix = "/_".$link_id.".json$/";
			$cur_model_name = get_model_name($runset_id, $cur_model_id);
			// $cur_model_name = "";
			$cur_model_idx = create_empty_forecast($resume_obj, $cur_model_id, $cur_model_name);
			foreach($scanned_files as $cur_scanned_file){
				if (!preg_match($prefix, $cur_scanned_file)){ continue; }
				$cur_timestamp = intval(explode("_", $cur_scanned_file)[0]);
				if (($cur_timestamp < $min_timestamp)||($cur_timestamp > $max_timestamp)){ continue; }
				$cur_leadtime = $cur_timestamp;
				$cur_file_path = $cur_folder_path.$cur_scanned_file;
				$cur_file_content = json_decode(file_get_contents($cur_file_path), true);
				$cur_stg_timeseries = array();
				$cur_dsc_timeseries = array();
				// $added = 0;
				for($cur_i = 0; $cur_i < count($cur_file_content["disch_mdl"]); $cur_i++){
					$cur_timestamp = $cur_file_content["stage_mdl"][$cur_i][0];
					$cur_stg = floatval(number_format($cur_file_content["stage_mdl"][$cur_i][1], 2));
					$cur_dsc = floatval(number_format($cur_file_content["disch_mdl"][$cur_i][1], 2));
					$cur_stg_timeseries[] = [$cur_timestamp, $cur_stg];
					$cur_dsc_timeseries[] = [$cur_timestamp, $cur_dsc];
					// $added ++;
				}
				$resume_obj["forecasts"][$cur_model_idx]["timeseries_stg"][$cur_leadtime] = $cur_stg_timeseries;
				$resume_obj["forecasts"][$cur_model_idx]["timeseries_dsc"][$cur_leadtime] = $cur_dsc_timeseries;
			}
		}
		
		// fill metadata
		$resume_obj["metadata"]["lead_time"] = $max_timestamp;
		$resume_obj["metadata"]["has_lead_time"] = true;
	}
	
	/**
	 * No return. Changes resume object.
	 */
	function fill_resume_with_observed(&$resume_obj, $ref_folder_path, $cur_timestamp, $link_id, 
	                                   $is_refresh){
		if($is_refresh){ return; }
		
		# read file
		$file_name = $cur_timestamp."_".$link_id.".json";
		$file_path = $ref_folder_path.$file_name;
		$file_content = json_decode(file_get_contents($file_path), true);
		
		# set timeseries and update meta data
		for($cur_i = 0; $cur_i < count($file_content["obs_stg"]); $cur_i++){
			$cur_timestamp = $file_content["obs_stg"][$cur_i][0];
			$cur_stg = floatval(number_format($file_content["obs_stg"][$cur_i][1], 2));
			$cur_dsc = floatval(number_format($file_content["obs_dsc"][$cur_i][1], 2));
			$resume_obj["observed"]["timeseries_stg"][] = [$cur_timestamp, $cur_stg];
			$resume_obj["observed"]["timeseries_dsc"][] = [$cur_timestamp, $cur_dsc];
			consider_min_max_y($resume_obj, $cur_stg);
			consider_min_max_y($resume_obj, $cur_stg);
		}
	}
	
	/**
	 * No return. Changes resume object.
	 */
	function fill_resume_with_commons(&$resume_obj, $common_folder_path, $link_id, $is_refresh){
		if($is_refresh){ return; }
		
		// read file
		$file_name = $link_id.".json";
		$file_path = $common_folder_path.$file_name;
		$file_content = json_decode(file_get_contents($file_path), true);
		
		// set description and drainage area values
		if(array_key_exists("description", $file_content)){
			$resume_obj["metadata"]["site_description"] = $file_content["description"];}
		if(array_key_exists("up_area", $file_content)){
			$resume_obj["metadata"]["drainage_area"] = $file_content["up_area"];}
		
		// set thresholds values
		if(array_key_exists("stage_threshold_act", $file_content)){
			consider_min_max_y($resume_obj, $file_content["stage_threshold_act"]);
			$resume_obj["metadata"]["thresholds_stg"]["action"] = $file_content["stage_threshold_act"];}
		if(array_key_exists("stage_threshold_act", $file_content)){
			consider_min_max_y($resume_obj, $file_content["stage_threshold_fld"]);
			$resume_obj["metadata"]["thresholds_stg"]["flood"] = $file_content["stage_threshold_fld"];}
		if(array_key_exists("stage_threshold_act", $file_content)){
			consider_min_max_y($resume_obj, $file_content["stage_threshold_mod"]);
			$resume_obj["metadata"]["thresholds_stg"]["moderate"] = $file_content["stage_threshold_mod"];}
		if(array_key_exists("stage_threshold_act", $file_content)){
			consider_min_max_y($resume_obj, $file_content["stage_threshold_maj"]);
			$resume_obj["metadata"]["thresholds_stg"]["major"] = $file_content["stage_threshold_maj"];}
	}
	
	/**
	 *
	 */
	function &create_empty_forecast(&$resume_obj, $forecast_id, $forecast_title){
		// TODO - check prior to add
		$added_obj = array("id" => $forecast_id,
                           "title" => $forecast_title,
		                   "timeseries_stg" => array(),
						   "timeseries_dsc" => array());
		array_push($resume_obj["forecasts"], $added_obj);
		return(count($resume_obj["forecasts"]) - 1);
	}
	
	/**
	 * Returns a mapped array
	 */
	function create_empty_resume($current_timestamp, $before, $after){
		$min_x_raw = $current_timestamp - ($before * 24 * 60 * 60);
		$min_x_trc = strtotime(date("Y-m-d", $min_x_raw));
		$max_x_trc = $min_x_trc + (($before + $after)*24*60*60);
		return(array("forecasts" => array(),
		             "observed"  => array("timeseries_stg" => array(),
					                      "timeseries_dsc" => array()),
                     "metadata"	 => array("current_time" => $current_timestamp,
					                      "has_current_time" => True,
										  "min_y" => null,
										  "max_y" => null,
										  "min_x" => $min_x_trc,
										  "max_x" => $max_x_trc,
										  "drainage_area" => null,
										  "thresholds_stg" => array("action" => null,
										                            "flood" => null,
																	"moderate" => null,
																	"major" => null))));
	}
	
	/**
	 *
	 */
	function consider_min_max_y(&$resume_obj, $x_value){
		if(is_null($resume_obj["metadata"]["min_y"]) || 
		   ($resume_obj["metadata"]["min_y"] > $x_value)){
			$resume_obj["metadata"]["min_y"] = floor($x_value);
		}
		if(is_null($resume_obj["metadata"]["max_y"]) || 
		   ($resume_obj["metadata"]["max_y"] < $x_value)){
			$resume_obj["metadata"]["max_y"] = ceil($x_value);
		}
	}
	
	/**
	 * Gets a integer or a null
	 */
	function define_current_timestamp($ref_folder_path, $link_id){
		$scanned_files = array_diff(scandir($ref_folder_path), array('..', '.'));
		arsort($scanned_files);
		$cur_timestamp = null;
		$prefix = "/_".$link_id.".json$/";
		foreach($scanned_files as $cur_scanned_file){
			if (preg_match($prefix, $cur_scanned_file)){
				return(intval(explode("_", $cur_scanned_file)[0]));
			}
		}
		return(null);
	}
	
	/**
	 * Gets the respective reference id
	 */
	function define_stagefore_models($stgfore_folder_path){
		$scanned_files = array_diff(scandir($stgfore_folder_path), array('..', '.'));
		$model_ids = [];
		foreach($scanned_files as $cur_scanned_file){
			$cur_folder_path = $stgfore_folder_path . DIRECTORY_SEPARATOR . $cur_scanned_file;
			if (is_dir($cur_folder_path)){ 
				array_push($model_ids, $cur_scanned_file);
			}
		}
		return($model_ids);
	}
	
	/**
	 * Gets the respective reference id
	 */
	function define_stageref_reference($stgref_folder_path){
		$scanned_files = array_diff(scandir($stgref_folder_path), array('..', '.'));
		$cur_folder_path = null;
		foreach($scanned_files as $cur_scanned_file){
			$cur_folder_path = $stgref_folder_path . DIRECTORY_SEPARATOR . $cur_scanned_file;
			if (is_dir($cur_folder_path)){ 
				return($cur_scanned_file);
			}
		}
		return(null);
	}
	
	/*********************************************** CALL **********************************************/
	
	// 1 - define stage_ref ref
	$ref_id = define_stageref_reference($stageref_folder_path);
	$ref_folder_path = $stageref_folder_path.$ref_id."/";
	// echo("Ref: ".$ref_id."\n");
	
	// 2 - define current timestamp
	$timestamp_cur = define_current_timestamp($ref_folder_path, $link_id);
	// echo("Cur: ".$timestamp_cur."\n");
	
	// 3 - create receiving object
	$resume_obj = create_empty_resume($timestamp_cur, $before_days, $after_days);
	
	// 4 - fill with site description and thresholds
	fill_resume_with_commons($resume_obj, $common_folder_path, $link_id, $is_refresh);
	
	// 5 - fill with observed data
	fill_resume_with_observed($resume_obj, $ref_folder_path, $timestamp_cur, $link_id, $is_refresh);
	
	// 6 - fill with forecast data
	fill_resume_with_forecast($resume_obj, $modelforestg_folder_path, $lead_timestamp, $timestamp_cur, 
	                          $link_id, $sc_runset_id, $is_refresh);
	
	// 7 - print resume object
	echo(json_encode($resume_obj));
?>