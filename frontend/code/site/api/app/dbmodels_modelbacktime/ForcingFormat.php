<?php

namespace DbModels;

// use DbModels\ScProduct;
use Illuminate\Database\Eloquent\Model as Eloquent;

class ForcingFormat extends Eloquent{
	protected $connection = 'model_backtime';
	protected $table = 'static_modelplus_definitions.forcingformat';
}

?>