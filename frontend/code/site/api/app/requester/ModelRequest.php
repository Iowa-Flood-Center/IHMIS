<?php

	namespace Requester;
	
	use Requester\AuxFilesLib as AuxFilesLib;

	// 
	class ModelRequest{
		public $model_id;                 //
		public $hillslope_model_id;       //
		public $forcings_dict;            //
		public $model_title;              //
		public $model_desc;               //
		public $gbl_parameters;           //
		public $model_reprs;              // Array of SC-Representation IDs
		public $modelseq_reprs;           // Array of SC-Representation IDs or null
		public $evaluations;              // Array of SC-Evaluation_SC-Reference IDs or null
		public $what_run;                 //
		public $globalfile_requests;      //
		
		// ATTENTION - THIS CLASS SHOULD BE CONSTRUCTED BY ModelRequestFactory
		
		/**
		 *
		 * $runsetRequest :
		 * RETURN : Array of GlobalFileRequest objects
		 */
		public function createGlobalFileRequests($runsetRequest, $app){
			
			// establish the current time of request and create temporary folders
			$current_time = $runsetRequest->current_timestamp;
			// $local_folder_path = $this->create_local_temp_dirs();
			
			$gbl_files_request = array();
			
			//
			switch($runsetRequest->what_run){
				
				case "what_run_06hseq":
				case "what_run_20dseq":
				
					\Settings::write_log_ln("Creating single global file for model '".$this->model_id."'.",
					                        $app->log->file_path);
				
					// define other timestamps
					$timestamp_initcond = AuxFilesLib::get_initcond_timestamp($runsetRequest->timestamp_ini);
					
					// create base global file object
					$base_gbl_file_req = new GlobalFileRequest();
					$base_gbl_file_req->fill_with_model_req($this);
					$base_gbl_file_req->fill_with_runset_req($runsetRequest);
					$base_gbl_file_req->timestamp_cur = $current_time;
					$base_gbl_file_req->reservoir_idx = null;
					$base_gbl_file_req->reservoir_rsv = null;
				
					// create run
					$prev_gbl_file_req = clone $base_gbl_file_req;
					$prev_gbl_file_req->model_id = $this->model_id."prevqpe";
					$prev_gbl_file_req->model_title = $this->model_title."(prev.)";
					$prev_gbl_file_req->timestamp_ini = $timestamp_initcond;
					$prev_gbl_file_req->timestamp_end = $runsetRequest->timestamp_ini;
					$prev_gbl_file_req->initcond_source = null;
					$prev_gbl_file_req->show_main = False;
					array_push($gbl_files_request, $prev_gbl_file_req);
					
					// create past
					$past_gbl_file_req = clone $base_gbl_file_req;
					$past_gbl_file_req->model_id = $this->model_id;
					$past_gbl_file_req->model_title = $this->model_title;
					$past_gbl_file_req->timestamp_ini = $runsetRequest->timestamp_ini;
					$past_gbl_file_req->timestamp_end = $runsetRequest->timestamp_end;
					$past_gbl_file_req->initcond_source = $prev_gbl_file_req->model_id;
					$past_gbl_file_req->show_main = True;
					array_push($gbl_files_request, $past_gbl_file_req);
				
					break;
				
				case "what_run_06hp06hf":
				case "what_run_10dp10df":
				
					\Settings::write_log_ln("Creating segmented global file for model '".$this->model_id."'.",
					                        $app->log->file_path);
				
					// define other timestamps
					$timestamp_initcond = AuxFilesLib::get_initcond_timestamp($runsetRequest->timestamp_ini);
					$timestamp_mid = ($runsetRequest->timestamp_ini + $runsetRequest->timestamp_end)/2;
					
					// create base global file object
					$base_gbl_file_req = new GlobalFileRequest();
					$base_gbl_file_req->fill_with_model_req($this);
					$base_gbl_file_req->fill_with_runset_req($runsetRequest);
					$base_gbl_file_req->timestamp_cur = $current_time;
					$base_gbl_file_req->reservoir_idx = null;
					$base_gbl_file_req->reservoir_rsv = null;
					
					// create prev
					$prev_gbl_file_req = clone $base_gbl_file_req;
					$prev_gbl_file_req->model_id = $this->model_id."prevqpe";
					$prev_gbl_file_req->model_title = $this->model_title."(prev.)";
					$prev_gbl_file_req->timestamp_ini = $timestamp_initcond;
					$prev_gbl_file_req->timestamp_end = $runsetRequest->timestamp_ini;
					$prev_gbl_file_req->initcond_source = null;
					$prev_gbl_file_req->show_main = False;
					array_push($gbl_files_request, $prev_gbl_file_req);
					
					// create past
					$past_gbl_file_req = clone $base_gbl_file_req;
					$past_gbl_file_req->model_id = $this->model_id."pastqpe";
					$past_gbl_file_req->model_title = $this->model_title."(past)";
					$past_gbl_file_req->timestamp_ini = $runsetRequest->timestamp_ini;
					$past_gbl_file_req->timestamp_end = $timestamp_mid;
					$past_gbl_file_req->initcond_source = $prev_gbl_file_req->model_id;
					$past_gbl_file_req->show_main = True;
					array_push($gbl_files_request, $past_gbl_file_req);
					
					// create fore - rain
					$fore_gbl_file_req_qpe = clone $base_gbl_file_req;
					$fore_gbl_file_req_qpe->model_id = $this->model_id."foreqpe";
					$fore_gbl_file_req_qpe->model_title = $this->model_title."(fore. qpe)";
					$fore_gbl_file_req_qpe->timestamp_ini = $timestamp_mid;
					$fore_gbl_file_req_qpe->timestamp_end = $runsetRequest->timestamp_end;
					$fore_gbl_file_req_qpe->initcond_source = $prev_gbl_file_req->model_id;
					$fore_gbl_file_req_qpe->show_main = True;
					array_push($gbl_files_request, $fore_gbl_file_req_qpe);
					
					// create fore - no rain
					$fore_gbl_file_req_non = clone $base_gbl_file_req;
					$fore_gbl_file_req_non->model_id = $this->model_id."forenon";
					$fore_gbl_file_req_non->model_title = $this->model_title."(fore. non)";
					$fore_gbl_file_req_non->timestamp_ini = $timestamp_mid;
					$fore_gbl_file_req_non->timestamp_end = $runsetRequest->timestamp_end;
					$fore_gbl_file_req_non->initcond_source = $prev_gbl_file_req->model_id;
					$fore_gbl_file_req_non->precip_source_id = null;
					$fore_gbl_file_req_non->show_main = True;
					array_push($gbl_files_request, $fore_gbl_file_req_non);
					
					break;
				
				default:
				
					// just log a message
					\Settings::write_log_ln("Unexpected 'what run' value: ".$runsetRequest->what_run, 
					                        $app->log->file_path);
					\Settings::write_log_ln("Not creating global files for model '".$this->model_id."'.",
					                        $app->log->file_path);
					
					break;
			}
			
			$this->globalfile_requests = $gbl_files_request;
			
			return($gbl_files_request);
		}
	}

?>