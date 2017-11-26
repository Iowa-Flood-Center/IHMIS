<?php

abstract class MetaInfoDefs{
	
	// public attributes
	const BASE_FOLDER_HTTP = "http://s-iihr50.iihr.uiowa.edu/andre/model_3_0/metafiles/";
	const BASE_FOLDER_PATH = "/local/iihr/andre/model_3_1/";
	const METAFILES_FOLDER = "metafiles/";
	const SCRUNSET_FOLDER = "sc_runset";
	const SCMODEL_FOLDER = "sc_models";
	const SCMODELCOMB_FOLDER = "sc_modelcombinations";
	const SCREFERENCE_FOLDER = "sc_references";
	const SCMENU_FOLDER = "sc_menu";
	const SCMENU_FILENAME = "Menu.json";
	const SCREPRESENTATION_FOLDER = "sc_representations";
	const SCEVALUATION_FOLDER = "sc_evaluations";
	const COMPARISONMTX_FOLDER = "cross_matrices";
	const COMPARISONMTX_FILENAME = "Comparison_matrix.json";
	const EVALUATIONMTX_FILENAME = "Evaluation_matrix.json";
	
	// public methods
	
	/**
	 *
	 * $runset_id - String
	 * RETURN - String.
	 */
	public static function get_runset_folder_path($runset_id){
		return(MetaInfoDefs::BASE_FOLDER_PATH.$runset_id."/");
	}
	
	/**
	 *
	 * $runset_id - String
	 * RETURN - String.
	 */
	public static function get_metafiles_folder_path($runset_id){
		return(MetaInfoDefs::BASE_FOLDER_PATH.$runset_id."/".MetaInfoDefs::METAFILES_FOLDER);
	}
	
	/**
	 *
	 * $runset_id - String
	 * RETURN - String.
	 */
	public static function get_sc_runset_file_path($runset_id){
		$cur_file_name = "Runset.json";
		$cur_file_path = MetaInfoDefs::get_metafiles_folder_path($runset_id).MetaInfoDefs::SCRUNSET_FOLDER."/".$cur_file_name;
		return($cur_file_path);
	}
	
	/**
	 *
	 * $runset_id -
	 * RETURN - List of ScModel objects
	 */
	public static function load_all_sc_models($runset_id){
		// list all files in sc_model folder
		$models_folder = MetaInfoDefs::get_metafiles_folder_path($runset_id).MetaInfoDefs::SCMODEL_FOLDER;
		
		// basic check
		if(!file_exists($models_folder)){ return(array()); }
		
		// list files and add to the output array
		$all_filenames = scandir($models_folder);
		$return_array = array();
		ScModel::useConstructMinimal();
		foreach($all_filenames as $cur_filename){
			if (($cur_filename == ".") || ($cur_filename == "..")){ continue; }
			$cur_file_basename = basename($cur_filename, ".json");
			$cur_file_path = MetaInfoDefs::get_metafiles_folder_path($runset_id).MetaInfoDefs::SCMODEL_FOLDER."/".$cur_filename;
			$return_array[$cur_file_basename] = new ScModel($cur_file_path);
		}
		
		return($return_array);
	}
	
	/**
	 *
	 * $runset_id -
	 * RETURN - List of ScModelCombination objects
	 */
	public static function load_all_sc_modelcombinations($runset_id){
		
		$return_array = array();
		
		// define sc_model_combination folder and check if it exists
		$modelcombs_folder = MetaInfoDefs::get_metafiles_folder_path($runset_id).MetaInfoDefs::SCMODELCOMB_FOLDER;
		if(!file_exists($modelcombs_folder)){ return($return_array); }
		
		// list files and add to the output array
		$all_filenames = scandir($modelcombs_folder);
		foreach($all_filenames as $cur_filename){
			if (($cur_filename == ".") || ($cur_filename == "..")){ continue; }
			$cur_file_basename = basename($cur_filename, ".json");
			$cur_file_path = MetaInfoDefs::get_metafiles_folder_path($runset_id).MetaInfoDefs::SCMODELCOMB_FOLDER."/".$cur_filename;
			$return_array[$cur_file_basename] = new ScModelCombination($cur_file_path);
		}
		
		return($return_array);
	}
	
