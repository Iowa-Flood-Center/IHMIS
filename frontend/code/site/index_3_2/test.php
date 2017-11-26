<?php
  require '../common/libs/settings.php';
  
  echo(getcwd()."<br />");
  
  $slash = DIRECTORY_SEPARATOR;
  $pattern = "#frontend".$slash."code".$slash.".*$#";
  //$pattern = "#frontend/code/#";
  echo($pattern."<br />");
  $replace = "frontend".$slash."conf".$slash;
  //$replace = "aa";
  $file_path = preg_replace($pattern, $replace, getcwd());
  echo($file_path);
  echo("<br />.");
  echo(Settings::get_raw_folder_path());
  echo("<br />!");
  $log_file = Settings::get_log_file_path(["ulaula", "dela"]);
  Settings::write_log("trigo", $log_file);
  Settings::write_log_ln("bacalhau", $log_file);
  Settings::write_log_ln("do alho poro", $log_file);
  echo("<br />X");
?>