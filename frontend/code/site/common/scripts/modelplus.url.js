// TODO - learn headers for globals...

/**
 * The ModelPlus variables and functions are being moved to this namespace to avoid clutering the global namespace.
 * @namespace
 */
var modelplus = modelplus || {};

(function () {
  "use strict";
  
  modelplus.url = modelplus.url || {};
  var mpu = modelplus.url;
  
  // function that reads server side files
  mpu.read_server_file = function(file_path){
    var result = null;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", "../../" + file_path, false);
    xmlhttp.send();
    if (xmlhttp.status==200) {
      result = xmlhttp.responseText;
    }
    return result;
  }
  
  // read frontend URL settings
  mpu.settings = mpu.read_server_file("");
  
  // TODO - load the following lines from a config file somehow
  mpu.base_frontend_deploy = 'http://ifis.iowafloodcenter.org/ifis/sc/modelplus/';
  mpu.base_runsets = 'https://s-iihr54.iihr.uiowa.edu/ihmis_data/runsets/';
  mpu.base_api = mpu.base_frontend_sandbox;
  mpu.base_api = 'http://s-iihr50.iihr.uiowa.edu/ifis/sc/ihmis_dev/';
  mpu.base_proxy = 
  
  // define root URL source
  mpu.base_url = function(){
    console.log("From base_url()");
    var url;
	url = document.documentURI;
    if (url.indexOf('ihmis') != -1) return(url);
	url = document.referrer;
	if(url.indexOf('ihmis') != -1) return(url);
	console.log('Not found root URL.');
	return(null)
  }
  mpu.base_url = mpu.base_url();
  
  // define basic URL address
  mpu.base_frontend = function() {
    var fd;
    if(window.location.href.indexOf('s-iihr50') != -1){
      mpu.is_deploy = false;
	  var uri = mpu.base_url;
	  if (uri.indexOf('/ihmis_dev/') != -1){
        fd = "index/";
        console.log("Under devs: "+ uri);
      } else {
		fd = "frontend/";
		console.log("Under dist: "+uri);
      }
	  if (uri.indexOf(fd) != -1){
        console.log("Cleaned");
	    return(uri.substring(0, uri.indexOf(fd)));
      } else {
		console.log("Not cleaned");
        return(uri);
	  }
    } else {
      mpu.is_deploy = true;
      return(mpu.base_frontend_deploy); 
	}};
  mpu.base_frontend = mpu.base_frontend();
  mpu.is_sandbox = !mpu.is_deploy;
  
  console.log("Under base_frontend: "+mpu.base_frontend);
  mpu.base_frontend_index  = mpu.base_frontend + 'index/';
  mpu.base_frontend_viewer = mpu.base_frontend + 'viewer/';
  mpu.base_frontend_common = mpu.base_frontend + 'common/';
  mpu.api                  = mpu.base_api + 'api/public/';     // TODO - remove it (?)
  mpu.api_old_v            = mpu.base_api + 'viewer/';         // TODO - remove it (!)
  mpu.proxy                = mpu.base_frontend_common + 'libs/proxy.php?url=';
  
  mpu.base_frontend_webservices = mpu.api_old_v;                   // TODO - remove it
  
  
  
  // read server side files
  var text_content = mpu.read_server_file("a_text.txt");
  console.log("Read '"+text_content+"'.");
  // mpu.base_runsets = 
  
  console.log("Using url.old_v...");
})();
