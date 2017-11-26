// TODO - learn headers for globals...

/**
 * The ModelPlus variables and functions are being moved to this namespace to avoid clutering the global namespace.
 * @namespace
 */
var modelplus = modelplus || {};

(function () {
  "use strict";
  
  modelplus.url = modelplus.url || {};
  
  modelplus.url.base_frontend_sandbox = 'http://s-iihr50.iihr.uiowa.edu/ifis/sc/test1/ihmis/dev/frontend/code/site/';
  modelplus.url.base_frontend_deploy = 'http://ifis.iowafloodcenter.org/ifis/sc/modelplus/';
  
  // define basic URL address
  modelplus.url.base_frontend = () => {
    if(window.location.href.indexOf('s-iihr50') != -1){
      modelplus.url.is_deploy = false;
      return(modelplus.url.base_frontend_sandbox);
    } else {
      modelplus.url.is_deploy = true;
      return(modelplus.url.base_frontend_deploy); 
	}};
  modelplus.url.base_frontend = modelplus.url.base_frontend();
  modelplus.url.is_sandbox = !modelplus.url.is_deploy;
  
  modelplus.url.base_frontend_index  = modelplus.url.base_frontend + 'index_3_2/';
  modelplus.url.base_frontend_viewer = modelplus.url.base_frontend + 'viewer_3_2/';
  modelplus.url.base_frontend_common = modelplus.url.base_frontend + 'common/';
  modelplus.url.api = modelplus.url.base_frontend + 'api_3_2/public/';
  
  modelplus.url.proxy = modelplus.url.base_frontend_common + 'libs/proxy.php?url=';
})();