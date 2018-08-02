<?php
	header('Content-type: application/json');
	
	// //////////////////////////////////////// CONS //////////////////////////////////////// //
	
	$evaluations_possible_file_path = "/local/iihr/andre/model_backtime/settings/eval_matrix_options.json";
	
	// //////////////////////////////////////// FUNC //////////////////////////////////////// //
	
	function read_file_and_write_it(){
		global $evaluations_possible_file_path;
		
		$myfile = fopen($evaluations_possible_file_path, "r");
		echo(fread($myfile, filesize($evaluations_possible_file_path)));
		fclose($myfile);
	}
	
	// //////////////////////////////////////// CALL //////////////////////////////////////// //
	
	read_file_and_write_it();
?>