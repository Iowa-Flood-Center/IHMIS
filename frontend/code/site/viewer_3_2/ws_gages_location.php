<?php
header("Content-Type: text/plain");
include_once("ws_metainfo_lib.php");
include_once("../common/libs/settings.php");

/************************************* ARGS *************************************/	
	
$file_date = get_arg("filedate");
if ($file_date == null){ $file_date = "20160628"; }

/************************************* DEFS *************************************/

$anci_folder_path = Settings::get_property("raw_data_folder_path");
$anci_folder_path .= "anci/gauges_location/";
$gages_csv_file_path = $anci_folder_path."gauges_location_".$file_date.".csv";
$has_header = true;
	
/************************************* CALL *************************************/

if (file_exists($gages_csv_file_path)){
	// read and print file content if it exists
	$f_handler = fopen($gages_csv_file_path, "r");
	$desc_file_data = "{\n";
	$desc_file_data .= " \"gauge\":[\n";
	$is_first = true;
	
	// skip current line
	if ($has_header){ fgets($f_handler); }
	
	// read all lines
	while (($cur_line = fgets($f_handler)) !== false) {
		# skip first comma
        if(!$is_first){ $desc_file_data .= ", \n"; }
		$is_first = false;
		
		# write content
		$splitted_line = explode(",", trim($cur_line));
		$desc_file_data .= " {\n";
		$desc_file_data .= sprintf("  \"ifis_id\":%s,\n", $splitted_line[0]);
		$desc_file_data .= sprintf("  \"link_id\":%s,\n", $splitted_line[1]);
		$desc_file_data .= sprintf("  \"lat\":%s,\n", $splitted_line[2]);
		$desc_file_data .= sprintf("  \"lng\":%s,\n", $splitted_line[3]);
		$desc_file_data .= sprintf("  \"type\":%s,\n", $splitted_line[4]);
		$desc_file_data .= sprintf("  \"desc\":\"%s\"", $splitted_line[5]);
		// $desc_file_data .= sprintf("  \"type\":%s\n", $splitted_line[4]);
		$desc_file_data .= " }";
    }
	$desc_file_data .= "\n]}";
		
} else {
	// generate an error message
	$desc_file_data = '{"error":"Gages CSV file not found '.$gages_csv_file_path.'"}';
}

echo($desc_file_data);
?>
