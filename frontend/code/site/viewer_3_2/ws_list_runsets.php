<?php
	header('Content-Type: application/json');
	include_once("ws_metainfo_lib.php");
	
	$runsets_rood_folder_path = MetaInfoDefs::BASE_FOLDER_PATH;
	
	// TODO - past it to common file
	$runset_sub_folder = "/metafiles/sc_runset/Runset.json";
	
	$all_files = scandir($runsets_rood_folder_path);
	
	// for each runset folder, try to read its inner sc_runset meta file
	$return_array = array();
	foreach($all_files as $cur_filename){
		if (($cur_filename == ".") || ($cur_filename == "..")){ continue; }
		
		$runset_filepath = $runsets_rood_folder_path.$cur_filename.$runset_sub_folder;
		
		if ((!file_exists($runset_filepath)) && (!readlink($runset_filepath))){
			$cur_id = $cur_filename;
			$cur_title = $cur_filename;
			$cur_show_main = "File does not exist: '".$runset_filepath."'.";
		} else {
			$the_runset_filepath = is_link($runset_filepath) ? readlink($runset_filepath) : $runset_filepath;			
			$cur_json_obj = json_decode(file_get_contents($the_runset_filepath));
			$cur_id = $cur_filename;
			$cur_title = $cur_json_obj->sc_runset->title;
			if(isset($cur_json_obj->sc_runset->show_main)){
				$cur_show_main = ScObject::boolean_to_string($cur_json_obj->sc_runset->show_main);
			} else {
				$cur_show_main = ScObject::boolean_to_string(true);
			}
		}
		$cur_str =  " {\n";
		$cur_str .= "  \"id\":\"".$cur_id."\",\n";
		$cur_str .= "  \"title\":\"".$cur_title."\",\n";
		$cur_str .= "  \"show_main\":\"".$cur_show_main."\"\n";
		$cur_str .= " }";
		$return_array[] = $cur_str;
	}
	
	echo("[\n".implode($return_array, ",\n")."]");
?>