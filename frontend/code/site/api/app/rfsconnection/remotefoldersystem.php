<?php

class RemoteFolderSystemFactory{
	
	const DEF_FILE_PATH = "../../../../conf/site/api/rfsconnection/rfsdefinition.json";
	
	public static function create(){
        $fi_content = file_get_contents(RemoteFolderSystemFactory::DEF_FILE_PATH);
		$fd_def = json_decode($fi_content, true);
		return((object)$fd_def);
	}
}

?>
