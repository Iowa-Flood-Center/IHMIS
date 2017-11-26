<?php

namespace DbModels;

// use DbModels\ScProduct;
use Illuminate\Database\Eloquent\Model as Eloquent;

class ScRepresentationCompositionRoleMdl extends Eloquent{
	protected $connection = 'model_backtime';
	protected $table = 'static_modelplus_definitions.screpresentationcompositionrolemdl';
	
	public function __toString(){ return((string)$this->id);}
}

?>