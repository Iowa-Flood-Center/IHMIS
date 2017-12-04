<?php

use Requester\AuxFilesLib as AuxFilesLib;
use Requester\RunsetRequest as RunsetRequest;
use Requester\ModelRequestFactory as ModelRequestFactory;
use Requester\ModelCombRequestFactory as ModelCombRequestFactory;

require_once '../../common/libs/settings.php';

function process_get_request($app){
	// get params
	$from = $app->request->params("from");
	
	// query search
	$all_retrieved = null;
	
	if ((!is_null($from))&&($from == "waiting_room")){
		$all_retrieved = RunsetRequest::in_waiting_room($app);
	} else {
		$all_retrieved = array();
	}
	
	// show
	echo(json_encode($all_retrieved));
}

function process_post_request($app){
	//error_reporting(E_ALL);
    //ini_set('display_errors', 1);
	
	// get arguments
	$post_data = $app->request->post();
	$post_data["runset_title"] = str_replace("_", " ", $post_data["runset_title"]);
	
	// build the RunsetRequest and all ModelRequest objects
	try{
		$runset_obj = new RunsetRequest($post_data);
		// add model requests
		$runset_obj->model_requests = array();
		for($count_mdl=1; $count_mdl < $runset_obj->max_models + 1; $count_mdl++){
			$cur_mdl_request = ModelRequestFactory::getModelRequest($post_data, $count_mdl);
			if (is_null($cur_mdl_request)) { continue; }
			array_push($runset_obj->model_requests, $cur_mdl_request); 
		}
		// add model combined requests
		$runset_obj->modelcomb_requests = ModelCombRequestFactory::getModelCombRequests($post_data);
	} catch(Exception $exp) {
		echo(json_encode(array("Exception" => $exp->getMessage())));
		exit();
	} 
	
	// set up log file
	if ((!property_exists($app->log, "file_path"))||(is_null($app->log->file_path)))
      $app->log->file_path = Settings::get_log_file_path(["api", "sc_runset_request"]);
	
	// create files
	AuxFilesLib::$app = $app;
	$runset_obj->create_all_meta_files($app);
	$runset_obj->compact_all_metafiles();
	$runset_obj->schedule_files_deletion(2);
	echo(json_encode($runset_obj->dispatch()));
	$app->log->file_path = null;
}

function process_delete_request($app, $file_name){
	
	if(RunsetRequest::delete_from_waiting_room($app, $file_name)){
		$ret = array("success"=>$file_name);
	} else {
		$ret = array("error"=>$file_name);
	}
	
	echo(json_encode($ret));
}

?>
