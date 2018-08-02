<?php

	namespace Requester;

	// 
	class ModelCombinationSequenceMap{
		// TODO - remove it, it is not being used. Silly idea?
		
		private $model_id_past;
		private $model_id_fore;
		private $model_comb_id;
		private $model_comb_title;
		public $representations_ids;
		
		function set_model_ids($model_id_past, $model_id_fore){
			$this->model_id_past = $model_id_past;
			$this->model_id_fore = $model_id_fore;
			
			$past_id_splitted = explode("past", $model_id_past);
			$fore_id_splitted = explode("fore", $model_id_fore);
			if (($past_id_splitted == $fore_id_splitted)&&(sizeof($past_id_splitted) == 2)&&(sizeof($fore_id_splitted) == 2)){
				return($past_id_splitted[0].$past_id_splitted[1].$fore_id_splitted[1]);
			} else {
				return($past_id_splitted[0].$past_id_splitted[1].$fore_id_splitted[1]);
			}
		}
		
		function __construct(){
			$this->representations_ids = array();
		}
	}

?>