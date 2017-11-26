<?php 
	header("Content-Type: text/plain");
	
	// //////////////////////////////////////// ARGS //////////////////////////////////////// //
	
	// basic check
	if (!isset($_GET['evaluation_id'])){
		echo("Missing 'runset id'.");
		exit();
	}
	$the_eval_id = $_GET['evaluation_id'];
	
	// //////////////////////////////////////// CONS //////////////////////////////////////// //
	
	$evaluations_possible_file_path = "/local/iihr/andre/model_backtime/settings/eval_matrix_options.json";
	
	// //////////////////////////////////////// FUNC //////////////////////////////////////// //
	
	function read_file_and_rewrite_it($removed_evaluation_id){
		global $evaluations_possible_file_path;
		
		// read content
		$myfile = fopen($evaluations_possible_file_path, "r");
		$file_content = fread($myfile, filesize($evaluations_possible_file_path));
		fclose($myfile);
		
		// replace content
		$json_obj = json_decode($file_content);
		$the_list = $json_obj->evaluation_matrix_options;
		if (($key = array_search($removed_evaluation_id, $the_list)) !== false) {
			unset($the_list[$key]);
		}
		$json_obj->evaluation_matrix_options = $the_list;
		$new_file_content = json_encode($json_obj);
		
		// write new content
		file_put_contents($evaluations_possible_file_path, $new_file_content);
	}
	
	// //////////////////////////////////////// CALL //////////////////////////////////////// //
	read_file_and_rewrite_it($the_eval_id);
?>