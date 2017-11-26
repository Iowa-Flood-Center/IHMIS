<?php

namespace DbModels;

use Illuminate\Database\Eloquent\Model as Eloquent;

class ScProduct extends Eloquent{
	protected $connection = 'model_backtime';
	protected $table = 'static_modelplus_definitions.scproducts';
	
	// Eloquent-based methods
	public function screpresentations(){
		return($this->belongsToMany('DbModels\ScRepresentation', 
		                            'static_modelplus_definitions.scproduct_screpresentation',
									'scproduct_id',
									'screpresentation_id'));
	}
	
	// 
	public function get_screpresentations(){
		$all_retrieved = array();
		foreach($this->screpresentations()->get() as $cur_repr){
		    array_push($all_retrieved, $cur_repr);}
		return($all_retrieved);
	}
	
	// 
	public function __toString(){ return((string)$this->id);}
}

?>