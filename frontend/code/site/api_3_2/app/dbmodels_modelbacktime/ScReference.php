<?php

namespace DbModels;

use Illuminate\Database\Capsule\Manager as DB;
use Illuminate\Database\Eloquent\Model as Eloquent;

class ScReference extends Eloquent{
	protected $connection = 'model_backtime';
	protected $table = 'static_modelplus_definitions.screference';
	
}

?>