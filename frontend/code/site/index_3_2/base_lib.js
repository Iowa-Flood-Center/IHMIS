/**************************************************************************************/
/**************************************** DEFS ****************************************/
/**************************************************************************************/

GLB_lib = function(){};

GLB_lib.prototype.api_url = modelplus.url.api;
GLB_lib.prototype.base_url = modelplus.url.base_frontend_index;
GLB_lib.prototype.base_viewer_url = modelplus.url.base_frontend_viewer;

GLB_lib.prototype.base_requester_url = GLB_lib.prototype.base_url + "requester/";
GLB_lib.prototype.header_url = GLB_lib.prototype.base_url + "template_header.html";
GLB_lib.prototype.footer_url = GLB_lib.prototype.base_url + "template_footer.html";
GLB_lib.prototype.img_icon_url = GLB_lib.prototype.base_url + "imgs/icons/";

/**************************************************************************************/
/*********************************** HEADER/FOOTER ************************************/
/**************************************************************************************/

$(document).ready(function() {
	"use strict";

	// change header
	$.get(GLB_lib.prototype.header_url, function(html_content) {
		$("#header").html(html_content);
	});

	// change footer
	$.get(GLB_lib.prototype.footer_url, function(html_content) {
		var page_file;
		$("#footer").html(html_content);
		
		// TODO - use constants
		$("#uiowa-logo").attr('src', GLB_lib.prototype.img_icon_url + 'uiowa.png');
		$("#iihr-logo").attr('src', GLB_lib.prototype.img_icon_url + 'iihr.png');
		$("#ifc-logo").attr('src', GLB_lib.prototype.img_icon_url + 'ifc2.jpg');
	});
});

/**************************************************************************************/
/**************************************** FUNCS ****************************************/
/**************************************************************************************/

/**
 * Load a script dynamically (copied from internet)
 * url - Imported script url
 * callback - Function o be called on callback
 * RETURN - None
 */
function loadScript(url, callback){

    var script = document.createElement("script")
    script.type = "text/javascript";

    if (script.readyState){  //IE
        script.onreadystatechange = function(){
            if (script.readyState == "loaded" ||
                    script.readyState == "complete"){
                script.onreadystatechange = null;
                callback();
            }
        };
    } else {  //Others
        script.onload = function(){
            callback();
        };
    }

    script.src = url;
    document.getElementsByTagName("head")[0].appendChild(script);
}
