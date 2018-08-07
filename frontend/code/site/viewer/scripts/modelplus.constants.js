// TODO - learn headers for globals...

/**
 * The ModelPlus variables and functions are being moved to this namespace to avoid clutering the global namespace.
 * @namespace
 */
var modelplus = modelplus || {};

(function () {
  "use strict";
  
  modelplus.ids = modelplus.ids || {};
  modelplus.labels = modelplus.labels || {};
  
  var mpi = modelplus.ids;
  
  // DOM ids - MENU - IFIS Specific
  mpi.BACKGROUND_DARK = "darkenBackground";
  
  // DOM ids - MENU - ModelPlus Specific
  mpi.MENU_SELECT_CLASS = "npact";
  mpi.MENU_MAIN_ALERT_DIV = "main_alert_div";
  mpi.MENU_MAIN_LOADING_DIV = "main_loading_div";
  mpi.MENU_RUNSET_SBOX_DIV = "main_runset_sbox_div";
  mpi.MENU_RUNSET_SBOX = "main_runset_sbox";
  mpi.MENU_RUNSET_ABOUT = "about_runset";
  mpi.MENU_MODEL_MAIN_SBOX_DIV = "main_model_sbox_div";
  mpi.MENU_MODEL_MAIN_SBOX = "main_model_sbox";
  mpi.MENU_MODEL_ABOUT = "about_model";
  mpi.MENU_MODEL_MAIN_RADIO_DIV = "model_main_radio_div";
  mpi.MENU_MODEL_MAIN_SELEC_DIV = "model_main_param_div";
  mpi.MENU_MODEL_COMP_SBOX = "comp_model_sbox"; // comp = comparison
  mpi.MENU_MODEL_COMP_RADIO_DIV = "model_comp_radio_div";
  mpi.MENU_MODEL_COMP_SELEC_DIV = "model_comp_param_div";
  mpi.MENU_MODEL_COMPMST_SELEC_DIV = "model_compmst_param_div";
  mpi.MENU_MODEL_EVAL_RADIO_DIV = "model_eval_radio_div";
  mpi.MENU_MODEL_EVAL_SELEC_DIV = "model_eval_param_div";
  mpi.MENU_MODEL_COMB_RADIO_DIV = "model_comb_radio_div";
  mpi.MENU_MODEL_COMB_PARAM_DIV = "model_comb_param_div";
  mpi.MENU_MODEL_HYDR_RADIO_DIV = "model_hydr_radio_div";
  mpi.MENU_MODEL_HYDR_PARAM_DIV = "model_hydr_param_div";
  
  // DOM ids - MENU AGGREGATION
  mpi.MENU_CONTENTS = [mpi.MENU_MODEL_MAIN_SELEC_DIV, 
					   mpi.MENU_MODEL_COMPMST_SELEC_DIV, 
					   "sc_set_tools", 
				       mpi.MENU_MODEL_EVAL_SELEC_DIV,
					   mpi.MENU_MODEL_COMB_PARAM_DIV,
					   mpi.MENU_MODEL_HYDR_PARAM_DIV];
  
  // DOM ids - MODALs
  modelplus.ids.MODAL_DIV = "modal_div";
  modelplus.ids.MODAL_CLOSE_SPAN = "modal_close_span";
  modelplus.ids.MODAL_RAWDATA_SPAN = "modal_rawdata_span";
  modelplus.ids.MODAL_HYDROGRAPH = "modal_hidrograph_div";
  modelplus.ids.MODAL_HYDROGRAPH_CONTENT = "modal_content_hidrograph_div";
  modelplus.ids.MODAL_HYDROGRAPH_CONTENT_MODELSCONF = "modal_content_hidrograph_modelsconf_div";
  modelplus.ids.MODAL_HYDROGRAPH_IFISBASED = "modal_hidrograph_ifisbased_div";
  
  // DOM ids - LEGEND
  modelplus.ids.LEGEND_BOTTOM_TITLE_DIV = "legend_bot_titl_div";
  modelplus.ids.LEGEND_BOTTOM_DIV = "colorscale_con";
  modelplus.ids.LEGEND_BOTTOM_MODELS_DIV = "legend_bot_mdls_div";
  modelplus.ids.LEGEND_BOTTOM_MODEL1_DIV = "legend_bot_mdl1_div";
  modelplus.ids.LEGEND_BOTTOM_MODEL2_DIV = "legend_bot_mdl2_div";
  modelplus.ids.LEGEND_TOP_DIV = "legend_top_div";
  modelplus.ids.LEGEND_TOP_HID = "legend_top_hid";
  
  // General definitions
  modelplus.COLOR_REFERENCE = "#000000";
  modelplus.COLOR_NOW = "#777777";
  
  modelplus.COLOR_THRESHOLD_ACTION   = "#ffcc55";
  modelplus.COLOR_THRESHOLD_FLOOD    = "#ff8833";
  modelplus.COLOR_THRESHOLD_MODERATE = "#ff0000";
  modelplus.COLOR_THRESHOLD_MAJOR    = "#ff77ff";
  
  // Menu texts
  modelplus.labels.NO_REPRESENTATION = "No representations available.";
  modelplus.labels.NO_EVALUATIONS = "No evaluations available.";
  modelplus.labels.NO_COMPARISONS = "No comparisons available.";
  modelplus.labels.SELECT_RUNSET = "Select a Runset.";
  modelplus.labels.SELECT_MODEL = "Select a Model.";
  
  // About pop-up look and feel
  modelplus.ABOUT_CLOSE_BUTTON = 27;
  
  // Modal Hydrograph pop-up look and feel
  modelplus.MODAL_HYDROGRAPH_CLOSE_BUTTON = 27;
  modelplus.MODAL_HYDROGRAPH_BGCOLOR = "#FFFFFF";
  modelplus.MODAL_HYDROGRAPH_WIDTH = "850px";
  modelplus.MODAL_HYDROGRAPH_HEIGHT = "560px";
  modelplus.MODAL_HYDROGRAPH_CONTENT_HEIGHT = "540px";
  
})();
 