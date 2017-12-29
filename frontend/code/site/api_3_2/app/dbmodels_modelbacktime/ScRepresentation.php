<?php

namespace DbModels;

// use DbModels\ScProduct;
use Illuminate\Database\Capsule\Manager as DB;
use Illuminate\Database\Eloquent\Model as Eloquent;

class ScRepresentation extends Eloquent{
	protected $connection = 'model_backtime';
	protected $table = 'static_modelplus_definitions.screpresentations';
	
	public function scproducts(){
		return($this->belongsToMany('DbModels\ScProduct', 
		                            'static_modelplus_definitions.scproduct_screpresentation',
									'screpresentation_id',
									'scproduct_id'));
	}
	
	public function __toString(){ return((string)$this->id);}
	
	/**
	 * Flexible-size constructor
	 */
	public function __construct($arg1, $arg2=null, $arg3=null, $arg4=null){
		if (!is_null($arg4)){
			$this->construct_4($arg1, $arg2, $arg3, $arg4);
		} else {
			$this->construct_1($arg1);
		}
	}
	
	/**
	 * Construct from SQL function's tuple
	 */
	private function construct_1($sql_tuple){
		// parse tuple
		$cur_result = str_replace("(", "[", $sql_tuple);
		$cur_result = str_replace(")", "]", $cur_result);
		$cur_result = json_decode($cur_result);
		
		// set values
		$this->id = $cur_result[0];
		$this->title = trim($cur_result[1]);
		$this->type = $cur_result[2];
		$this->acronym = trim($cur_result[3]);
	}
	
	/**
	 * Construct from raw values
	 */
	private function construct_4($id, $title, $type, $acronym){
		$this->id = $id;
		$this->title = $title; 
		$this->type = $type;
		$this->acronym = $acronym;
	}
	
	# ------------------------------{ GENR }------------------------------- #
	
	/**
	 *
	 */
	public static function byCombining($repr_acronyms){
		$f_name = "get_screpresentations_combined";
		
		$pg_array = "ARRAY['".implode("','", $repr_acronyms)."']";
		$sql_command = "SELECT * FROM ".HlModel::schema.".".$f_name."(".$pg_array.");";
		$sql_result = DB::connection('model_backtime')->select($sql_command);
		$return_array = array();
		foreach($sql_result as $cur_result){
			array_push($return_array, 
			           new ScRepresentation($cur_result->id, 
											$cur_result->title,
											$cur_result->type, 
											$cur_result->acronym));
		}
		return($return_array);
	}
}

?>