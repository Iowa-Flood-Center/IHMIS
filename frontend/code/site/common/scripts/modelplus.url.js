// TODO - learn headers for globals...

/**
 * The ModelPlus variables and functions are being moved to this namespace to avoid clutering the global namespace.
 * @namespace
 */
var modelplus = modelplus || {};

(function () {
  "use strict";
  
  modelplus.url = modelplus.url || {};
  
  // TODO - load the following lines from a config file somehow
  modelplus.url.base_frontend_sandbox = 'http://s-iihr50.iihr.uiowa.edu/ifis/sc/test1/ihmis/dev/frontend/code/site/';
  modelplus.url.base_frontend_distrib = 'http://s-iihr50.iihr.uiowa.edu/ifis/sc/test1/ihmis/dst/';
  modelplus.url.base_frontend_deploy = 'http://ifis.iowafloodcenter.org/ifis/sc/modelplus/';
  
  modelplus.url.base_realtime_folder = 'http://s-iihr50.iihr.uiowa.edu/andre/model_3_1/';
  modelplus.url.base_api = modelplus.url.base_frontend_sandbox;
  
  // define basic URL address
  modelplus.url.base_frontend = function() {
    if(window.location.href.indexOf('s-iihr50') != -1){
      modelplus.url.is_deploy = false;
	  if (document.referrer.indexOf('/dev/') != -1){
        console.log("Under dev: "+document.referrer);
        return(modelplus.url.base_frontend_sandbox);
      } else {
		console.log("Under dist: "+document.referrer);
        return(modelplus.url.base_frontend_distrib);
      }
    } else {
      modelplus.url.is_deploy = true;
      return(modelplus.url.base_frontend_deploy); 
	}};
  modelplus.url.base_frontend = modelplus.url.base_frontend();
  modelplus.url.is_sandbox = !modelplus.url.is_deploy;
  
  modelplus.url.base_frontend_index  = modelplus.url.base_frontend + 'index_3_2/';
  modelplus.url.base_frontend_viewer = modelplus.url.base_frontend + 'viewer_3_2/';
  modelplus.url.base_frontend_common = modelplus.url.base_frontend + 'common/';
  modelplus.url.api                  = modelplus.url.base_api + 'api_3_2/public/';     // TODO - remove it (?)
  modelplus.url.api_old_v            = modelplus.url.base_api + 'viewer_3_2/';         // TODO - remove it (!)
  modelplus.url.proxy                = modelplus.url.base_frontend_common + 'libs/proxy.php?url=';
  
  modelplus.url.base_frontend_webservices = modelplus.url.api_old_v;                   // TODO - remove it
  
  console.log("Using url.old_v...");
})();