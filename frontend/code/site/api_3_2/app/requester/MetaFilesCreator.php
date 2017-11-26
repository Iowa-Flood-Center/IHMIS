<?php

	namespace Requester;

	use Requester\AuxFilesLib as AuxFilesLib;
	
	abstract class MetaFilesCreator{
		
		/**
		 * 
		 * $global_file_requester :
		 * $app :
		 * RETURN :
		 */
		public static function create_model_meta_file($global_file_requester, $app){
			
			$timestamp_cur = $global_file_requester->timestamp_cur;
			$model_id = $global_file_requester->model_id;
			$json_final_filepath = AuxFilesLib::get_local_metamodel_file_path($timestamp_cur, $model_id);
			
			// read template file and edits its content
			$json_final_content = file($app->fss->metamodel_template_filepath);
			$all_prods_id = "\"".implode("\",\"", AuxFilesLib::get_sc_product_ids($global_file_requester->hillslope_model_id))."\"";
			// $all_reprs_id = "\"".implode("\",\"", AuxFilesLib::get_sc_representation_ids($global_file_requester->hillslope_model_id))."\"";
			if ( isset($global_file_requester->model_reprs) ){
				$all_reprs_id = "\"".implode("\",\"", $global_file_requester->model_reprs)."\"";
			} else {
				$all_reprs_id = "\"\"";
			}
			$json_final_content[1] = str_replace("SC_MODEL_ID", 
			                                     $global_file_requester->model_id, $json_final_content[1]);   
			$json_final_content[2] = str_replace("MODEL_TITLE", 
			                                     $global_file_requester->model_title, $json_final_content[2]);
			$json_final_content[3] = str_replace("MODEL_DESC", 
			                                     $global_file_requester->model_desc, $json_final_content[3]);
			$json_final_content[4] = str_replace("MODEL_SHOW", 
			                                     $global_file_requester->get_show_main_string(), 
												 $json_final_content[4]);
			$json_final_content[5] = str_replace("SC_PRODUCT_IDS", 
			                                     $all_prods_id, 
												 $json_final_content[5]);
			$json_final_content[6] = str_replace("SC_REPRESENTATION_IDS", 
			                                     $all_reprs_id, 
												 $json_final_content[6]);
			$json_final_content[7] = str_replace("BINGEN_SING_SCRIPT", 
			                                     AuxFilesLib::get_sing_script_path($global_file_requester->hillslope_model_id), 
												 $json_final_content[7]);
			$json_final_content[8] = str_replace("BINGEN_HIST_SCRIPT", 
												 AuxFilesLib::get_hist_script_path($global_file_requester->hillslope_model_id), 
												 $json_final_content[8]);
			
			// save edited template into file
			$fp = fopen($json_final_filepath, 'w');
			foreach ($json_final_content as $key => $value){
				fwrite($fp, $value);
			}
			fclose($fp);
		}
		
		/**
		 *
		 * $runset_request : 
		 * $model_requests :
		 * RETURN :
		 */
		public static function create_comparison_mtx_meta_json_file($runset_request, $model_requests){
			
			switch($runset_request->what_run){
				case "06p06f_loginless":
				case "10p10f_loginless":
					// focus on model combination comparison
					MetaFilesCreator::create_comb_comparison_meta_json_file($runset_request, 
																			$model_requests);
					break;
					
				default:
					// focus on model comparison
					MetaFilesCreator::create_simp_comparison_meta_json_file($runset_request, 
																			$model_requests);
					break;
			}
		}
		
		/**
		 *
		 * $runset_request : 
		 * $model_requests : 
		 * RETURN :
		 */
		public static function create_evaluation_mtx_meta_file($runset_request, $model_requests){
			switch($runset_request->what_run){
				case "06p06f_loginless":
				case "10p10f_loginless":
					break;
				default:
					break;
			}
		}
		
		/**
		 *
		 * $runset_request :
		 * RETURN :
		 */
		public static function create_email_text_file($runset_request){
			// defines file path
			$text_filepath = AuxFilesLib::get_local_emailtext_file_path($runset_request->current_timestamp);
			
			// create file
			$fp = fopen($text_filepath, 'w');
			fwrite($fp, $runset_request->user_email);
			fclose($fp);
		}
		
		/**
		 *
		 * >-+ IMPORTANT +-< It was just copy-and-pasted. Need to be uncommented and worked on.
		 * $runset_request : 
		 * $model_requests : 
		 * RETURN :
		 */
		public static function create_metacomb_hydrographpast($runset_request, $model_requests){
			
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
		 * $runset_request : 
		 * $model_requests : 
		 * RETURN :
		 */
		public static function create_metacomb_sequencemaps($runset_request){
			
			/*
			$possible_forecasts_suffix = array('forenon', 'foreqpe');
			$only_possible_prefix = "pastqpe";
			
			// basic check
			if ((is_null($runset_request)) || 
					(is_null($runset_request->globalfile_requests)) || 
					(sizeof($runset_request->globalfile_requests) == 0)){
				return;
			}
			
			// all pairs
			$all_model_pairs = array();
			
			// find connections
			foreach($runset_request->globalfile_requests as $cur_globalfile_request){
				$cur_model_id = $cur_globalfile_request->model_id;
				
				foreach($possible_forecasts_suffix as $cur_pos_forecast_suffix){
					if (strpos($cur_model_id, $cur_pos_forecast_suffix) !== false){
						$cur_past_model_id = str_replace($cur_pos_forecast_suffix, $only_possible_prefix, $cur_model_id);
						foreach($runset_request->globalfile_requests as $cur_globalfile_request_2){
							$cur_model_id_2 = $cur_globalfile_request_2->model_id;
							if($cur_model_id == $cur_model_id_2){
								$cur_pair = array($cur_past_model_id, $cur_model_id);
								array_push($all_model_pairs, $cur_pair);
							}
						}
					}
				}
			}
			
			// basic check
			if(sizeof($all_model_pairs) == 0){
				echo("No matches found for sequencemaps in ".sizeof($all_model_pairs)." global file requests.");
				return;
			}
			
			// create files
			foreach($all_model_pairs as $cur_pair){
				MetaFilesCreator::create_metacomb_sequencemap($cur_pair[0], $cur_pair[1], $cur_pair[1]."seq", 
															  "SequenceMap(TODO)", 
															  $runset_request->current_timestamp,
															  null);
			}
			*/
			
			///////////////////////////////// SECOND APPROACH /////////////////////////////////
			
			foreach($runset_request->model_requests as $cur_model_request){
				if((!is_null($cur_model_request->modelseq_reprs)) && (sizeof($cur_model_request->globalfile_requests)>2)){
					
					for($cur_fore_idx = 2; $cur_fore_idx < sizeof($cur_model_request->globalfile_requests); $cur_fore_idx++){
						
						$cur_model_fore_id = $cur_model_request->globalfile_requests[$cur_fore_idx]->model_id;
						
						// define title
						if (strpos($cur_model_fore_id, "forenon") !== false){
							$cur_model_seq_title = $cur_model_request->model_title." Seq. (Non Rain)";
						} elseif (strpos($cur_model_fore_id, "foreqpe") !== false) {
							$cur_model_seq_title = $cur_model_request->model_title." Seq. (QPE)";
						} elseif (strpos($cur_model_fore_id, "fore2in") !== false) {
							$cur_model_seq_title = $cur_model_request->model_title." Seq. (2 in)";
						} else {
							continue;
						}
						
						// TODO - make this step a loop for all forecasts
						$cur_modelseqs_id = $cur_model_fore_id."seqsrepr";
						$cur_modelpast_id = $cur_model_request->globalfile_requests[1]->model_id;
						$cur_modelfore_id = $cur_model_fore_id;
						MetaFilesCreator::create_metacomb_sequencemap($cur_modelpast_id, $cur_modelfore_id, 
																	  $cur_modelseqs_id, $cur_model_seq_title, 
																	  $runset_request->current_timestamp,
																	  $cur_model_request->modelseq_reprs);

					}
				} else if (is_null($cur_model_request->modelseq_reprs)) {
					// echo("modelseq_reprs of '".$cur_model_request->modelseq_reprs."' is null. ");
				} else if (sizeof($cur_model_request->globalfile_requests)<=2){
					// echo("size of globalfile_requests of '".$cur_model_request->modelseq_reprs."' is ".sizeof($cur_model_request->globalfile_requests).". ");
				} else {
					// echo("??!!?? ");
				}
				
			}
		}
		
		/**
		 *
		 * $model_past_id : 
		 * $model_fore_id : 
		 * $model_id :
		 * $model_title :
		 * $current_timestamp : 
		 * $representations :
		 * RETURN : 
		 */
		private static function create_metacomb_sequencemap($model_past_id, $model_fore_id, $model_id, $model_title, 
															$current_timestamp, $representation_ids){
			
			// read template file and replace its content
			$json_final_content = file_get_contents(FoldersDefs::METAMODELCOMB_SEQUENCEMAPS_TEMPLATE_FILEPATH);
			$json_final_content = str_replace("RAWMODELID", $model_id, $json_final_content);
			$json_final_content = str_replace("RAWMODELTITLE", $model_title, $json_final_content);
			$json_final_content = str_replace("MODELIDPAST", $model_past_id, $json_final_content);
			$json_final_content = str_replace("MODELIDFORE", $model_fore_id, $json_final_content);
			
			// TODO: make the following line dynamic
			if (is_null($representation_ids)){
				$json_final_content = str_replace("REPRIDS", '', $json_final_content);
			} else {
				$all_repr_ids_tagged = array();
				foreach($representation_ids as $cur_repr_id){
					array_push($all_repr_ids_tagged, '"'.$cur_repr_id.'"');
				}
				$json_final_content = str_replace("REPRIDS", 
												  implode(",", $all_repr_ids_tagged), 
												  $json_final_content);
			}
			
			// define new meta file path and save it
			$json_final_filepath = AuxFiles::get_local_metacomb_hydrographpast_file_path($current_timestamp,
																						 $model_id);
			file_put_contents($json_final_filepath, $json_final_content);
		}
		
		/**
		 *
		 * $runset_request : 
		 * $model_requests : 
		 * RETURN :
		 */
		private static function create_simp_comparison_meta_json_file($runset_request, $model_requests){
			
			$json_final_filepath = AuxFiles::get_local_metacomparisonmtx_file_path($runset_request->current_timestamp);
			
			// read template file and separates main line
			$json_final_content = file(AuxFiles::METACOMPARISON_TEMPLATE_FILEPATH);
			$template_line = $json_final_content[1];
			
			// generates all internal lines
			$comp_lines = array();
			foreach($model_requests as $key_1 => $model_req1){
				foreach($model_requests as $key_2 => $model_req2){
					if($key_1 != $key_2){
						$cur_line = str_replace("MODELID01", $model_req1->model_id, $template_line);
						$cur_line = str_replace("MODELID02", $model_req2->model_id, $cur_line);
						$repr_ids = AuxFiles::get_sc_comparison_product_ids($model_req1->hillslope_model_id, 
																			$model_req2->hillslope_model_id);
						$cur_line = str_replace("SC_PRODUCT_IDS", "\"".implode("\",\"", $repr_ids)."\"", $cur_line);
						$comp_lines[] = $cur_line;
					}
				}
			}
			$json_final_content[1] = implode("		,\n", $comp_lines);
			
			// write all internal lines
			$fp = fopen($json_final_filepath, 'w');
			foreach ($json_final_content as $value){
				fwrite($fp, $value);
			}
			fclose($fp);
		}
		
		/**
		 *
		 * $runset_request :
		 * $model_requests :
		 * RETURN :
		 */
		private static function create_comb_comparison_meta_json_file($runset_request, $model_requests){
			// TODO
			return;
		}
	}

?>