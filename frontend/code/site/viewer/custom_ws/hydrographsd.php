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
    //$sc_model_id = "fc254ifc01norain";
    $sc_reference_id = $_GET['sc_reference_id'];
  } else {
    exit();
  }

  /* definitions */
  $json_url = "repres_displayed/".$sc_model_id."/hydrographsd_".$sc_reference_id."/";
  $json_format = ".json";

  /*********************************************** DEFS **********************************************/
  
  /**
   * 
   * $sc_model_id : 
   * $cur_timestamp : 
   * RETURN : Associative list in the form of [link_id]->timestamp
   */
  function list_available_hydroforecasts_linkid($sc_model_id, $cur_timestamp){
    // list all files in directory
    $return_files = array();
    
    $all_file_names = DataAccess::list_datafolder_content($GLOBALS['json_url'], 
                                                          $GLOBALS['sc_runset_id'], 
                                                          $GLOBALS['json_format']);
    
    foreach($all_file_names as $cur_file_name){
      $cur_basename = basename($cur_file_name, $GLOBALS['json_format']);
      $splited_filename = explode("_", $cur_basename);
      if(($cur_timestamp == null) || ($cur_timestamp == $splited_filename[0])){
        $return_files[] = '"'.$splited_filename[1].'":'.$splited_filename[0];
      }
    }
    return($return_files);
  }
  
  /**
   * Auxiliar function for string processing
   * $haystack :
   * $needle :
   * RETURN : Boolean
   */
  function endsWith($haystack, $needle){
    return $needle === '' || substr_compare($haystack, $needle, -strlen($needle)) === 0;
  }

  /*********************************************** CALL **********************************************/
  
  $all_available_hydroforecasts = list_available_hydroforecasts_linkid($sc_model_id, null);
  echo("{\n  ");
  echo(implode(",\n  ", $all_available_hydroforecasts));
  echo("\n}");
  /*
  echo("<pre>");
  print_r($all_available_hydroforecasts);
  echo("</pre>");
  */
?>
