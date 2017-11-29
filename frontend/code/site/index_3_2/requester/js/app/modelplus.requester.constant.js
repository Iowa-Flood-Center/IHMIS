var modelplus = modelplus || {};

(function () {
  "use strict";

  // define model constants
  modelplus.requester = modelplus.requester || {};
  modelplus.requester.constant = modelplus.requester.constant || {};
  
  // define HTML ids
  
  modelplus.requester.constant.id = modelplus.requester.constant.id || {};
  
  var ids = modelplus.requester.constant.id;
  
  ids.RUNSET_NAME_DIV = "runset_name_div";
  ids.RUNSET_NAME_SPAN = "runset_name_span";
  ids.RUNSET_NAME_INPUT = "runset_name_input";
  ids.RUNSET_BASIC_HR = "runset_basic_hr";
  ids.RUNSET_MID_DATE_SPAN = "runset_mid_date_span";
  ids.RUNSET_MID_DATE_INPUT = "runset_mid_date_input";
  ids.RUNSET_MID_DATE_PREDEF_DIV = "runset_mid_date_predefined_div";
  
  ids.WHATRUN_RADIO_NAME = "what_run";
  ids.RUNSET_INIEND_DATE_SPAN = "runset_iniend_date_span";
  ids.SIMULATION_TYPE_DIV = "simulation_type_div";
  
  ids.REFERENCES_INCLUDE_DIV = "references_include_div";
  ids.REFERENCES_INCLUDE_LIST_DIV = "references_include_list_div";
  ids.REFERENCES_INCLUDE_TITLE = "references_include_h2";
  ids.REFERENCES_INCLUDE_LABEL = "references_include_label";
  ids.REFERENCES_INCLUDE_NAMES = "references_include_names";
  ids.REFERENCES_INCLUDE_ID_PREF = "references_include_id_";
  
  ids.SET_MODELS_DIV = "set_models_div";
  ids.SET_MODELS_TITLE = "set_models_h2";
  ids.SET_MODELS_LABEL = "set_models_label";
  ids.SET_MODELS_NAMES = "set_models_names";
  ids.SET_MODELS_ADD_DIV = "set_models_add_div";
  ids.SET_MODELS_ADDED_DIV = "set_models_added_div";
  ids.SET_MODELS_INNER_PREF = "set_models_inner_div_";
  ids.SET_MODELS_INNER_FORC_DIV_PREF = "set_models_inner_forcing_div_";
  ids.SET_MODELS_INNER_PARM_DIV_PREF = "set_models_inner_glbparm_div_";
  ids.SET_MODELS_INNER_EVAL_DIV_PREF = "set_models_inner_evaluat_div_";
  ids.SET_MODELS_INNER_REPR_DIV_PREF = "set_models_inner_represn_div_";
  ids.SET_MODELS_SEL_REPR_PREF = "model_representation_";
  
  ids.SET_MODELS_COMPAR_H2 = "set_models_comparison_h2";
  ids.SET_MODELS_COMPAR_DIV = "set_models_comparison_div";
  ids.SET_MODELS_COMPAR_NAMES = "set_models_comparison_span";
  ids.SET_MODELS_COMPAR_LABEL = "set_models_comparison_label";
  
  ids.SET_MODELS_COMPOS_H2 = "set_models_compositions_h2";
  ids.SET_MODELS_COMPOS_DIV = "set_models_compositions_div";
  ids.SET_MODELS_COMPOS_NAMES = "set_models_compositions_span";
  ids.SET_MODELS_COMPOS_LABEL = "set_models_compositions_label";
  
  ids.WHAT_DO_DIV = "what_do_div";
  ids.WHAT_DO_H2 = "what_do_h2";
  ids.WHAT_DO_SPAN = "what_do_span";
  ids.WHAT_DO_LABEL = "what_do_label";
  ids.WHAT_DO_RADIO_NAME = "what_do";
  ids.WHAT_DO_RADIOS_DIV = "what_do_radios_div";
  
  ids.CONTACT_INFO_DIV = "contact_info_div";
  ids.CONTACT_EMAIL_INPUT = "contact_email_input";
  ids.HOWCONTACT_TITLE = "contact_info_h2";
  ids.HOWCONTACT_LABEL = "contact_info_label";
  ids.HOWCONTACT_SPAN = "contact_info_span";
  ids.HOWCONTACT_RADIO_NAME = "how_contact";
  ids.HOWCONTACT_RADIOS_DIV = "how_contact_radios_div";
  
  ids.BUTTONS_DIV = "buttons_div"
  ids.LABEL_NEXT_STEP_ERROR = "label_next_step_error";
  ids.LABEL_NEXT_STEP = "label_current_step";
  ids.BUTTON_PREV_STEP = "button_prev_step";
  ids.BUTTON_NEXT_STEP = "button_next_step";
  ids.BUTTON_SUBMIT = "button_submit";
  ids.SUBMIT_SUCCESS_DIV = "submit_success_div";
  ids.SUBMIT_FAILURE_DIV = "submit_failure_div";
  ids.SUBMIT_FAILURE_MSG_DIV = "submit_failure_msg_div";
  
  // define CSS classes
  
  modelplus.requester.constant.classes = modelplus.requester.constant.classes || {};
  modelplus.requester.constant.classes.FILLING_FORM = "filling_form";
  
  // define labels
  
  modelplus.requester.constant.labels = modelplus.requester.constant.labels || {};
  
  modelplus.requester.constant.labels.REFERENCES_SELECTION = "Select References";
  modelplus.requester.constant.labels.HLM_SELECTION = "[Select a Hillslope model]";
  modelplus.requester.constant.labels.NONE = "None";
  modelplus.requester.constant.labels.SUBMIT_FAILURE = "Exception";
  
  // define recommended dates
  
  modelplus.requester.constant.predefined_mid_dates = [
    {"date_str":"20080606",
     "label":"2008 Flood - June",
     "enable":true},
	{"date_str":"20091029",
     "label":"2009 Flood - October",
     "enable":true},
	{"date_str":"20100625",
     "label":"2010 Flood - June",
     "enable":true},
	{"date_str":"20100815",
     "label":"2010 Flood - August",
     "enable":true},
	{"date_str":"20110616",
     "label":"2011 Flood - June",
     "enable":true},
	{"date_str":"20130529",
     "label":"2013 - May",
     "enable":true},
	{"date_str":"20140626",
     "label":"2014 - June",
     "enable":true},
	{"date_str":"20150622",
     "label":"2015 - June",
     "enable":true},
	{"date_str":"20151205",
     "label":"2015 - December",
     "enable":false},
	{"date_str":"20160921",
     "label":"2016 - September",
     "enable":true}
  ];

})();
