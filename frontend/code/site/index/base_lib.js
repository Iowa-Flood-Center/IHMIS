/**************************************************************************************/
/**************************************** DEFS ****************************************/
/**************************************************************************************/

GLB_lib = function(){};

var glb = GLB_lib.prototype;

glb.api_url = modelplus.url.api;
glb.base_url = modelplus.url.base_frontend_index;
glb.base_viewer_url = modelplus.url.base_frontend_viewer;

glb.base_requester_url = glb.base_url + "requester/";
glb.header_url = glb.base_url + "template_header.html";
glb.footer_url = glb.base_url + "template_footer.html";
glb.img_icon_url = glb.base_url + "imgs/icons/";

console.log("Base URL: " + glb.base_url);
console.log("Header URL: " + glb.header_url);

/**************************************************************************************/
/*********************************** HEADER/FOOTER ************************************/
/**************************************************************************************/

$(document).ready(function() {
	"use strict";

	// change header
	$.get(glb.header_url, function(html_content) {
		$("#header").html(html_content);
	});

	// change footer
	$.get(glb.footer_url, function(html_content) {
		var page_file;
		$("#footer").html(html_content);
		
		// TODO - use constants
		$("#uiowa-logo").attr('src', glb.img_icon_url + 'uiowa.png');
		$("#iihr-logo").attr('src', glb.img_icon_url + 'iihr.png');
		$("#ifc-logo").attr('src', glb.img_icon_url + 'ifc2.jpg');
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