	// RETURN: List of ScReference objects
	public static function load_all_sc_references($runset_id){
		$meta_ref_folder_path = MetaInfoDefs::get_metafiles_folder_path($runset_id).MetaInfoDefs::SCREFERENCE_FOLDER;
		
		// basic check
		if (!file_exists($meta_ref_folder_path)){ return(array()); }
		
		// list all files in sc_reference folder
		$all_filenames = scandir($meta_ref_folder_path);
		$return_array = array();
		foreach($all_filenames as $cur_filename){
			if (($cur_filename == ".") || ($cur_filename == "..")){ continue; }
			$cur_file_basename = basename($cur_filename, ".json");
			$cur_file_path = $meta_ref_folder_path."/".$cur_filename;
			$return_array[$cur_file_basename] = new ScReference($cur_file_path);
		}
		
		return($return_array);
	}
	
	/**
	 *
	 * runset_id :
	 * RETURN : List of ScRepresentation objects
	 */
	public static function load_all_sc_representations($runset_id){
		$meta_repr_folder_path = MetaInfoDefs::get_metafiles_folder_path($runset_id).MetaInfoDefs::SCREPRESENTATION_FOLDER;
		
		// basic check
		if (!file_exists($meta_repr_folder_path)){ return(array()); }
		
		// list all files in sc_model folder
		$all_filenames = scandir($meta_repr_folder_path);
		$return_array = array();
		foreach($all_filenames as $cur_filename){
			if (($cur_filename == ".") || ($cur_filename == "..")){ continue; }
			$cur_file_basename = basename($cur_filename, ".json");
			$cur_file_path = $meta_repr_folder_path."/".$cur_filename;
			$return_array[$cur_file_basename] = new ScRepresentation($cur_file_path);
		}
		return($return_array);
	}
	
	// RETURN:
	public static function load_all_sc_evaluations($runset_id){
		$meta_eval_folder_path = MetaInfoDefs::get_metafiles_folder_path($runset_id).MetaInfoDefs::SCEVALUATION_FOLDER;
		
		// basic check
		if (!file_exists($meta_eval_folder_path)){ return(array()); }
		
		$all_filenames = scandir($meta_eval_folder_path);
		$return_array = array();
		foreach($all_filenames as $cur_filename){
			if (($cur_filename == ".") || ($cur_filename == "..")){ continue; }
			$cur_file_basename = basename($cur_filename, ".json");
			$cur_file_path = $meta_eval_folder_path."/".$cur_filename;
			$return_array[$cur_file_basename] = new ScEvaluation($cur_file_path);
		}
		return($return_array);
	}
	
	// RETURN: Dictionary with 'mdl1_mdl2'->['par1', 'par2']
	public static function load_comparison_matrix($runset_id){
		
		// build path
		$comp_mtx_folder_path = MetaInfoDefs::get_metafiles_folder_path($runset_id).MetaInfoDefs::COMPARISONMTX_FOLDER;
		$comp_mtx_file_path = $comp_mtx_folder_path."/".MetaInfoDefs::COMPARISONMTX_FILENAME;
		
		// basic check
		if (!file_exists($comp_mtx_file_path)){ return(array()); }
		
		// read file
		$json_obj = json_decode(file_get_contents($comp_mtx_file_path), true);
		return($json_obj["comparison_matrix"]);
	}
	
	// RETURN :
	public static function load_evaluation_matrix($runset_id){
		// build path
		$eval_mtx_folder_path = MetaInfoDefs::get_metafiles_folder_path($runset_id).MetaInfoDefs::COMPARISONMTX_FOLDER;
		$eval_mtx_file_path = $eval_mtx_folder_path."/".MetaInfoDefs::EVALUATIONMTX_FILENAME;
		
		// basic check
		if (!file_exists($eval_mtx_file_path)){ return(array()); }
		
		// read file
		$json_obj = json_decode(file_get_contents($eval_mtx_file_path), true);
		return($json_obj["evaluation_matrix"]);
	}
	
