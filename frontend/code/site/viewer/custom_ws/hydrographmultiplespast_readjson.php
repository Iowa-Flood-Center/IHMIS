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
  
  $sc_represcomb_id = "hydrographmultiplespast";
  
  /*********************************************** DEFS **********************************************/
  
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
  
  /*********************************************** CALL **********************************************/
  
  $root_folder_url = "repres_displayed/".$sc_model_id."/".$sc_represcomb_id."/";
  $common_folder_path = $root_folder_url."common/";
  $stageref_folder_path = $root_folder_url."stageref/";
  $dischref_folder_path = $root_folder_url."dischref/";
  $modelpaststg_folder_path = $root_folder_url."modelpaststg/";
  
  $modelpaststg_dict = array();
  $stageref_dict = array();
  $dischref_dict = array();
  $output_dict = array();
  
  // will find all files related to the linkid in each folder
  
  // will find all 'stageref' files
  if (DataAccess::check_datafile_exists($stageref_folder_path, 
                                        $sc_runset_id)){
    $all_scref_folders = DataAccess::list_datafolder_content($stageref_folder_path, 
                                                             $sc_runset_id,
                                                             "\/");
    foreach($all_scref_folders as $cur_scref_folder){
      // ignore back folders references
      if (($cur_scref_folder == ".") || ($cur_scref_folder == "..")){ continue; }
      
      $cur_subfolder_path = $stageref_folder_path.$cur_scref_folder."/";
      $all_inner_files = DataAccess::list_datafolder_content($cur_subfolder_path, 
                                                             $sc_runset_id,
                                                             ".json");
      foreach($all_inner_files as $cur_inner_file){
        if (check_file_is_linkid($cur_inner_file, $link_id)){
          $cur_inner_file_path = $cur_subfolder_path.$cur_inner_file;
          $file_content = DataAccess::get_datafile_content($cur_inner_file_path,
                                                           $sc_runset_id);
          $stageref_dict[$cur_scref_folder] = json_decode($file_content, true);
        }
      }
    }
  }
  
  // will find all 'dischref' files
  if (DataAccess::check_datafile_exists($dischref_folder_path,
                                        $sc_runset_id)){
    $all_scref_folders = DataAccess::list_datafolder_content($dischref_folder_path,
                                                             $sc_runset_id,
                                                             "\/");
    foreach($all_scref_folders as $cur_scref_folder){
      // ignore back folders references
      if (($cur_scref_folder == ".") || ($cur_scref_folder == "..")){ continue; }
      
      $cur_subfolder_path = $dischref_folder_path.$cur_scref_folder."/";
      $all_inner_files = scandir($cur_subfolder_path);
      foreach($all_inner_files as $cur_inner_file){
        if (check_file_is_linkid($cur_inner_file, $link_id)){
          $cur_inner_file_path = $cur_subfolder_path.$cur_inner_file;
          $stageref_dict[$cur_scref_folder] = json_decode(file_get_contents($cur_inner_file_path), true);
        }
      }
    }
  }
  
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
        $cur_file_content = DataAccess::get_datafile_content($cur_inner_file_path,
                                                             $sc_runset_id);
        $modelpaststg_dict[$cur_scmodel_folder] = json_decode($cur_file_content, true);
      }
    }
  }
  
  // load common information
  $common_file_path = $common_folder_path.$link_id.".json";
  $common_dict = DataAccess::get_datafile_content($common_file_path,
                                                  $sc_runset_id);
  $common_dict = json_decode($common_dict, true);
  
  // build output object and print it
  $output_dict["sref"] = $stageref_dict;
  $output_dict["past"] = $modelpaststg_dict;
  $output_dict["common"] = $common_dict;
  echo(json_encode($output_dict));
?>
