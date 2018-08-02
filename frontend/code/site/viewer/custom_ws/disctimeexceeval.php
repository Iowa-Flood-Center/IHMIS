<?php
  require_once("libs/debug.php");
  require_once("libs/headers.php");
  
  /*********************************************** ARGS **********************************************/
  
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
  
  // read sc_runset_id
  if(isset($_GET['sc_runset_id'])){
    $sc_runset_id = $_GET['sc_runset_id'];
  } else {
    $sc_runset_id = null;
  }
  
  // read reference time
  if(isset($_GET['ref_time'])){
    $sc_reftime = $_GET['ref_time'];
  } else {
    $sc_reftime = 0;
  }
  
  // read timestamp
  if(isset($_GET['ref_timestamp'])){
    $sc_reftimestamp = $_GET['ref_timestamp'];
  } else {
    $sc_reftimestamp = null;
  }

  /*********************************************** CONS **********************************************/
  
  /* definitions */
  $sc_evaluation_id = "disctimeexceeval";
  
  $sc_ref0_file_path = "txts_timestamp_ref0/".$sc_model_id."/".$sc_evaluation_id."_".$sc_reference_id.".txt";
  $json_folder = "repres_displayed/".$sc_model_id."/".$sc_evaluation_id."_".$sc_reference_id."/";
  $json_format = $sc_evaluation_id.".json";
  
  /*********************************************** DEFS **********************************************/
  
  /**
   * Just read the ref0 file content
   * RETURN : Integer if possible to read file. Null otherwise.
   */
  function read_ref0_timestamp($file_path, $runset_id){
    if(DataAccess::check_datafile_exists($file_path, $runset_id)){
      $file_content = DataAccess::get_datafile_content($file_path, 
                                                       $runset_id);
      return((int)trim($file_content));
    } else {
      echo("File '".$file_path."' not found.");
      return(null);
    }
  }
  
  /**
   *
   * $ref0_timestamp : ref0 timestamp
   * $ref_timestamp : 
   * $ref_time : A value starting at 0 for ref0 timestamp
   * RETURN :
   */
  function setup_reftime($ref0_timestamp, $ref_timestamp, $ref_time){
    if ($ref_timestamp == null){
      return($ref_time);
    } else {
      return(($ref0_timestamp - $ref_timestamp)/3600);
    }
  }
  
  /**
   * Reads a JSON file.
   * $ref_time_arg : 
   * $json_folder_arg : 
   * $json_format_arg : 
   * $runset_id :
   * RETURN : Filled text if file was found, empty text ("") otherwise.
   */
  function read_file($ref_time_arg, $json_folder_arg, $json_format_arg,
                     $runset_id){
    $file_path = $json_folder_arg.$ref_time_arg.$json_format_arg;
    if(DataAccess::check_datafile_exists($file_path, $runset_id)){
      return(DataAccess::get_datafile_content($file_path, $runset_id));
    } else {
      return("");
    }
  }
  
  /**
   * Define the value of previous daily time available.
   * $ref0_timestamp : 
   * $effc_timestamp :
   * $json_folder :
   * $json_format :
   * RETURN : A positive integer if a previous value is expected to be available, '-1' otherwise.
   */
  function setup_prev_d_timestamp($ref0_timestamp, $effc_timestamp, 
                                  $json_folder, $json_format,
                                  $runset_id){
    $poss_timestamp = $effc_timestamp - (24 * 3600);
    $poss_reftime = setup_reftime($ref0_timestamp, $poss_timestamp, null);
    $poss_file_path = $json_folder.$poss_reftime.$json_format;
    if(!DataAccess::check_datafile_exists($poss_file_path, $runset_id)){
      return(-1);
    } else {
      return($poss_timestamp);
    }
  }
  
  /**
   * Define the value of previous hourly time available.
   * $ref0_timestamp : 
   * $effc_timestamp :
   * $json_folder :
   * $json_format :
   * RETURN : A positive integer if a previous value is expected to be available, '-1' otherwise.
   */
  function setup_prev_h_timestamp($ref0_timestamp, $effc_timestamp, 
                                  $json_folder, $json_format,
                                  $runset_id){
    $poss_timestamp = $effc_timestamp - 3600;
    $poss_reftime = setup_reftime($ref0_timestamp, $poss_timestamp, null);
    $poss_file_path = $json_folder.$poss_reftime.$json_format;
    if(!DataAccess::get_datafile_content($poss_file_path, $runset_id)){
      return(-1);
    } else {
      return($poss_timestamp);
    }
  }
  
  /**
   * Define the value of next hourly time available.
   * $ref0_timestamp : 
   * $effc_timestamp :
   * RETURN : A positive integer if a next value is expected to be available, '-1' otherwise.
   */
  function setup_next_h_timestamp($ref0_timestamp, $effc_timestamp){
    if ($effc_timestamp > ($ref0_timestamp - 3600)){
      return(-1);
    } else {
      return($effc_timestamp + 3600);
    }
  }
  
  /**
   * Define the value of next daily time available.
   * $ref0_timestamp : 
   * $effc_timestamp :
   * RETURN : A positive integer if a next value is expected to be available, '-1' otherwise.
   */
  function setup_next_d_timestamp($ref0_timestamp, $effc_timestamp){
    if ($effc_timestamp > ($ref0_timestamp - (24 * 3600))){
      return(-1);
    } else {
      return($effc_timestamp + 3600);
    }
  }
  
  /*********************************************** CALL **********************************************/
  
  $ref0_timestamp = read_ref0_timestamp($sc_ref0_file_path, $sc_runset_id);
  // echo("\$sc_reftimestamp:".$sc_reftimestamp."\n");
  $sc_reftime = setup_reftime($ref0_timestamp, $sc_reftimestamp, $sc_reftime);
  $effc_timestamp = $ref0_timestamp - ($sc_reftime * 3600);
  $json_file_path = $json_folder.$sc_reftime.$json_format;
  $file_content = DataAccess::get_datafile_content($json_file_path,
                                                   $sc_runset_id);
  $json_content = json_decode($file_content);
  if ($json_content != null){
    // $json_content->file_path = $json_file_path;
    $json_content->timestamp = $effc_timestamp;
    $json_content->timestamp_prev_d = setup_prev_d_timestamp($ref0_timestamp, $effc_timestamp, $json_folder, $json_format, $sc_runset_id);
    $json_content->timestamp_prev_h = setup_prev_h_timestamp($ref0_timestamp, $effc_timestamp, $json_folder, $json_format, $sc_runset_id);
    $json_content->timestamp_next_h = setup_next_h_timestamp($ref0_timestamp, $effc_timestamp);
    $json_content->timestamp_next_d = setup_next_d_timestamp($ref0_timestamp, $effc_timestamp);
    echo(json_encode($json_content));
  } else {
    echo('{"error":"No content in '.$sc_reftime.', '.$json_folder.','.$json_format.'"}');
  }
?>
