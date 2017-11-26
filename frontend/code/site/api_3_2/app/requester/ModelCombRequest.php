<?php

	namespace Requester;
	
	use Requester\AuxFilesLib as AuxFilesLib;

	// 
	class ModelCombRequest{
		public $repr_comb_id;
		public $roles;
		
		public function __construct($repr_comb_id, $the_array){
			$this->repr_comb_id = $repr_comb_id;
			$this->roles = $the_array;
		}
		
		public function create_file($current_timestamp){
			$folder_path = AuxFilesLib::get_local_temp_meta_folder_path($current_timestamp, 
			                                                            $subfolder="modelcomb");
			$file_path = $folder_path.$this->repr_comb_id."mdlcomb.json";
			
			$file_content = array();
			$file_content["sc_modelcombination"] = array();
			$file_content["sc_modelcombination"]["id"] = $this->repr_comb_id."mdlcomb";
			$file_content["sc_modelcombination"]["title"] = $this->repr_comb_id."mdlcomb";
			$file_content["sc_modelcombination"]["sc_represcomb_set"] = array();
			$file_content["sc_modelcombination"]["sc_represcomb_set"][$this->repr_comb_id ] = $this->roles;
			$file_content["sc_modelcombination"]["description"] = "";

			$file_content = json_encode($file_content);
			$file_content = str_replace('\"', '"', $file_content);
			
			$file = fopen($file_path,"w");
			echo(fwrite($file, $file_content));
			fclose($file);
		}
		
	}

?>