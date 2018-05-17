"use strict"

// This script assumes echarts 3 was loaded

// opens workspace
var richhydroforecast01;
richhydroforecast01 = richhydroforecast01 || {};
richhydroforecast01.chartDivId = null;
richhydroforecast01.sliderId = null;
richhydroforecast01.sliderSpanId = null;
richhydroforecast01.specifications = null;
richhydroforecast01.chartObj = null;
richhydroforecast01.stepSize = 60;  // a default value
richhydroforecast01.current_timestamp = 0;

/**
 *
 */
richhydroforecast01.init = function(div_id, slider_id, span_id, specs){
  richhydroforecast01.chartDivId = div_id;
  richhydroforecast01.sliderId = slider_id;
  richhydroforecast01.sliderSpanId = span_id;
  richhydroforecast01.specifications = JSON.parse(specs);
}

/**
 *
 */
richhydroforecast01.updateLeadTime = function(new_lead_time){
  var specs = richhydroforecast01.specifications;
  
  // call Ajax
  specs.metadata["lead_time"] = new_lead_time;
  // console.log("Only models: " + richhydroforecast01.only_models);
  richhydroforecast01.ajaxCall(new_lead_time, true, null, 
                               richhydroforecast01.updateLeadTime_callback, 
							   richhydroforecast01.only_models);
}

/**
 * Called to process ajax call on timeseries retrieval
 * 
 */
richhydroforecast01.updateLeadTime_callback = function(data){
  var cur_fore_id, cur_release_idx, cur_release_timestamp, cur_keys;
  var cur_timeseries_stg, cur_timeseries_dsc;
  var added_timesries = 0;
  var json_data = ($.type(data) === "string") ? JSON.parse(data) : data;
  for(var fore_idx = 0; fore_idx < json_data.forecasts.length; fore_idx++){
    cur_fore_id = json_data["forecasts"][fore_idx]["id"];
    cur_keys = Object.keys(json_data["forecasts"][fore_idx]["timeseries_stg"]);
	  
    // add retrieved data to 'global' variable '...specifications'
    for(var cur_release_idx = 0; cur_release_idx < cur_keys.length; cur_release_idx++){
      cur_release_timestamp = cur_keys[cur_release_idx];
      cur_timeseries_stg = json_data["forecasts"][fore_idx]["timeseries_stg"][cur_release_timestamp];
      cur_timeseries_dsc = json_data["forecasts"][fore_idx]["timeseries_dsc"][cur_release_timestamp];
	  richhydroforecast01.addTimesseries(cur_fore_id, cur_release_timestamp, cur_timeseries_stg, cur_timeseries_dsc);
	  
	  // debug
	  added_timesries += 1;
    }
  }
  
  // refresh graph	
  richhydroforecast01.refreshGraph();
}

/**
 * Changes 'richhydroforecast01.specifications' to hide models not listed in 'richhydroforecast01.only_models'
 */
/*
richhydroforecast01.cleanTimesseries = function(){
  richhydroforecast01.specifications["forecasts"].forEach(function(current_obj){
    if(richhydroforecast01.only_models.indexOf(current_obj["id"]) >= 0) continue;
	
	current_obj["timeseries_stg"] = [];
	current_obj["timeseries_dsc"] = [];
	array.splice(index, 1);
	
    console.log("Cleaned " + current_obj['name']); 
	
	// clean timeseries
	richhydroforecast01.
  });
}
*/

/**
 *
 *
 * timeseries : 
 */
richhydroforecast01.addTimesseries = function(model_id, release_timestamp, timeseries_stg, timeseries_dsc){
  richhydroforecast01.specifications["forecasts"].forEach(function(current_obj){
    if (current_obj["id"] != model_id) return;
    current_obj["timeseries_stg"][release_timestamp] = timeseries_stg;
	current_obj["timeseries_dsc"][release_timestamp] = timeseries_dsc;
  });
}

/**
 *
 */
richhydroforecast01.refreshGraph = function(){
  var specs = richhydroforecast01.specifications;
  var options = richhydroforecast01.buildGraphOptions(specs);
  // console.log("Legend: " + JSON.stringify(options));
  richhydroforecast01.chartObj.setOption(options);
}

/**
 * Main function.
 */
