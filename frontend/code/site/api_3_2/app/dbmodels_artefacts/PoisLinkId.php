<?php

namespace DbArtefacts;

use Illuminate\Database\Capsule\Manager as DB;
use Illuminate\Database\Eloquent\Model as Eloquent;

class PoisLinkId extends Eloquent{
	const schema = 'lookup';
	protected $connection = 'artefacts';
	protected $table = 'lookup.pois_adv_linkid';
	
}

?>