<?php
  require_once("libs/debug.php");
  require_once("libs/headers.php");
  
  /*********************************************** ARGS **********************************************/
  
  // read sc_runset_id
  if(isset($_GET['sc_runset_id'])){
    $sc_runset_id = $_GET['sc_runset_id'];
  } else {
    echo('{"ERROR":"Missing parameter \'runset_id\'."}');
    exit();
  }
  
  // read sc_modelcomb_id
  if(isset($_GET['sc_modelcomb_id'])){
    $sc_modelcomb_id = $_GET['sc_modelcomb_id'];
  } else {
    echo('{"ERROR":"Missing parameter \'sc_modelcomb_id\'."}');
    exit();
  }
  
  // read sc_modelcomb_id
  $sc_represcomb_id = "hydrographmultiplesalertcurrent";
  
  /*********************************************** DEFS **********************************************/
  
  /*********************************************** CALL **********************************************/
  
  // definitions - meta
  $modelcomb_metafile_url = "sc_modelcombinations/".$sc_modelcomb_id.".json";
  $represcomb_metafile_url = "sc_represcomps/".$sc_represcomb_id.".json";
  
  // definitions - data
  $basic_data_folder_url = "repres_displayed/";
  $basic_data_folder_url .= $sc_modelcomb_id."/".$sc_represcomb_id."/";
  $common_files_folder_url = $basic_data_folder_url."common/";
  
  // basic files check
  if (!DataAccess::check_metafile_exists($modelcomb_metafile_url, 
                                         $sc_runset_id)){
    echo('{"ERROR":"Missing file \''.$modelcomb_metafile_url.'\'."}');
    exit;
  }
  if (!DataAccess::check_metafile_exists($represcomb_metafile_url, 
                                         $sc_runset_id)){
    echo('{"ERROR":"Missing file \''.$represcomb_metafile_url.'\'."}');
    exit;
  }
  
  // plot data
  echo("{\n");
  $all_common_files = DataAccess::list_datafolder_content($common_files_folder_url,
                                                          $sc_runset_id,
                                                          ".json");
  $links_array = array();
  foreach($all_common_files as $cur_common_file_name){
    // ignore back folders references
    if (($cur_common_file_name == ".") || ($cur_common_file_name == "..")){ continue; }
    
    // read file
    $cur_common_file_url = $common_files_folder_url.$cur_common_file_name;
    $cur_common_file_json = DataAccess::get_datafile_content($cur_common_file_url, 
                                                             $sc_runset_id);
    $cur_common_file_json = json_decode($cur_common_file_json);
    
    $cur_common_linkid = basename($cur_common_file_name, ".json");
    
    $links_array[] = (" \"".$cur_common_linkid."\":".$cur_common_file_json->fld_level);
  }
  echo(implode(",\n", $links_array));
  echo("\n}");
?>
