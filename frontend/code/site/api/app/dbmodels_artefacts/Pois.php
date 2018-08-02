<?php

namespace DbArtefacts;

use Illuminate\Database\Capsule\Manager as DB;
use Illuminate\Database\Eloquent\Model as Eloquent;

class Pois extends Eloquent{
	const schema = 'pois';
	protected $connection = 'artefacts';
	protected $table = 'pois.pois_adv';
	
}

?>