<?php

namespace DbModels;

use Illuminate\Database\Capsule\Manager as DB;
use Illuminate\Database\Eloquent\Model as Eloquent;
use Requester\AuxFilesLib as ReqAuxFiles;
use DbModels\ScRepresentation;

class HlModel extends Eloquent{
	const schema = 'static_modelplus_definitions';  // TODO - move to shared place in $app
	protected $connection = 'model_backtime';
	protected $table = 'static_modelplus_definitions.hlmodel';
	
	
	# ------------------------------{ ELOQ }------------------------------- #
	
	// 
	public function screpresentations($app){
		
		$f_name = "get_screpresentations_from_hlmodel";
		
		$sql_command = "SELECT ".HlModel::schema.".".$f_name."(".$this->id.");";
		$sql_result = DB::connection('model_backtime')->select($sql_command);
		$return_array = array();
		foreach($sql_result as $cur_result){
			array_push($return_array, 
			           new ScRepresentation($cur_result[$f_name]));
		}
		
		return($return_array);
	}
	
	//
	public function screpresentations_comparable($app, $hl_model_2){
		
		$f_name = "get_common_screpresentations_from_hlmodels";
		
		$sql_command = "SELECT ".HlModel::schema.".".$f_name.
		                   "(".$this->id.", ". $hl_model_2->id .");";
		$sql_result = DB::connection('model_backtime')->select($sql_command);
		$return_array = array();
		foreach($sql_result as $cur_result){
			array_push($return_array, 
			           new ScRepresentation($cur_result[$f_name]));
		}
		
		return($return_array);
	}
	
	//
	public function scproducts($app){
		$hl_model_query = $this->belongsToMany('DbModels\ScProduct',
											   'static_modelplus_definitions.hlmodel_scproduct',
										       'hlmodel_id', 'scproduct_id');
		return($hl_model_query);
	}
	
	//
	public function forcingtypes(){
		$global_parms_query = $this->belongsToMany('DbModels\ForcingType',
												   'static_modelplus_definitions.hlmodel_forcingtype',
												   'hlmodel_id', 'forcingtype_id');
		
		return($global_parms_query);
	}
	
	//
	public function hydrologicalmodel(){
		return($this->hasOne('DbModels\HydrologicalModel',
		                     'id', 'hydrologicalmodel_id'));
	}
	
	//
	public function globalparameters($app){
		$global_parms_query = $this->hasMany(
		                            'DbModels\HlModelGlobalParameter',
									'hlmodel_id', 'id');
		
		return($global_parms_query);
	}
	
	# ------------------------------{ GENR }------------------------------- #
	
	//
	// $app
	// $timestamp_ini
	// $timestamp_end
	// RETURN: 
	public static function inTimestampsInterval($app, $timestamp_ini, 
	                                            $timestamp_end){
		$asynch_vers = '1.3';  // TODO - remove hardcoded asynch version
		$lhmodel_ids = array();
													 
		// define "10 days" initial condition timestamp
		$initcond_timestamp = ReqAuxFiles::get_initcond_timestamp($timestamp_ini);
		
		// read content in initial conditions catalogue file
		$json_str = file_get_contents($app->fss->initialstates_hdf5_list_filepath);
		$json_data = json_decode($json_str, true);
		
		// check if it exists in the dictionary
		if (!array_key_exists($initcond_timestamp, $json_data))
			return ($lhmodel_ids);
		
		// check if version is present
		if (!array_key_exists($asynch_vers, $json_data[$initcond_timestamp]))
			return($lhmodel_ids);
		
		// push push
		$lhmodel_ids = $json_data[$initcond_timestamp][$asynch_vers];
		
		// get from database
		return(HlModel::whereIn('id', $lhmodel_ids)->get());
		
	}
	
	public function __toString(){ return((string)$this->id);}
}

?>