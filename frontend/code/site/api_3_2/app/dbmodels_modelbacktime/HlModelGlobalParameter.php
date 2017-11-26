<?php 

namespace DbModels;

use Illuminate\Database\Eloquent\Model as Eloquent;

class HlModelGlobalParameter extends Eloquent{
	protected $connection = 'model_backtime';
	protected $table = 'static_modelplus_definitions.hlmodel_globalparameters';
	
}

?>
