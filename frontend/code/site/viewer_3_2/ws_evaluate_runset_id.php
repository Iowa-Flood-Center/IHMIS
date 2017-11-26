<?php
	header("Content-Type: text/plain");
	include_once("ws_metainfo_lib.php");
	
	// debug flag
	$debug = true;
	
	// get arguments
	$runset_id = get_arg("runsetid");
	$runset_title = get_arg("runset_title");
	$runset_title = str_replace("_", " ", $runset_title);
	
	// basic check
	if($runset_id == null){
		echo("F");
		if($debug){ echo(" - empty argument"); }
		return;
	}
	
	// basic name check
	if (preg_match('/[^A-Za-z0-9]/', $runset_id)){
		echo("F");
		if($debug){ echo(" - invalid character"); }
		return;
	}
	
	// check against its existing ones
	$runsets_rood_folder_path = MetaInfoDefs::BASE_FOLDER_PATH;
	$runset_sub_folder = "/metafiles/sc_runset/Runset.json";  // TODO - past it to common file
	$all_files = scandir($runsets_rood_folder_path);
	foreach($all_files as $cur_filename){
		// skip 'upper level folder' references
		if (($cur_filename == ".") || ($cur_filename == "..")){ continue; }
		
		// read Runset.json file if possible to establish current runset id and runset title
		$cur_runset_filepath = $runsets_rood_folder_path.$cur_filename.$runset_sub_folder;
		if (!file_exists($cur_runset_filepath)){
			$cur_id = $cur_filename;
			$cur_title = $cur_filename;
		} else {
			$cur_json_obj = json_decode(file_get_contents($cur_runset_filepath));
			$cur_id = $cur_filename;
			$cur_title = $cur_json_obj->sc_runset->title;
		}
		
		// non-repetitive evaluation
		if($runset_id == $cur_id){
			echo("F");
			if($debug){ echo(" - previously existing runset"); }
			return;
		} elseif (($runset_title != null) && (($runset_title == $cur_id))||($runset_title == $cur_title)){
			echo("F");
			if($debug){ echo(" - previously existing title"); }
			return;
		}
	}
	
	// if it got to this point, it deserves to be approved by Chuck Norris
	echo("T");
?>