richhydroforecast01.buildHydroforecast = function(){
  var FUNC_NAME = "richhydroforecast01.buildHydroforecast()";  // dbg
  
  // check if it is ok to go
  var div_id = richhydroforecast01.chartDivId;
  var specs = richhydroforecast01.specifications;
  if (!richhydroforecast01.checkStart(div_id, specs)) return;
  
  // use configuration item and data specified to show chart
  (function (){
    var myChart = echarts.init(document.getElementById(div_id));
    richhydroforecast01.chartObj = myChart;
  }());
  
  // update slider width
  (function (){
    var cur_date = new Date(specs.metadata["current_time"] * 1000);
    var cur_size_norm = 1 + (cur_date.getHours() / 230);
	var ini_width = parseInt($("#"+richhydroforecast01.sliderId).css("width").replace("px", ""));
	var new_width = parseInt(ini_width * cur_size_norm) + "px";
    $("#"+richhydroforecast01.sliderId).css("width", new_width);
  }());
  
  // update slider values
  (function (){
    $("#"+richhydroforecast01.sliderId).attr("min", specs.metadata["min_x"]);
    $("#"+richhydroforecast01.sliderId).attr("max", specs.metadata["current_time"]);
    $("#"+richhydroforecast01.sliderId).val(specs.metadata["min_x"]);
  }());
  
  return;
}

/**
 * 
 * Returns a 'series element'
 */
richhydroforecast01.createThresholdSeries = function(the_id, the_name, y_value, the_color, specs){
  return ({
    id: the_id,
	name: the_name,
	type: "line",
	showSymbol: false,
    symbolSize: 0,
    smooth: true,
	lineStyle:{
      normal:{
        color: the_color
	  }
	},
    data: [[specs.metadata["min_x"], y_value], 
	       [specs.metadata["max_x"], y_value]],
    markPoint: {
      itemStyle: {
        normal: {
          color: 'transparent'
        }
      },
      label: {
        normal: {
          show: true,
          position: 'left',
          formatter: function(){ return(the_name) },
		  padding: [60, -17, 0, 0],
		  align: 'right',
          textStyle: {
            color: the_color,
            fontSize: 11
          }
        }
      },
      data: [{
        coord: [specs.metadata["max_x"], y_value]
      }]
    }
  });
}

/**
 * 
 * It assumes 'specs' is valid. Converts all Timestamps to Date
 */
