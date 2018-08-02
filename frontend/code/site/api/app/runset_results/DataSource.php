<?php
  namespace Results;
  
  class DataSource{

    public static function isSourceLocalFilePath($app){
      return(property_exists($app->fss, "runsets_result_folder_path"));
	}

	public static function isSourceRemoteFilePath($app){
      return(property_exists($app->rfs, "runsets_result_url"));
	}
  }
?>