	// RETURN: 
	public static function load_ifis_model_parameters($model_id){
		
		// define file path
		$file_name = $model_id.".json";
		$file_path = MetaInfoDefs::BASE_FOLDER_PATH.MetaInfoDefs::ASYNCHMODEL_FOLDER."/".$file_name;
		
		// basic check
		if (!file_exists($file_path)){ return(array()); }
		
		// return list
		$json_obj = json_decode(file_get_contents($file_path), true);
		return($json_obj["asynch_model"]["parameter_set"]);
	}
	
	// 
	// RETURN:
	public static function load_menu_raw_str($runset_id){
		$sc_menu_folder_path = MetaInfoDefs::get_metafiles_folder_path($runset_id).MetaInfoDefs::SCMENU_FOLDER;
		$sc_menu_file_name = MetaInfoDefs::SCMENU_FILENAME;
		$sc_menu_file_path = $sc_menu_folder_path."/".$sc_menu_file_name;
		
		// basic check
		if (!file_exists($sc_menu_file_path)){ return('{"web_menu":{}}'); }
		
		return(file_get_contents($sc_menu_file_path));
	}
}

class ScObject{
	
	public static function get_optional_value($the_array, $the_key){
		if(array_key_exists($the_key, $the_array)){
			return($the_array[$the_key]);
		} else {
			return(null);
		}
	}
	
	public static function boolean_to_string($boolean_value){
		if($boolean_value){
			return("T");
		} else {
			return("F");
		}
	}
}

class ScModel{
	private static $construct_method = 1;  // 0:minimal, 1:complete, 2:total
	private $sc_model_id = null;
	private $sc_model_name = null;
	private $sc_model_description = null;
	private $sc_model_representation_set = null;
	private $sc_model_title_acronym = null;
	private $sc_show_main = true;
	
	public static function useConstructMinimal(){
		ScModel::$construct_method = 0;
	}
	
	public static function useConstructComplete(){
		ScModel::$construct_method = 1;
	}
	
	public static function useConstructTotal(){
		ScModel::$construct_method = 2;
	}
	
	public function __construct() {
		// 1 argument: JSON file path
		// 2 arguments: id and name
		$a = func_get_args();
        $i = func_num_args();
		if ($i >= 1) {
			$json_obj = json_decode(file_get_contents($a[0]), true);
			
			// basic constructor
			if (ScModel::$construct_method >= 0){
				$this->sc_model_id = $json_obj["sc_model"]["id"];
				$this->sc_model_name = $json_obj["sc_model"]["title"];
				if (isset($json_obj["sc_model"]["title_acronym"])){
					$this->sc_model_title_acronym = $json_obj["sc_model"]["title_acronym"];
				} else {
					$this->sc_model_title_acronym = $this->sc_model_id;
				}
				if(isset($json_obj["sc_model"]["show_main"])){
					$this->sc_show_main = $json_obj["sc_model"]["show_main"];
				}
			}
			
			// advanced constructor
			if (ScModel::$construct_method >= 1){
				$this->sc_model_description = $json_obj["sc_model"]["description"];
				if (isset($json_obj["sc_model"]["sc_representation_set"])){
					$this->sc_model_representation_set = $json_obj["sc_model"]["sc_representation_set"];
				} else {
					$this->sc_model_representation_set = null;
				}
			}
		}
	}
	
	// getters
	public function get_id(){ return ($this->sc_model_id); }
	public function get_name(){ return ($this->sc_model_name); }
	public function get_representation_set(){ return ($this->sc_model_representation_set); }
	public function get_title_acronym(){ return ($this->sc_model_title_acronym); }
	public function get_showmain(){ return ($this->sc_show_main); }
}

class ScModelCombination extends ScObject{
	private static $construct_method = 0;
	private $sc_modelcomb_id = null;
	private $sc_modelcomb_name = null;
	private $sc_modelcomb_description = null;
	private $sc_modelcomb_repres_set = null;
	private $sc_modelcomb_represcomb_set = null;
	