richhydroforecast01.buildGraphOptions = function(specs){
  var options, series, leadIndex, legend_names, desc, area;
  var leadTimestampMin, leadTimestampMax;
  
  legend_names = [];
  series = [];
  leadIndex = (specs.metadata["current_time"] - specs.metadata["lead_time"]);
  leadIndex /= Math.round(richhydroforecast01.stepSize);
  
  leadTimestampMin = specs.metadata["lead_time"] - 3600;
  leadTimestampMax = specs.metadata["lead_time"];
  
  // define description and drainage area
  desc = specs.metadata["site_description"] == null ? "Hydrograph" : specs.metadata["site_description"];
  area = specs.metadata["drainage_area"] == null ? "Undefined" : specs.metadata["drainage_area"].toFixed(1) + " km^2";
  
  // add thresholds
  // TODO - make it flexible
  if(specs.metadata.thresholds_stg.action != null){
    series.push(richhydroforecast01.createThresholdSeries(
      "thresholds_act", "Action", specs.metadata.thresholds_stg.action, modelplus.COLOR_THRESHOLD_ACTION, specs));}
  if(specs.metadata.thresholds_stg.flood != null){
    series.push(richhydroforecast01.createThresholdSeries(
      "thresholds_fld", "Flood", specs.metadata.thresholds_stg.flood, modelplus.COLOR_THRESHOLD_FLOOD, specs));}
  if(specs.metadata.thresholds_stg.moderate != null){
    series.push(richhydroforecast01.createThresholdSeries(
      "thresholds_mod", "Moderate", specs.metadata.thresholds_stg.moderate, modelplus.COLOR_THRESHOLD_MODERATE, specs));}
  if(specs.metadata.thresholds_stg.major != null){
    series.push(richhydroforecast01.createThresholdSeries(
      "thresholds_maj", "Major", specs.metadata.thresholds_stg.major, modelplus.COLOR_THRESHOLD_MAJOR, specs));}
  
  // find closes previous forecast
  specs.forecasts.forEach(function(modelspec){
    var cur_releaseTimestamp, cur_timeseries;
    var closest_timestamp = null;
	var cur_dist = null;
    var closest_dist = null;
	var peak_stage, peak_index, peak_timestamp, lower_stage;
	var hide_model = false;
	
	// ignore graph that are not present in the 'richhydroforecast01.only_models' list
	if (richhydroforecast01.only_models != null){
      hide_model = (richhydroforecast01.only_models.indexOf(modelspec.id) == -1) ? true : false;
    } else {
      hide_model = false;
	}
	
    for(var index in modelspec.timeseries_stg){
		
      if(hide_model) break;
		
	  // find closest
      cur_releaseTimestamp = parseInt(index);
      if(cur_releaseTimestamp > specs.metadata["lead_time"]){
        continue;
	  }
	  cur_dist = specs.metadata["lead_time"] - cur_releaseTimestamp;
	  if((closest_dist == null)||(cur_dist < closest_dist)){
        closest_dist = cur_dist;
		closest_timestamp = cur_releaseTimestamp;
	  }
    }
	
	// remove all others
    for(var index in modelspec.timeseries_stg){

      cur_releaseTimestamp = parseInt(index);
      if(!hide_model){
        if (cur_releaseTimestamp == closest_timestamp){
          cur_timeseries = modelspec.timeseries_stg[index];
	    } else {
          cur_timeseries = null;
        }
      } else {
        cur_timeseries = null;
      }
	  
      // find and mark peak
	  if (cur_timeseries != null){
        peak_stage = null;
        peak_index = null;
	    peak_timestamp = null;
		lower_stage = null;
        for(var cur_idx = 0; cur_idx < cur_timeseries.length; cur_idx++){
          cur_timeseries[cur_idx][2] = 0;
          if((peak_stage == null)||(peak_stage < cur_timeseries[cur_idx][1])){
            peak_stage = cur_timeseries[cur_idx][1];
            peak_index = cur_idx;
		    peak_timestamp = cur_timeseries[cur_idx][0];
		  }
		  if((lower_stage == null)||(lower_stage > cur_timeseries[cur_idx][1])){
            lower_stage = cur_timeseries[cur_idx][1];
		  }
        }
        // console.log("Peak " +peak_stage+ " at " +peak_timestamp+ ", " + peak_index);
        if(peak_index != null){ 
		  cur_timeseries[peak_index][2] = 20; 
		  if(peak_stage > specs.metadata["max_y"]){
            specs.metadata["max_y"] = peak_stage; } }
		
        if((lower_stage != null)&&(lower_stage < specs.metadata["min_y"])){
          specs.metadata["min_y"] = lower_stage;
        }
	  }

      // add graph
	  if (typeof cur_releaseTimestamp !== "undefined"){
        series.push({
          id: modelspec.id + "_" + cur_releaseTimestamp,
          name: modelspec.title,
          type: 'line',
          showSymbol: true,
          showAllSymbol: false,
          symbolSize: function (val){
            return (val[2] > 0) ? (Math.round(val[2]/10) + 2) : 0;
          },
          tooltip:{
            formatter: function(val){
              var val_time = richhydroforecast01.timestampToDateLabel(val.value[0], true);
              return("Peak: " + val.value[1] + " ft at " + val_time);
            }
          },
          smooth: true,
          data: cur_timeseries
	    });
      }

      if(!hide_model)
        legend_names.push(modelspec.title);
    }
  });
  
  // set up current time
  series.push({
    id: "currentTime",
	name: "Current Time",
    type: 'line',
    smooth: false,
	itemStyle:{ normal:{ color:"#000000" } },
    data: [[specs.metadata["current_time"], specs.metadata["min_y"]], 
	       [specs.metadata["current_time"], specs.metadata["max_y"]]]
  });
  
  // set up lead time
  series.push({
    id: "leadtime",
    name: "Lead Time",
    type: 'line',
    smooth: false,
    data: [[specs.metadata["lead_time"], specs.metadata["min_y"]], 
	       [specs.metadata["lead_time"], specs.metadata["max_y"]]]
  });
  
  // observed
  series.push({
    id: "Observed",
	name: "Observed",
    type: 'scatter',
	symbol: 'circle',
    symbolSize: 5,
	itemStyle:{ normal:{ color:"#000000" } },
    data: specs.observed["timeseries_stg"],
    tooltip:{
      trigger: 'item',
	  showContent: true,
      formatter:function(the_val){
        var val_time = richhydroforecast01.timestampToDateLabel(the_val.value[0], true);
        return(the_val.value[1] + " ft at " + val_time);
	  }
    }
  });
  legend_names.push("Observed");
  
  // wrap up options
  options = {
    title: {
	  text: desc,
	  show: true,
	  subtext: 'Drainage area: ' + area,
	  padding:[0, 0, 150, 0,]
	},
	legend:{
      data:legend_names,
      show:true,
      padding:[30, 0, 0, 0, ],
	  align:'right',
	  top: 25,
      right: 20,
      textStyle:{ align:"right" }
    },
    grid: {
      top: 80,
      left: '2.5%',
      right: '1%',
      bottom: '8%',
      containLabel: true
    },
	xAxis: {
      min: specs.metadata["min_x"],
      max: specs.metadata["max_x"],
      type: 'value',
	  interval: 86400,
	  axisLabel:{
        show: true,
		rotate: 45,
		fontSize:10,
        formatter: function(val){
          if((val - specs.metadata["min_x"]) % 172800 == 0){
            return(richhydroforecast01.timestampToDateLabel(val));
          } else {
            return(null);
          }
        }
	  },
      axisTick:{
        interval: 86400
      }
    },
	yAxis: {
      name: "Stage (ft)",
      nameLocation: "middle",
      nameTextStyle: { 
        padding: [0,0,10,0],
		fontSize: 14
      },
      min: specs.metadata["min_y"],
      max: specs.metadata["max_y"],
      type: 'value'
    },
	tooltip: {
      trigger: 'axis',
	  showContent: true,
      axisPointer: {
        type: 'line',
        axis: 'x',
        snap: false,
        label:{
          show: true,
          formatter:function(the_val){
            return(richhydroforecast01.timestampToDateLabel(the_val.value, true));
          }
        }
      }
    },
    series:series
  }
  return(options);
}

