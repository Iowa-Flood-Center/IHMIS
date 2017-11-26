<?php

namespace DbModels;

// use DbModels\ScProduct;
use Illuminate\Database\Eloquent\Model as Eloquent;

class ScRepresentationComposition extends Eloquent{
	protected $connection = 'model_backtime';
	protected $table = 'static_modelplus_definitions.screpresentationcomposition';
	public $roles_mdl = null;
	
	public function scrolesmodel(){
		return($this->hasMany('DbModels\ScRepresentationCompositionRoleMdl',
							  'screpresentationcomposition_id', 'id'));
	}
	
	public function __toString(){ return((string)$this->id);}
}

?>