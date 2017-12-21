<?php
  const FOLDER_PATH = "/tmp/";
  const FILE_NAME_PATTERN = "/^[0-9]+$|^[0-9]+\.tar\.gz$/";
  
  // display errors
  ini_set('display_errors', 1);
  ini_set('display_startup_errors', 1);
  error_reporting(E_ALL);
  
  // clean files
  $count_del = 0;
  $all_file_names = scandir(FOLDER_PATH);
  foreach($all_file_names as $file_name){
    if(!preg_match(FILE_NAME_PATTERN, $file_name)) continue;
    $f_path = FOLDER_PATH.$file_name;
	if(is_dir($f_path))
      system("rm -r ".$f_path);
	else
      unlink($f_path);
	$count_del++;
  }
  
  echo("Deleted ".$count_del." files/folders from '".FOLDER_PATH."'.");
?>