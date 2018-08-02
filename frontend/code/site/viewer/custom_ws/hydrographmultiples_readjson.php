<?php
  require_once("libs/debug.php");
  require_once("libs/headers.php");
  
  /*********************************************** ARGS **********************************************/

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
  
  // read link_id
  if(isset($_GET['link_id'])){
    $link_id = $_GET['link_id'];
  } else {
    exit();
  }
  
  $sc_represcomb_id = "hydrographmultiples";
  
  /**
   *
   * $filename -
   * $link_id -
   * RETURN - 
   */
  function check_file_is_linkid($filename, $link_id){
    // ignore back folders references
    if (($filename == ".") || ($filename == "..")){ return(false); }
    
    $aaa = explode("_",basename($filename, ".json"));
    if ($aaa[1] == $link_id){
      return(true);
    } else {
      //echo($aaa[1]."!=".$link_id.". ");
      return(false);
    }
  }
  
  $root_folder_url = "repres_displayed/".$sc_model_id."/".$sc_represcomb_id."/";
  $common_folder_path = $root_folder_url."common/";
  $modelpaststg_folder_path = $root_folder_url."modelpaststg/";
  $modelforestg_folder_path = $root_folder_url."modelforestg/";
  
  $modelpaststg_dict = array();
  $modelforestg_dict = array();
  $output_dict = array();
  
  // find all files related to the linkid in each folder
  $all_scmodel_folders = DataAccess::list_datafolder_content($modelforestg_folder_path, 
                                                             $sc_runset_id,
                                                             "\/");
  foreach($all_scmodel_folders as $cur_scmodel_folder){
    // ignore back folders references
    if (($cur_scmodel_folder == ".") || ($cur_scmodel_folder == "..")){ continue; }
    
    $cur_subfolder_path = $modelforestg_folder_path.$cur_scmodel_folder."/";
    $all_inner_files = DataAccess::list_datafolder_content($cur_subfolder_path, 
                                                             $sc_runset_id,
                                                             ".json");
    foreach($all_inner_files as $cur_inner_file){
      if (check_file_is_linkid($cur_inner_file, $link_id)){
        $cur_inner_file_path = $cur_subfolder_path.$cur_inner_file;
        $file_content = DataAccess::get_datafile_content($cur_inner_file_path,
                                                         $sc_runset_id);
        $modelforestg_dict[$cur_scmodel_folder] = json_decode($file_content, true);
      }
    }
  }
  
  // $all_scmodel_folders = scandir($modelpaststg_folder_path);
  $all_scmodel_folders = DataAccess::list_datafolder_content($modelpaststg_folder_path,
                                                             $sc_runset_id,
                                                             "\/");
  foreach($all_scmodel_folders as $cur_scmodel_folder){
    // ignore back folders references
    if (($cur_scmodel_folder == ".") || ($cur_scmodel_folder == "..")){ continue; }
    
    $cur_subfolder_path = $modelpaststg_folder_path.$cur_scmodel_folder."/";
    $all_inner_files = DataAccess::list_datafolder_content($cur_subfolder_path,
                                                           $sc_runset_id,
                                                           ".json");
    foreach($all_inner_files as $cur_inner_file){
      if (check_file_is_linkid($cur_inner_file, $link_id)){
        $cur_inner_file_path = $cur_subfolder_path.$cur_inner_file;
        $file_content = DataAccess::get_datafile_content($cur_inner_file_path,
                                                         $sc_runset_id);
        $modelpaststg_dict[$cur_scmodel_folder] = json_decode($file_content, true);
      }
    }
  }
  
  // load common information
  $common_file_path = $common_folder_path.$link_id.".json";
  $file_content = DataAccess::get_datafile_content($common_file_path,
                                                   $sc_runset_id);
  $common_dict = json_decode($file_content, true);
  
  // build output object and print it
  $output_dict["fore"] = $modelforestg_dict;
  $output_dict["past"] = $modelpaststg_dict;
  $output_dict["common"] = $common_dict;
  echo(json_encode($output_dict));
?>
