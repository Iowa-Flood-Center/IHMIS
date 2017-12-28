<?php

use Results\ModelResult as ModelResult;

function process_delete_request($app, $runset_id, $model_id){
  error_reporting(E_ALL);
  ini_set('display_errors', 1);
  
  ModelResult::setApp($app);
  ModelResult::delete($model_id, $runset_id);
  
  echo(json_encode(array("error" => "Function being implemented.")));
  
  // echo(json_encode(array("error" => "Function not implemented yet.")));
}

?>