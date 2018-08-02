<?php

namespace DbPrecipitations;

use Illuminate\Database\Eloquent\Model as Eloquent;

class PrecipitationSource extends Eloquent{
	protected $connection = 'precipitation';
	protected $table = 'public.precipitationsource';
	
}

?>