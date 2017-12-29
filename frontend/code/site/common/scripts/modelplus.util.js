var modelplus = modelplus || {};

(function () {
  "use strict";
  
  modelplus.util = modelplus.util || {};
  
  /**
   * Converts a date string in 'MM/DD/YYYY' format to timestamp
   * RETURN: Integer
   */
  modelplus.util.datestr_to_timestamp = function(date_str){
    if (date_str.length != 10)
      return(null);
    var mid_year = date_str.substring(6,10);
    var mid_month = parseInt(date_str.substring(0,2)) - 1;
    var mid_day = date_str.substring(3,5);
    return (modelplus.util.get_timestamp(mid_day, mid_month, mid_year));
  }
  
  /**
   * Converts a date into timestamp. Assumes 00:00 Iowa time.
   * RETURN: Integer. Timestasmp in seconds.
   */
  modelplus.util.get_timestamp = function(day, month, year){
    // TODO - check if this function is summer-time safe
    var date_obj = new Date(Date.UTC(year, month, day, 0, 0, 0));
    date_obj.setUTCHours(date_obj.getUTCHours() + 5);
    return (date_obj.getTime() / 1000);
  }
  
  /**
   * 
   * RETURN: Boolean
   */
  modelplus.util.is_runset_visible_public = function(sc_runset_obj){
    if(sc_runset_obj == null) return(false);
    if(!sc_runset_obj.hasOwnProperty('show_main')) return(false);
    var show_main = sc_runset_obj['show_main'];
    if((Array.isArray(show_main))&&(show_main.indexOf('main') > -1))
      return(true);
    if ((typeof show_main === 'string')||(show_main instanceof String))
      return(true);
    return(false);
  }
  
})();