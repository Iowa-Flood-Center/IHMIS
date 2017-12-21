<?php

function process_get_request($app){
  // get params
  $action = $app->request->params("do");
  
  $all_retrieved = array();
  
  if(!is_null($action)){
    switch($action){
      case "get_new_runset_id":
        // list all auto_names and get the latest one
        $auto_folders = glob($app->fss->runsets_result_folder_path."rset[0-9]*");
        rsort($auto_folders);
        if (count($auto_folders) > 0) {
          // get latest
          $latest_filename = basename($auto_folders[0]);
          $latest_time = (int)substr($latest_filename, 4);
        } else {
          // start from 0
          $latest_time = 0;
        }
        
        $the_time = $latest_time + 1;
        
        $all_retrieved["runset_id"] = "rset".sprintf('%06d', $latest_time);
        break;
    }
  }
  
  // show
  echo(json_encode($all_retrieved));
}

?>