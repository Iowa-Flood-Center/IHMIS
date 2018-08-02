<?php

class FolderSystemFactory{
	
	const DEF_FILE_PATH =         "../../../../conf/site/api/fsconnection/fsdefinition.json";
	const DEF_DEPLOY_FILE_PATH =  "../../../../conf/site/api/fsconnection/fsdefinition_deploy.json";
	const DEF_SANDBOX_FILE_PATH = "../../../../conf/site/api/fsconnection/fsdefinition_sandbox.json";
	
	public static function create($is_sandbox=false){
		$folders_def = json_decode(file_get_contents(FolderSystemFactory::DEF_FILE_PATH), true);
		$folders_def = FolderSystemFactory::load_specific($folders_def, $is_sandbox);
		return((object)$folders_def);
	}
	
	private static function load_specific($general_obj, $is_sandbox=false){
		if($is_sandbox)
			$file_path = FolderSystemFactory::DEF_SANDBOX_FILE_PATH;
		else
			$file_path = FolderSystemFactory::DEF_DEPLOY_FILE_PATH;
		$folders_def = json_decode(file_get_contents($file_path), true);
		return (array_merge($general_obj, $folders_def));
	}
}

?>
