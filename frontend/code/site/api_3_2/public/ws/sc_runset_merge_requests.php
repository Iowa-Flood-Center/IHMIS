<?php

require_once '../../common/libs/settings.php';

function process_post_request($app){
  // error_reporting(E_ALL);
  // ini_set('display_errors', 1);
  
  // get arguments
  $post_data = $app->request->post();
  
  // TODO - use logs
  
  // TODO - this following step may be defined in a separate file
  $out_folder = $app->fss->runsetmergers_waiting_room_folder_path;
  $out_filename = time().".json";
  $out_filepath = $out_folder.$out_filename;
  
  // do it
  $out_file = fopen($out_filepath,"w+");
  fwrite($out_file, json_encode($post_data, JSON_PRETTY_PRINT));
  fclose($out_file);
  
  echo('{"dispatch":"yes:'.$out_filepath.'"}');
}

function process_get_request($app){
  // error_reporting(E_ALL);
  // ini_set('display_errors', 1);
  
  // get params
  $from = $app->request->params("from");
  
  // TODO - use logs
  
  // TODO - this following step should be defined in a separate files (as RunsetRequest.php)
  if ($from == "waiting_room"){
    $file_ext = ".json";
    $waitingroom_folder_path = $app->fss->runsetmergers_waiting_room_folder_path;
      
    $all_files = scandir($waitingroom_folder_path);
    $all_retrieved = array();
    foreach($all_files as $cur_file){
      if (substr($cur_file, strlen($cur_file) - strlen($file_ext)) !== $file_ext) continue;
      $all_retrieved[] = $cur_file;
    }
  } else {
    $all_retrieved = array();
  }
  
  // show
  echo(json_encode($all_retrieved));
}

function process_delete_request($app, $file_name){
  $waitingroom_folder_path = $app->fss->runsetmergers_waiting_room_folder_path;
  $deleted_file_path = $waitingroom_folder_path.$file_name;
  if(unlink($deleted_file_path)){
    $ret = array("success"=>$file_name);
  } else {
    $ret = array("error"=>$file_name);
  }
  
  echo(json_encode($ret));
}

?>