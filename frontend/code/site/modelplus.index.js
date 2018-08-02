// ATTENTION: depends on:
// - JQuery libray
// -
// -

var modelplus = modelplus || {};

(function () {
  "use strict";
  
  modelplus.index = modelplus.index || {};
  
  var mpi = modelplus.index;
  var mput = modelplus.util;
  var mpa = modelplus.api;
  
  mpi.ref0_timestamp = null;
  
  //
  // args: should be a dictionary with
  //   {
  //     dom_img_id: 
  //     dom_label_id: 
  //     sc_model_id: 
  //     sc_runset_id: 
  //     sc_result_id: 
  //     sc_result_title:
  //   }
  // RETURN: None. Changes performed in the interface.
  mpi.update_landing_image = function(args){
	

    // 1: get current ref 0 time
    mpa.get_timestamp_ref0(args.sc_runset_id,
                           args.sc_model_id,
                           args.sc_result_id)
      .then(function(data){
        mpi.ref0_timestamp = data[0];
        var delta_t = Math.floor(Date.now() / 1000) - mpi.ref0_timestamp;
        
        // 1.5: basic check
        var limit_older = 3 * 24 * 60 * 60; // ignore if images is older than 3 days
		var img_url, label_txt;
		var dom_img = $('#intro_map_view');
		var dom_span = $('#intro_date_view');
        if (delta_t <= limit_older){
          // 2: 'general case' image
          mpa.get_result_url(args.sc_runset_id,
                             args.sc_model_id,
                             args.sc_result_id,
                             0)
            .then(mpi.update_map_image);
        } else {
          // 2: 'general case' image
		  $('#intro_map_background').css('display', 'none');
		  img_url = 'index/imgs/launchviewer.png';
		  label_txt = "";
		  dom_img.css("border-width", "0px");
		  dom_img.css("top", "0px");
          dom_img.attr('src', img_url);
          dom_span.html(label_txt);
        }
    });
  };
  
  // 
  // data:
  mpi.update_map_image = function(data){
    var prev_timestamp = mpi.ref0_timestamp - (24*60*60);
    var label_txt = "Activity on " + mput.timestamp_to_datestr(prev_timestamp);
	var dom_img = $('#intro_map_view');
	var dom_span = $('#intro_date_view');
	var dom_loading_gif = $('#intro_map_loading');
    dom_img.attr('src', data['url']);
	dom_loading_gif.css('display', 'none');
	dom_img.css('display', 'block');
    dom_span.html(label_txt);
  }
  
})();