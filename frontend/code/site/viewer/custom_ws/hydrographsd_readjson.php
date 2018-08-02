<?php
  error_reporting(E_ALL | E_STRICT );
  ini_set("display_errors", 1);

  header("Content-Type: application/json");
  require_once("../../common/libs/data_access.php");

  // read sc_runset_id
  if(isset($_GET['sc_runset_id'])){
    $sc_runset_id = $_GET['sc_runset_id'];
  } else {
    exit();
  }
  
  // read sc_model_id
  if(isset($_GET['sc_model_id'])){
    $sc_model_id = $_GET['sc_model_id'];
  } else {
    exit();
  }
  
  // read sc_reference_id
  if(isset($_GET['sc_reference_id'])){
    $sc_reference_id = $_GET['sc_reference_id'];
  } else {
    exit();
  }
  
  // read link_id
  if(isset($_GET['link_id'])){
    $link_id = $_GET['link_id'];
  } else {
    exit();
  }
  
  // read timestamp
  if(isset($_GET['timestamp'])){
    $timestamp = $_GET['timestamp'];
  } else {
    exit();
  }
  
  /* definitions */
  $sc_eval_id = "hydrographsd";
  
  // get file url
  $json_fd_url = "repres_displayed/".$sc_model_id."/".$sc_eval_id."_".$sc_reference_id."/";
  $json_filename = $timestamp."_".$link_id.".json";
  $json_file_url = $json_fd_url.$json_filename;
  
  # read file and display it
  echo(DataAccess::get_datafile_content($json_file_url, $sc_runset_id));
?>
