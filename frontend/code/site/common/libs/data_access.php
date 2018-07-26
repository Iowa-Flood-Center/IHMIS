<?php
  error_reporting(E_ALL | E_STRICT );
  ini_set("display_errors", 1);

  require_once("settings.php");
  
  class DataAccess{
    private static $data_server_url = NULL;
    const DATA_FILES_FOLDER = "files";
    const META_FILES_FOLDER = "metafiles";
    const RUNSETS_FOLDER = "runsets_tmp";

    //
    // 
    // $file_direction: can be both a relative file path or an array of directories/filename.
    // RETURN:
    public static function get_datafile_content($file_direction, 
                                                $runset_id){
      // build target data file URL and perform HTTP request
      $base_url = DataAccess::_get_base_url($runset_id);
      if(is_null($base_url)) return(NULL);
      $base_url .= DataAccess::DATA_FILES_FOLDER."/";
      $fi_url = DataAccess::_build_url($base_url, $file_direction);
      return(DataAccess::_http_request($fi_url));
    }
    
    //
    // $file_direction: 
    // RETURN: Boolean.
    public static function check_datafile_exists($file_direction, 
                                                 $runset_id){
      $file_content = DataAccess::get_datafile_content($file_direction,
                                                       $runset_id);
      return(($file_content == "" ? FALSE : TRUE));
    }

    //
    // $folder_direction:
    // $runset_id: 
    // $file_ext:
    // RETURN:
    public static function list_datafolder_content($folder_direction, 
                                                   $runset_id,
                                                   $file_ext,
                                                   $echo_url=FALSE){
      // build target data folder URL and perform HTTP request
      $base_url = DataAccess::_get_base_url($runset_id);
      if(is_null($base_url)) return(NULL);
      $base_url .= DataAccess::DATA_FILES_FOLDER."/";
      $fd_url = DataAccess::_build_url($base_url, $folder_direction);
      if($echo_url) echo($fd_url."<br />");
      $fd_html = DataAccess::_http_request($fd_url);
      return(DataAccess::_get_file_list($fd_html, $file_ext));
    }
    
    //
    // 
    // $file_direction: can be both a relative file path or an array of directories/filename.
    // RETURN:
    //
    public static function get_metafile_content($file_direction, 
                                                $runset_id){
      // build target data file URL and perform HTTP request
      $base_url = DataAccess::_get_base_url($runset_id);
      if(is_null($base_url)) return(NULL);
      $base_url .= DataAccess::META_FILES_FOLDER."/";
      $fi_url = DataAccess::_build_url($base_url, $file_direction);
      return(DataAccess::_http_request($fi_url));
    }

    //
    // $file_direction: 
    // RETURN: Boolean.
    public static function check_metafile_exists($file_direction, 
                                                 $runset_id){
      $file_content = DataAccess::get_metafile_content($file_direction,
                                                       $runset_id);
      return(($file_content == "" ? FALSE : TRUE));
    }

    //
    // $folder_direction:
    // $runset_id: 
    // $file_ext:
    // RETURN:
    public static function list_metafolder_content($folder_direction, 
                                                   $runset_id,
                                                   $file_ext){
      // build target data folder URL and perform HTTP request
      $base_url = DataAccess::_get_base_url($runset_id);
      if(is_null($base_url)) return(NULL);
      $base_url .= DataAccess::META_FILES_FOLDER."/";
      $fd_url = DataAccess::_build_url($base_url, $folder_direction);
      $fd_html = DataAccess::_http_request($fd_url);
      return(DataAccess::_get_file_list($fd_html, $file_ext));
    }
    
    // ////////////////////////// PRIV ////////////////////////////// //

    //
    // $runset_id:
    // RETURN:
    private static function _get_base_url($runset_id){
      if(!DataAccess::_load_settings_if_needed()) return(NULL);
      $base_url = DataAccess::$data_server_url;
      $base_url .= DataAccess::RUNSETS_FOLDER."/";
      $base_url .= $runset_id."/";
      return($base_url);
    }
    
    // Changes content of $data_server_url parameter if it is null
    // RETURN: Boolean. TRUE if able to load, FALSE otherwise
    private static function _load_settings_if_needed(){
      if(!is_null(DataAccess::$data_server_url)) return(true);
      $url = Settings::get_property("raw_data_url");
      if(is_null($url)) return(false);
      DataAccess::$data_server_url = $url;
      return(true);
    }
    
    // 
    // $base_url: 
    // $file_direction: 
    // RETURN: 
    private static function _build_url($base_url, $file_direction){
      if(is_string($file_direction)){
        return($base_url.$file_direction);
      }elseif(is_array($file_direction)){
        return ($base_url.implode($file_direction, "/"));
      } else {
        return(NULL);
      }
    }
    
    // Searches for all files with an extension in an HTML response.
    // Basically it text mines the response, assuming an Apache server.
    // $html_response: 
    // $file_ext: 
    // RETURN: 
    private static function _get_file_list($html_response, $file_ext){
      $regex = '/href=".*'.$file_ext.'"/';
      preg_match_all($regex, $html_response, $matches);
      $matches = $matches[0];
      for($i = 0; $i < count($matches); $i++){
        $matches[$i] = str_replace('href="', '', $matches[$i]);
        $matches[$i] = str_replace('"', '', $matches[$i]);
        if(DataAccess::_endsWith($matches[$i], '/')){
		  $matches[$i] = substr($matches[$i], 0, -1);
		}
		$matches[$i] = explode('/', $matches[$i]);
        $matches[$i] = end($matches[$i]);
      }
      // if listing directories, remove the first one (parent dir)
      if($file_ext == "\/"){
        $matches = array_splice($matches, 1, count($matches)-1);
      }
      return($matches);
    }
    
    // Just perform an HTTPS REQUEST ignoring the lack of certificate
    // $url: String. Final URL of the file to be read
    // RETURN: String with the file content if able to access it or NULL otherwise
    private static function _http_request($url){
      $context = array(
        "ssl"=>array(
          "verify_peer"=>false,
          "verify_peer_name"=>false,
        ),
      );  
      $context = stream_context_create($context);
      $content = @file_get_contents($url, false, $context);
      return($content);
    }
    
    // return tru if $str ends with $sub
    private static function _endsWith($str, $sub) {
      return(substr( $str, strlen( $str ) - strlen( $sub ) ) == $sub);
    }
  }
  
  // TODO: remove this test
  // DATA:
  // $file1 = "repres_displayed/mdl1/hydrographsd_usgsgagesdischarge/1527220800_79118.json";
  // $file2 = "repres_displayed/mdl1/hydrographsd_usgsgagesdischarge/1527220800_791181.json";
  // echo("Files existance: ".DataAccess::check_datafile_exists($file1, "rset000122")." and ".DataAccess::check_datafile_exists($file2, "rset000122")."<br />");
  
  /*
  $file_content = DataAccess::get_datafile_content($file1, "rset000122");
  echo($file_content);
  echo("<br />...Is null? ".is_null($file_content)."<br />");
  echo("<br />...<br />");
  print_r(DataAccess::list_datafolder_content("repres_displayed/mdl1/podwacih", "rset000122", ".png"));
  */
  
  // META:
  /*
  echo(DataAccess::get_metafile_content("sc_menu/Menu.json", "realtime"));
  echo("<br />---<br />");
  print_r(DataAccess::list_metafolder_content("sc_modelcombinations", "realtime", ".json"));
  */
?>
