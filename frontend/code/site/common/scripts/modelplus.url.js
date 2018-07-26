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
  
  // TODO - load the following lines from a config file somehow
  mpu.base_frontend_sandbox = 'http://s-iihr50.iihr.uiowa.edu/ifis/sc/test1/ihmis/dev/frontend/code/site/';
  mpu.base_frontend_distrib = 'http://s-iihr50.iihr.uiowa.edu/ifis/sc/test1/ihmis/dst/';
  mpu.base_frontend_deploy = 'http://ifis.iowafloodcenter.org/ifis/sc/modelplus/';
  
  mpu.base_runsets = 'http://s-iihr50.iihr.uiowa.edu/andre/model_3_1/';  // it was modelplus.url.base_realtime_folder
  mpu.base_api = mpu.base_frontend_sandbox;
  
  // define basic URL address
  mpu.base_frontend = function() {
    if(window.location.href.indexOf('s-iihr50') != -1){
      mpu.is_deploy = false;
	  if (document.referrer.indexOf('/dev/') != -1){
        console.log("Under dev: "+document.referrer);
        return(mpu.base_frontend_sandbox);
      } else {
		console.log("Under dist: "+document.referrer);
        return(mpu.base_frontend_distrib);
      }
    } else {
      mpu.is_deploy = true;
      return(mpu.base_frontend_deploy); 
	}};
  mpu.base_frontend = mpu.base_frontend();
  mpu.is_sandbox = !mpu.is_deploy;
  
  mpu.base_frontend_index  = mpu.base_frontend + 'index_3_2/';
  mpu.base_frontend_viewer = mpu.base_frontend + 'viewer_3_2/';
  mpu.base_frontend_common = mpu.base_frontend + 'common/';
  mpu.api                  = mpu.base_api + 'api_3_2/public/';     // TODO - remove it (?)
  mpu.api_old_v            = mpu.base_api + 'viewer_3_2/';         // TODO - remove it (!)
  mpu.proxy                = mpu.base_frontend_common + 'libs/proxy.php?url=';
  
  mpu.base_frontend_webservices = mpu.api_old_v;                   // TODO - remove it
  
  // function that reads server side files
  mpu.read_server_file = function(file_path){
    var result = null;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", "../sc/test1/ihmis/dev/frontend/" + file_path, false);
    xmlhttp.send();
    if (xmlhttp.status==200) {
      result = xmlhttp.responseText;
    }
    return result;
  }
  
  // read server side files
  var text_content = mpu.read_server_file("a_text.txt");
  console.log("Read '"+text_content+"'.");
  // mpu.base_runsets = 
  
  console.log("Using url.old_v...");
})();