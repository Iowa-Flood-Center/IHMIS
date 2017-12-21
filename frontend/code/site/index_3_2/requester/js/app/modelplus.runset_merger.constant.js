var modelplus = modelplus || {};

(function () {
  "use strict";

  // define model constants
  modelplus.model_requester = modelplus.model_requester || {};
  modelplus.model_requester.constant = modelplus.model_requester.constant || {};
  
  // define HTML ids
  
  modelplus.model_requester.constant.id = modelplus.model_requester.constant.id || {};
  var ids = modelplus.model_requester.constant.id;
  
  // basic
  ids.UPPER_SPANS_DIV = "upper_spans_div";
  ids.LOWER_SPANS_DIV = "lower_spans_div";
  ids.FROM_RUNSET_SPAN = "from_runset_span";
  ids.TO_RUNSET_SPAN = "to_runset_span";
  
  // step 01
  ids.RUNSET_CHOICE_DIV = "runsets_choice_div";
  ids.RUNSET_FROM_SPAN = "runset_label_from_span";
  ids.RUNSET_FROM_INPUT = "runset_id_from_input";
  ids.RUNSET_TO_DIV = "runset_to_div";
  ids.RUNSET_TO_SPAN = "runset_label_to_span";
  ids.RUNSET_TO_INPUT = "runset_id_to_input";
  
  // step 02
  ids.REFERENCES_COPY_DIV = "references_copy_div";
  ids.REFERENCES_COPY_LIST_DIV = "references_copy_list_div";
  ids.REFERENCES_COPY_TITLE = "references_copy_h2";
  ids.REFERENCES_COPY_LABEL = "references_copy_label";
  ids.REFERENCES_COPY_SPAN = "references_copy_span";
  ids.REFERENCES_COPY_ID_PREF = "references_copy_id_";
  
  // step 03
  ids.COPY_MODELS_ADDED_DIV = "copy_models_added_div";
  
  // step 04
  ids.SET_MODELS_COMPAR_H2 = "copy_models_comparison_h2";
  ids.SET_MODELS_COMPAR_DIV = "copy_models_comparison_div";
  ids.SET_MODELS_COMPAR_NAMES = "copy_models_comparison_span";
  ids.SET_MODELS_COMPAR_LABEL = "copy_models_comparison_label";
  
  // step 05
  ids.COPY_MODELS_COMPOS_H2 = "copy_models_compositions_h2";
  ids.COPY_MODELS_COMPOS_DIV = "copy_models_compositions_div";
  ids.COPY_MODELS_COMPOS_NAMES = "copy_models_compositions_span";
  ids.COPY_MODELS_COMPOS_LABEL = "copy_models_compositions_label";
  
  // step 06
  ids.CONTACT_INFO_DIV = "contact_info_div";
  ids.CONTACT_EMAIL_INPUT = "contact_email_input";
  ids.HOWCONTACT_TITLE = "contact_info_h2";
  ids.HOWCONTACT_LABEL = "contact_info_label";
  ids.HOWCONTACT_SPAN = "contact_info_span";
  ids.HOWCONTACT_RADIO_NAME = "how_contact";
  ids.HOWCONTACT_RADIOS_DIV = "how_contact_radios_div";
  
  ids.RUNSET_BASIC_HR = "runset_basic_hr";
  ids.RUNSET_MID_DATE_SPAN = "runset_mid_date_span";
  ids.RUNSET_MID_DATE_INPUT = "runset_mid_date_input";
  ids.RUNSET_MID_DATE_PREDEF_DIV = "runset_mid_date_predefined_div";
  
  ids.RUNSET_INFO_DIV = "runset_info_div";
  ids.RUNSET_INFO_LABEL_SPAN = "runset_info_label_span";
  ids.RUNSET_INFO_INTER_SPAN = "runset_info_interval_span";
  ids.RUNSET_INFO_MODEL_SPAN = "runset_info_models_span";
  ids.RUNSET_INFO_REFER_SPAN = "runset_info_references_span";
  
  ids.WHATRUN_RADIO_NAME = "what_run";
  ids.RUNSET_INIEND_DATE_SPAN = "runset_iniend_date_span";
  ids.SIMULATION_TYPE_DIV = "simulation_type_div";
  
  
  
  ids.SET_MODELS_DIV = "set_models_div";
  ids.SET_MODELS_TITLE = "set_models_h2";
  ids.SET_MODELS_LABEL = "set_models_label";
  ids.SET_MODELS_NAMES = "set_models_names";
  ids.SET_MODELS_ADD_DIV = "set_models_add_div";
  ids.SET_MODELS_INNER_PREF = "set_models_inner_div_";
  ids.SET_MODELS_INNER_FORC_DIV_PREF = "set_models_inner_forcing_div_";
  ids.SET_MODELS_INNER_PARM_DIV_PREF = "set_models_inner_glbparm_div_";
  ids.SET_MODELS_INNER_EVAL_DIV_PREF = "set_models_inner_evaluat_div_";
  ids.SET_MODELS_INNER_REPR_DIV_PREF = "set_models_inner_represn_div_";
  ids.SET_MODELS_SEL_REPR_PREF = "model_representation_";
  
  ids.SET_MODELS_REPR_COMBINED_DIV = "set_models_repr_combined_div";
  ids.SET_MODELS_REPR_COMBINED_INNER_DIV = "set_models_repr_combined_inner_div";
  ids.SET_MODELS_INNER_REPR_COMBINED_DIV_PREF = "set_models_inner_repr_combined_div_";
  
  
  
  
  
  ids.WHAT_DO_DIV = "what_do_div";
  ids.WHAT_DO_H2 = "what_do_h2";
  ids.WHAT_DO_SPAN = "what_do_span";
  ids.WHAT_DO_LABEL = "what_do_label";
  ids.WHAT_DO_RADIO_NAME = "what_do";
  ids.WHAT_DO_RADIOS_DIV = "what_do_radios_div";
  
  
  
  //ids.BUTTONS_DIV = "buttons_div"
  //ids.LABEL_NEXT_STEP_ERROR = "label_next_step_error";
  //ids.LABEL_NEXT_STEP = "label_current_step";
  //ids.BUTTON_PREV_STEP = "button_prev_step";
  //ids.BUTTON_NEXT_STEP = "button_next_step";
  //ids.BUTTON_SUBMIT = "button_submit";
  //ids.SUBMIT_SUCCESS_DIV = "submit_success_div";
  //ids.SUBMIT_FAILURE_DIV = "submit_failure_div";
  //ids.SUBMIT_FAILURE_MSG_DIV = "submit_failure_msg_div";
  
  // define CSS classes
  
  //modelplus.model_requester.constant.classes = modelplus.model_requester.constant.classes || {};
  //modelplus.model_requester.constant.classes.FILLING_FORM = "filling_form";
  
  // define labels
  modelplus.model_requester.constant.labels = modelplus.model_requester.constant.labels || {};
  var labels = modelplus.model_requester.constant.labels;
  
  labels.LOADING = "Loading...";
  
  //modelplus.model_requester.constant.labels.REFERENCES_SELECTION = "Select References";
  //modelplus.model_requester.constant.labels.HLM_SELECTION = "[Select a Hillslope model]";
  //modelplus.model_requester.constant.labels.NONE = "None";
  //modelplus.model_requester.constant.labels.SUBMIT_FAILURE = "Exception";

})();
