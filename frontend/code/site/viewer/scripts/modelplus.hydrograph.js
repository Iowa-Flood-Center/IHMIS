// TODO - learn headers for globals...

/**
 * The ModelPlus variables and functions are being moved to this namespace to avoid clutering the global namespace.
 * @namespace
 */
var modelplus = modelplus || {};

(function () {
  "use strict";
  
  modelplus.hydrograph = modelplus.hydrograph || {};
  
  /**
   * Create modal div.
   */
  modelplus.hydrograph.create = function(){
    var div_modal, div_modal_ctt;
	
	// create main div
	div_modal = document.getElementById(modelplus.ids.MODAL_HYDROGRAPH);
	div_modal.style.display = "block";
	
	// create content div
	div_modal_ctt = $('#' + modelplus.ids.MODAL_HYDROGRAPH_CONTENT);
    div_modal_ctt.css("background-color", 
	                  modelplus.MODAL_HYDROGRAPH_BGCOLOR);
    div_modal_ctt.height(modelplus.MODAL_HYDROGRAPH_CONTENT_HEIGHT);
    div_modal_ctt.width(modelplus.MODAL_HYDROGRAPH_WIDTH);
	
	// register 'ESC' as closing key
	modelplus.keyCodes[modelplus.MODAL_HYDROGRAPH_CLOSE_BUTTON] = function(){
      modelplus.hydrograph.close();
    };
  }
  
  /**
   * Create modal div. TEMP
   */
  modelplus.hydrograph.create_tmp = function(){
    var div_modal, div_modal_ctt;
	
	// make background dark
	$('#' + modelplus.ids.BACKGROUND_DARK).show();
	
	// create main div
	div_modal = $('#' + modelplus.ids.MODAL_HYDROGRAPH_IFISBASED);
	div_modal.show();
	
	// create content div
    div_modal.css("background-color", 
	                  modelplus.MODAL_HYDROGRAPH_BGCOLOR);
    div_modal.height(modelplus.MODAL_HYDROGRAPH_CONTENT_HEIGHT);
    div_modal.width(modelplus.MODAL_HYDROGRAPH_WIDTH);
	
	// register 'ESC' as closing key
	modelplus.keyCodes[modelplus.MODAL_HYDROGRAPH_CLOSE_BUTTON] = function(){
      modelplus.hydrograph.close();
    };
  }
  
  /**
   * Add headers to the modal div
   */
  modelplus.hydrograph.addHeader = function(options){
	var modal_ctt_div, header_div, header_span_close, header_span_rawdata;
  
    // basic check - modal div must exist
	if((!options) || (!options.div_id)){
	    modal_ctt_div = $('#' + modelplus.ids.MODAL_HYDROGRAPH_CONTENT);
	} else {
		modal_ctt_div = $('#' + options.div_id);
	}
    
	if(!modal_ctt_div.length) {return;}

	if((!options) || (!options.position) || (options.position == 'static')){
		header_div = $("<div style='background-color:"+modelplus.MODAL_HYDROGRAPH_BGCOLOR+"; \
									display:block; \
									border-top:0px; \
									adding-top:0px'></div>");
	} else if (options.position == 'absolute') {
		header_div = $("<div style='background-color:"+modelplus.MODAL_HYDROGRAPH_BGCOLOR+"; \
									display:block; \
									position:relative; \
									right: 0px; \
									top: 0px; \
									z-index: 15; \
									border-top:0px; \
									border-right:0px; \
									adding-top:0px'></div>");
	}

    // add 'Close' button
    // header_span_close = $("<span>Close</span>&nbsp;");
	header_span_close = $("<button class='btn-close' ></button>");
    header_span_close.attr("id", modelplus.ids.MODAL_CLOSE_SPAN);
	// header_span_close.attr("title", "Close");
    header_span_close.click(modelplus.hydrograph.close);
    header_div.append(header_span_close);

    // add optional buttons
    if(options){
		
      // add raw data
      if("raw_data_function" in options){
		header_span_rawdata = $("<span>Raw Data</span>&nbsp;&nbsp;");
		header_span_rawdata.attr("id", modelplus.ids.MODAL_RAWDATA_SPAN);
		header_span_rawdata.click(function(){
          if("raw_data_argument" in options){
            options["raw_data_function"](options["raw_data_argument"]);
          } else {
            options["raw_data_function"]();
          }
        });
		header_div.append(header_span_rawdata);
	  }
	}
	
    modal_ctt_div.prepend(header_div);
	modal_ctt_div.height(modelplus.MODAL_HYDROGRAPH_HEIGHT);
  }
  
  /**
   * 'On close' function
   */
  modelplus.hydrograph.close = function(){
    $("#"+modelplus.ids.MODAL_HYDROGRAPH).hide();
	$("#"+modelplus.ids.MODAL_HYDROGRAPH_CONTENT).html("<p>&nbsp;</p>");
    delete modelplus.keyCodes[modelplus.MODAL_HYDROGRAPH_CLOSE_BUTTON];
	
	// 
	$('#' + modelplus.ids.MODAL_HYDROGRAPH_IFISBASED).html("");
	$('#' + modelplus.ids.MODAL_HYDROGRAPH_IFISBASED).hide();
	
	// hide dark background
	$('#' + modelplus.ids.BACKGROUND_DARK).hide();
  }
  
})();
