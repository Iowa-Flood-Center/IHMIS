// TODO - learn headers for globals...

/**
 * The ModelPlus variables and functions are being moved to this namespace to avoid clutering the global namespace.
 * @namespace
 */
var modelplus = modelplus || {};

(function () {
  "use strict";
  
  modelplus.url = modelplus.url || {};
  
  modelplus.url.base_frontend_sandbox = 'http://s-iihr50.iihr.uiowa.edu/ifis/sc/test1/modelplus_3_1_git_develop/frontend/';
  modelplus.url.base_frontend_deploy = 'http://ifis.iowafloodcenter.org/ifis/sc/modelplus/';
  
  modelplus.url.base_frontend = () => {
    if(window.location.href.indexOf('s-iihr50') != -1)
      return(modelplus.url.base_frontend_sandbox);
    else
      return(modelplus.url.base_frontend_deploy); };
  modelplus.url.base_frontend = modelplus.url.base_frontend();                          // TODO - delete and use only the one on common folder
  modelplus.url.api = modelplus.url.base_frontend_sandbox + 'api_3_2/public/';          // TODO - delete and use only the one on common folder
  modelplus.url.base_webservice = modelplus.url.base_frontend_sandbox + 'viewer_3_1/';  // TODO - move to API
  modelplus.url.base_frontend_index = modelplus.url.base_frontend + 'index_3_1/';
  modelplus.url.base_frontend_viewer = modelplus.url.base_frontend + 'viewer_3_1/';
  
  modelplus.url.proxy = modelplus.url.base_frontend_viewer + 'the_proxy.php?url=';      // TODO - send to common folder
  
  modelplus.url.is_landing_page = () => {
	var page_file = location.pathname.split("/").slice(-1);
    return((page_file == "") || (page_file == "index.php"));
  };
  
})();