	public static function useConstructMinimal(){
		ScModelCombination::$construct_method = 0;
	}
	
	public static function useConstructTotal(){
		ScModelCombination::$construct_method = 2;
	}
	
	public function __construct() {
		// 1 argument: JSON file path
		// 2 arguments: id and name
		$a = func_get_args();
        $i = func_num_args();
		if ($i >= 1) {
			$json_obj = json_decode(file_get_contents($a[0]), true);
			
			$this->sc_modelcomb_id = $json_obj["sc_modelcombination"]["id"];
			$this->sc_modelcomb_name = $json_obj["sc_modelcombination"]["title"];
			
			if (ScModelCombination::$construct_method >= 1){
				$this->sc_modelcomb_description = ScModelCombination::get_optional_value($json_obj["sc_modelcombination"], 
																						 "description");
				// $this->sc_modelcomb_description = $json_obj["sc_modelcombination"]["description"];
				if(ScModelCombination::$construct_method >= 2){
					# add representations if they exist
					if (array_key_exists("sc_repres_set", $json_obj["sc_modelcombination"])){
						$tmp_dict_var = $json_obj["sc_modelcombination"]["sc_repres_set"];
						if (array_key_exists("sc_repr", $tmp_dict_var)){
							$this->sc_modelcomb_repres_set = $tmp_dict_var["sc_repr"];
						} else {
							$this->sc_modelcomb_repres_set = null;
						}
					} else {
						$this->sc_modelcomb_repres_set = null;
					}
					
					# add representation combinations if they exist
					if (array_key_exists("sc_represcomb_set", $json_obj["sc_modelcombination"])){
						$this->sc_modelcomb_represcomb_set = $json_obj["sc_modelcombination"]["sc_represcomb_set"];
					} else {
						$this->sc_modelcomb_represcomb_set = null;
					}
				}
			}
		}
	}
	
	// getters
	public function get_id(){ return ($this->sc_modelcomb_id); }
	public function get_name(){ return ($this->sc_modelcomb_name); }
	public function get_description(){ return ($this->sc_modelcomb_description); }
	public function get_repres_set(){ return ($this->sc_modelcomb_repres_set); }
	public function get_represcomb_set(){ return ($this->sc_modelcomb_represcomb_set); }
}

class ScReference{
	private $sc_reference_id = null;
	private $sc_reference_title = null;
	private $sc_reference_title_acronym = null;
	
	public function __construct() {
		$a = func_get_args();
        $i = func_num_args();
		if ($i == 1) {
			// one argument: JSON file path
			$json_obj = json_decode(file_get_contents($a[0]), true);
			
			$this->sc_reference_id = $json_obj["sc_reference"]["id"];
			$this->sc_reference_title = $json_obj["sc_reference"]["title"];
			$this->sc_reference_title_acronym = $this->get_optional_attribute("title_acronym", $json_obj);
		}
	}
	
	// getters
	public function get_id(){ return ($this->sc_reference_id); }
	public function get_title(){ return ($this->sc_reference_title); }
	public function get_title_acronym(){ return ($this->sc_reference_title_acronym); }
	
	/**
	 *
	 * $attribute_id : 
	 * $json_obj : 
	 * RETURN : 
	 */
	private function get_optional_attribute($attribute_id, $json_obj){
		if (array_key_exists($attribute_id, $json_obj["sc_reference"])){
			return($json_obj["sc_reference"][$attribute_id]);
		} else {
			return(null);
		}
	}
}

class ScRepresentation{
	private $sc_representation_id = null;
	private $sc_representation_name = null;
	private $sc_description = null;
	private $sc_call_radio = null;
	private $sc_call_select = null;
	private $sc_legend = null;
	private $sc_legend_sing = null;
	private $sc_legend_comp = null;
	private $representation = null;
	private $time_interval = null;
	private $sc_calendar_type = null;
	
