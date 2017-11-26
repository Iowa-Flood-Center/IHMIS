<?php

namespace DbModels;

use Illuminate\Database\Capsule\Manager as DB;
use Illuminate\Database\Eloquent\Model as Eloquent;

class ScEvaluation extends Eloquent{
	protected $connection = 'model_backtime';
	protected $table = 'static_modelplus_definitions.scevaluation';
	
	/**
	 *
	 * $reference_id :
	 */
	public static function fromReference($app, $reference_id){
		return (ScEvaluation::fromReferences($app, array($reference_id)));
	}
	
	/**
	 *
	 * $references_id : Array of strings
	 */
	public static function fromReferences($app, $references_id){
		$where_in = "('".implode("','", $references_id)."')";
		$where_tag = 'static_modelplus_definitions.screference.acronym in '.$where_in;
		$sel_query = $app->dbs->table('static_modelplus_definitions.scproduct_screference',
		                              'model_backtime')
						    ->join('static_modelplus_definitions.scevaluation_scproduct', 
						           'static_modelplus_definitions.scproduct_screference.id_scproduct', 
							       '=',
							       'static_modelplus_definitions.scevaluation_scproduct.id_scproduct_reference')
							->join('static_modelplus_definitions.scevaluation', 
						           'static_modelplus_definitions.scevaluation.id', 
							       '=',
							       'static_modelplus_definitions.scevaluation_scproduct.id_scevaluation')
							->join('static_modelplus_definitions.screference', 
							       'static_modelplus_definitions.screference.id', 
								   '=', 
								   'static_modelplus_definitions.scproduct_screference.id_screference')
							->select('static_modelplus_definitions.scevaluation.*', 
                                     'static_modelplus_definitions.screference.title as screference_title',
							         'static_modelplus_definitions.screference.acronym as screference_acronym')
							->whereRaw($where_tag);
		return($sel_query->get());
	}
	
	/**
	 *
	 * $hl_model : Integer
	 */
	public static function forHlModel($app, $hl_model){
		$where_tag = '"static_modelplus_definitions"."hlmodel"."id" = '.$hl_model;
		$sel_query = $app->dbs->table('static_modelplus_definitions.scevaluation',
		                              'model_backtime')
						    ->join('static_modelplus_definitions.scevaluation_scproduct', 
						           'static_modelplus_definitions.scevaluation_scproduct.id_scevaluation', 
							       '=',
							       'static_modelplus_definitions.scevaluation.id')
							->join('static_modelplus_definitions.hlmodel_scproduct', 
						           'static_modelplus_definitions.hlmodel_scproduct.scproduct_id', 
							       '=',
							       'static_modelplus_definitions.scevaluation_scproduct.id_scproduct_evaluated')
							->join('static_modelplus_definitions.hlmodel', 
							       'static_modelplus_definitions.hlmodel.id', 
								   '=', 
								   'static_modelplus_definitions.hlmodel_scproduct.hlmodel_id')
							->select('static_modelplus_definitions.scevaluation.*')
							->whereRaw($where_tag);
		return($sel_query->get());
	}
	
	public function __toString(){ return((string)$this->id);}
}

?>