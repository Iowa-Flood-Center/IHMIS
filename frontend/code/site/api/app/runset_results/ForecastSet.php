<?php

  namespace Results;
  
  use Results\MetaFile as MetaFile;
  
  class ForecastSet extends MetaFile{
	  
    const ROOT_ATTR = "forecast_matrix";            // must-have   
    const SUB_META_FOLDER_NAME = "cross_matrices";  // must-have
    const FILE_BASENAME = "Forecast_matrix";	
	
    const SUB_FILE_PATH = "/metafiles/cross_matrices/Forecast_matrix.json";
	
	// //////////////////// INTERFACE //////////////////// //
	
	/**
     * List all models from Runset
     */
    public static function all($runset_id){
	  return(self::get_base($runset_id));
    }
  
  }
  
?>
