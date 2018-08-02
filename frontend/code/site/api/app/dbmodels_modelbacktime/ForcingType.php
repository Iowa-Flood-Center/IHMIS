<?php

namespace DbModels;

// use DbModels\ScProduct;
use Illuminate\Database\Eloquent\Model as Eloquent;

class ForcingType extends Eloquent{
	protected $connection = 'model_backtime';
	protected $table = 'static_modelplus_definitions.forcingtype';
	
	// -----------------------------{ ELOQ }------------------------------ //
	
	public function forcingsources(){
		return($this->hasMany('DbModels\ForcingSource', 
							  'forcingtype_id', 'id'));
	}
	
	// -----------------------------{ GENR }------------------------------ //
}

?>