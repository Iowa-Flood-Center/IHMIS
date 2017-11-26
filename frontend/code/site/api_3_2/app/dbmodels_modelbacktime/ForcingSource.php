<?php

namespace DbModels;

// use DbModels\ScProduct;
use Illuminate\Database\Eloquent\Model as Eloquent;

class ForcingSource extends Eloquent{
	protected $connection = 'model_backtime';
	protected $table = 'static_modelplus_definitions.forcingsource';
	
	// -----------------------------{ GENR }------------------------------ //
	
	public function isAvailable($app, $timestamp_ini, $timestamp_end){
		if ($this->forcingformat_id == 7){
			return(true);  // recurrent forcings are always available
		} elseif($this->forcingformat_id == 3) {
			$db_def_folderpath = $app->fss->dbconnection_folder_path;
			$db_def_filename = "dbdefinition_forcingsource_".$this->id;
			$db_def_filepath = $db_def_folderpath.$db_def_filename.".json";
			
			if(!file_exists($db_def_filepath)){ return(false); }
			
			$file_content_text = file_get_contents($db_def_filepath);
			$file_content_json = json_decode($file_content_text);
			
			return($this->process_dbcon_file($file_content_json, 
			                                 $timestamp_ini, 
											 $timestamp_end));
		} else {
			return(false);
		}
	}
	
	private function process_dbcon_file($db_file_content, 
	                                    $timestamp_ini, 
										$timestamp_end){
		try{
			// execute call
			$con_str = "host=%s port=%d dbname=%s user=%s password=%s";
			$con_str = sprintf($con_str, $db_file_content->host, 
			                             $db_file_content->port,
			                             $db_file_content->database, 
										 $db_file_content->username,
										 $db_file_content->password);
			$db_con = pg_connect($con_str);
			$select_query = $db_file_content->query_search;
			$select_query = str_replace("<TIMESTAMP_INI>", $timestamp_ini, 
			                            $select_query);
			$select_query = str_replace("<TIMESTAMP_END>", $timestamp_end, 
			                            $select_query);
			$result = pg_query($db_con, $select_query);
			pg_close($db_con);
			$result = pg_fetch_row($result);
			return($result[0] == 't' ? true : false);
		} catch (Exception $e) {
			echo('Caught exception: '.$e->getMessage()."\n");
		}
	}
}

?>