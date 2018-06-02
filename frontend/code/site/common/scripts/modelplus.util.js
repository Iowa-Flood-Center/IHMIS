var modelplus = modelplus || {};

(function () {
  "use strict";
  
  modelplus.util = modelplus.util || {};
  var mpu = modelplus.util;
  
  /**
   * Converts a date string in 'MM/DD/YYYY' format to timestamp
   * RETURN: Integer
   */
  mpu.datestr_to_timestamp = function(date_str){
    if (date_str.length != 10)
      return(null);
    var mid_year = date_str.substring(6,10);
    var mid_month = parseInt(date_str.substring(0,2)) - 1;
    var mid_day = date_str.substring(3,5);
    return (mpu.get_timestamp(mid_day, mid_month, mid_year));
  };

  /**
   * 
   * RETURN: String
   */
  mpu.timestamp_to_datestr = function(timestamp){
    var d = new Date(timestamp * 1000);
    return(mpu.date_to_datestr(d));
  };

  /**
   * Converts a epoch timestamp (in seconds) to string date-time format 'MM/DD/YY, HH:mm'
   * RETURN: String
   */
  mpu.timestamp_to_datetimestr = function(timestamp){
    var d = new Date(timestamp * 1000);
    return(mpu.date_to_datetimestr(d));
  };

  /**
   * Converts a Date object into a date-time string in the format 'MM/DD/YY, HH:mm'
   * RETURN:
   */
  mpu.date_to_datetimestr = function(d){
    var return_txt;
    return_txt = mpu.two_digits(d.getMonth()+1) + '/';
    return_txt += mpu.two_digits(d.getDate()) + '/';
    return_txt += d.getFullYear() + ', ';
    return_txt += mpu.two_digits(d.getHours()) + ':';
    return_txt += mpu.two_digits(d.getMinutes());
    return(return_txt);
  };

  /**
   *
   * RETURN: String
   */
  mpu.date_to_datestr = function(d){
    var return_txt;
    return_txt = mpu.two_digits(d.getMonth()+1) + '/';
    return_txt += mpu.two_digits(d.getDate()) + '/';
    return_txt += d.getFullYear();
    return(return_txt);
  };

  /**
   * Converts a date into timestamp. Assumes 00:00 Iowa time.
   * RETURN: Integer. Timestasmp in seconds.
   */
  mpu.get_timestamp = function(day, month, year){
    // TODO - check if this function is summer-time safe
    var date_obj = new Date(Date.UTC(year, month, day, 0, 0, 0));
    date_obj.setUTCHours(date_obj.getUTCHours() + 5);
    return (date_obj.getTime() / 1000);
  };
  
  /**
   * 
   * RETURN: Boolean
   */
  mpu.is_runset_visible_public = function(sc_runset_obj){
    if(sc_runset_obj == null) return(false);
    if(!sc_runset_obj.hasOwnProperty('show_main')) return(false);
    var show_main = sc_runset_obj['show_main'];
    if((Array.isArray(show_main))&&(show_main.indexOf('main') > -1))
      return(true);
    if ((typeof show_main === 'string')||(show_main instanceof String))
      return(true);
    return(false);
  };

  /**
   * Converts a numeric value into a String of two-digits size
   * a_number: 
   * RETURN: String.
   */
  mpu.two_digits = function(a_number){
    var i = Math.round(a_number);
    return(i > 9 ? "" + i: "0" + i);
  };
  
})();