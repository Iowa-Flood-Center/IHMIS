<?php
	if ($_SERVER['SERVER_NAME']=='s-iihr50.iihr.uiowa.edu') { // for local development
		include_once "/local/iihr/ifis.iowawis.org/sc/inc_config.php";
	} else {
		include_once "../inc_config.php"; 
	}

	// function IFIS_Init(IFIS Plus mode (0 or 1 integer), title of the page (string), id for special case project (string)) {
	if ($_SERVER['SERVER_NAME']=='s-iihr50.iihr.uiowa.edu') { // for local development
		IFIS_Init(1, 'IFIS MODEL 3.1', 'test1/modelplus_3_1_git/frontend/viewer_3_1', 1);
	} else {
		IFIS_Init(1, 'IFIS MODEL 3.1', 'modelplus', 1);
	}
?>