/**
 * 
 */
richhydroforecast01.onSlideUpdateLabel = function(issue_timestamp){
  var lead_time;
  var lead_label = richhydroforecast01.timestampToDateLabel(issue_timestamp, true);
  var spanId = richhydroforecast01.sliderSpanId;
  var spanObj = document.getElementById(spanId);

  // define message
  if(richhydroforecast01.specifications.metadata["is_snapshot"]){
    spanObj.innerHTML = " around " + lead_label;
  } else {
    lead_time = richhydroforecast01.specifications.metadata["current_time"] - issue_timestamp;
	lead_time = Math.round(lead_time / 3600);
    if(lead_time > 48){
      lead_time = Math.round(lead_time / 24);
      spanObj.innerHTML = lead_time + " days ago (around " + lead_label + ")";
	} else {
      spanObj.innerHTML = lead_time + " hours ago (around " + lead_label + ")";
    }
  }
}

/**
 *
 */
richhydroforecast01.onSlideInput = function(){
  var slideObj = document.getElementById(richhydroforecast01.sliderId);
  var issue_timestamp = parseInt(slideObj.value);
  
  // update label and graph
  richhydroforecast01.onSlideUpdateLabel(issue_timestamp);
}

/**
 *
 */
richhydroforecast01.onSlideChange = function(){
  var slideObj = document.getElementById(richhydroforecast01.sliderId);
  var issue_timestamp = parseInt(slideObj.value);
  
  // update label and graph
  richhydroforecast01.onSlideUpdateLabel(issue_timestamp);
  richhydroforecast01.updateLeadTime(issue_timestamp);
}

/**
 * Check if minimal conditions. Console.logs are printed for errors.
 * RETURN: Boolean. True if are met, FALSE otherwise.
 */
richhydroforecast01.checkStart = function(div_id, specs){
  var all_ok = true;
  
  // check receiving div
  if(document.getElementById(div_id) == null){
    all_ok = false;
  }
  
  // check Echarts availability
  if(typeof echarts === "undefined"){
    all_ok = false;
  }
  
  // check minimum arguments provided
  // TODO - check forecasts or observed is available and valid
  
  return(all_ok);
}

/**
 * Example: 9 becomes 09, 99 keeps 99 and 1999 becomes 99
 */
richhydroforecast01.twoDigits = function(val){
  return(("0" + val).slice(-2));
}

/**
 * Converts a timestamp into a Date object
 */
richhydroforecast01.timestampToDateLabel = function(a_timestamp, has_hours){
  if((typeof(has_hours) !== "boolean") || (has_hours != true)){
	  has_hours = false;
  }
  if (Number.isInteger(a_timestamp)){
    var date_obj = new Date(a_timestamp * 1000);
    var date_str = richhydroforecast01.twoDigits(date_obj.getMonth() + 1) + '/';
	date_str += richhydroforecast01.twoDigits(date_obj.getDate()) + '/';
    date_str += date_obj.getFullYear();
    if (has_hours){
      date_str += " " + richhydroforecast01.twoDigits(date_obj.getHours());
	  date_str += ":" + richhydroforecast01.twoDigits(date_obj.getMinutes());
    }
    return(date_str);
  } else {
    console.log("Unexpected value: "+a_timestamp+" ("+typeof(a_timestamp)+").");
    return(null);
  }
}

/**
 * lead_timestamp : integer
 * refresh : boolean
 * sc_model_ids : [string] or null
 * callback_function : function
 * RETURN: Notthing. Calls the callback function
 */
richhydroforecast01.ajaxCall = function(lead_timestamp, refresh, sc_model_ids, callback_function, selected_models){
  var BASE_URL = modelplus.viewer.ws + "custom_ws/richhydroforecast_readjson.php%i%";
  var refresh_label = refresh ? 't' : 'f';
  var url = BASE_URL + "sc_runset_id=" + richhydroforecast01.runsetid;
  url += "%e%sc_model_id=" + richhydroforecast01.modelcomb_id;
  url += "%e%link_id=" + richhydroforecast01.link_id;
  url += "%e%refresh=" + refresh_label;
  url += ((selected_models == null)||(!refresh_label)) ? "" : "%e%sc_models_only="+selected_models.join(",");
  if(lead_timestamp != null){
    url += "%e%lead_timestamp="+lead_timestamp;
  }
  $.ajax({url: url, success: callback_function});
}