	public function __construct() {
		// 1 argument: JSON file path
		// 2 arguments: id and name
		$a = func_get_args();
        $i = func_num_args();
		if ($i == 1) {
			// one argument: JSON file path
			$json_obj = json_decode(file_get_contents($a[0]), true);
			
			$this->sc_representation_id = $json_obj["sc_representation"]["id"];
			if (isset($json_obj["sc_representation"]["comments"])){
				$this->sc_description = $json_obj["sc_representation"]["comments"];
			} else {
				$this->sc_description = "";
			}
			$this->time_interval = $this->get_optional_attribute("time_interval", $json_obj);
			$this->sc_calendar_type = $this->get_optional_attribute("calendar_type", $json_obj);
			$this->sc_call_radio = $this->get_optional_attribute("call_radio", $json_obj);
			$this->sc_call_select = $this->get_optional_attribute("call_select", $json_obj);
			$this->sc_legend = $this->get_optional_attribute("legend", $json_obj);
			$this->sc_legend_sing = $this->get_optional_attribute("legend_sing", $json_obj);
			$this->sc_legend_comp = $this->get_optional_attribute("legend_comp", $json_obj);
			$this->representation = $this->get_optional_attribute("representation", $json_obj);
		} elseif ($i == 2) {
			$this->sc_representation_id = $a[0];
			$this->sc_description = $a[1];
        }
	}
	
	// getters
	public function get_id(){ return ($this->sc_representation_id); }
	public function get_description(){ return ($this->sc_description); }
	public function get_callRadio(){ return ($this->sc_call_radio); }
	public function get_callSelect(){ return ($this->sc_call_select); }
	public function get_legend(){ return ($this->sc_legend); }
	public function get_legend_sing(){ return ($this->sc_legend_sing); }
	public function get_legend_comp(){ return ($this->sc_legend_comp); }
	public function get_representation(){ return ($this->representation); }
	public function get_time_interval(){ return ($this->time_interval); }
	public function get_calendar_type(){ return ($this->sc_calendar_type); }
	
	/**
	 *
	 * $attribute_id : 
	 * $json_obj : 
	 * RETURN : 
	 */
	private function get_optional_attribute($attribute_id, $json_obj){
		if (array_key_exists($attribute_id, $json_obj["sc_representation"])){
			return($json_obj["sc_representation"][$attribute_id]);
		} else {
			return(null);
		}
	}
}

class ScEvaluation{
	private $sc_evaluation_id = null;
	
	public function __construct() {
		$a = func_get_args();
        $i = func_num_args();
		if ($i == 1) {
			// one argument: JSON file path
			$json_obj = json_decode(file_get_contents($a[0]), true);
			
			$this->sc_evaluation_id = $json_obj["sc_evaluation"]["id"];
			$this->sc_evaluation_description = $json_obj["sc_evaluation"]["comments"];
		}
	}
	
	// getters
	public function get_id(){ return ($this->sc_evaluation_id); }
	public function get_description(){ return ($this->sc_evaluation_description); }
}

class ScComparisonMatrix{
	
	
	public function get_comparison_set($runset_id, $scmodel_id){
		return(array());
	}
}

class ScEvaluationMatrix{
	private $json_obj;
	
	public function __construct() {
		$a = func_get_args();
        $i = func_num_args();
		if ($i == 0) {
			$this->json_obj = MetaInfoDefs::load_evaluation_matrix();
		} elseif ($i == 1) {
			$this->json_obj = MetaInfoDefs::load_evaluation_matrix($a[0]);
		}
	}
	
	public function get_evaluation_set($runset_id, $scmodel_id){
		$ret_array = array();
		foreach($this->json_obj as $cur_id => $cur_models){
			if (in_array($scmodel_id, $cur_models)){
				$ret_array[] = $cur_id;
			}
		}
		return($ret_array);
	}
}

function get_arg($argument_name){
	// Retrive argument past using GET
	if(isset($_GET[$argument_name]) && trim($_GET[$argument_name])){
		return($_GET[$argument_name]);
	} else {
		return(null);
	}
}

?>