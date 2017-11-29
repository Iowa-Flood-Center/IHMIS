<?php

// -----------------------------{ LOAD }------------------------------ //

date_default_timezone_set('America/Chicago');

require '../vendor/autoload.php';
require_once 'util/util.php';
require_once '../app/dbconnection/database.php';
require_once '../app/fsconnection/foldersystem.php';

use Illuminate\Database\Capsule\Manager as Capsule;

// -----------------------------{ SLIM }------------------------------ //

$app = new \Slim\Slim();
$app->dbs = function(){ return(new Capsule); };
$app->fss = FolderSystemFactory::create(is_sandbox());
$app->log = (object) null;

// ----------------------{ MODELPLUS SPECIFICS }---------------------- //

$app->invalid_argument = array('ERROR' => 'Invalid argument'); 
load_utils($app);

// -----------------------------{ ROUTE }----------------------------- //

// --- Static definitions

// request statical HL-Models
$app->get('/hl_models', function() use ($app){
	require './ws/hl_models.php';
	process_get_request($app);
});

// request statical global parameters of HL-Models
$app->get('/hl_models_global_parameters', function() use ($app){
	require './ws/hl_models_global_parameters.php';
	process_get_request($app);
});

// request statical SC-References
$app->get('/sc_references', function() use ($app){
	require './ws/sc_references.php';
	process_get_request($app);
});

// request statical SC-Representations
$app->get('/sc_representations', function() use ($app){
	require './ws/sc_representations.php';
	process_get_request($app);
});

// 
$app->get('/sc_representationscomp', function() use ($app){
	require './ws/sc_representation_compositions.php';
	process_get_request($app);
});

// request statical SC-Evaluations
$app->get('/sc_evaluations', function() use ($app){
	require './ws/sc_evaluations.php';
	process_get_request($app);
});

// request forcing types
$app->get('/forcing_types', function() use ($app){
	require './ws/forcing_types.php';
	process_get_request($app);
});

// request forcing sources
$app->get('/forcing_sources', function() use ($app){
	require './ws/forcing_sources.php';
	process_get_request($app);
});

// request forcing precipitations
// TODO - remove it - replace by generic ForcingSources one
$app->get('/forcing_precipitations', function() use ($app){
	require './ws/forcing_precipitations.php';
	process_get_request($app);
});

// --- Runset Requests

// request runsets requests
$app->get('/sc_runset_requests', function () use ($app) {
	require './ws/sc_runset_requests.php';
	process_get_request($app);
});

// create new runset request
$app->post('/sc_runset_requests/new', function () use ($app) {
	require './ws/sc_runset_requests.php';
	process_post_request($app);
});

// delete a runset request
$app->delete('/sc_runset_requests/:file_name', 
             function($file_name) use ($app){
	require './ws/sc_runset_requests.php';
	process_delete_request($app, $file_name);
});

// --- Runset Results

// creates a new runset result
$app->post('/sc_runset_results/', function () use ($app) {
	require './ws/sc_runset_results.php';
	process_post_request($app);
});

// list all runset results
$app->get('/sc_runset_results/', function() use ($app) {
	require './ws/sc_runset_results.php';
	process_get_request($app);
});

// delete an specific runset result
$app->delete('/sc_runset_results/:sc_runset_id', 
             function($sc_runset_id) use ($app) {
	require './ws/sc_runset_results.php';
	process_delete_request($app, $sc_runset_id);
});

$app->get('/sc_forecast_set/', function() use ($app) {
	require './ws/sc_forecast_set.php';
	process_get_request($app);
});

// --- Others

// list all Points Of Interest (POIs)
$app->get('/pois/', function() use ($app) {
	require './ws/pois.php';
	process_get_request($app);
});

// 
$app->get('/sc_runsets/', function() use ($app) {
	require './ws/sc_runsets.php';
	process_get_request($app);
});

//
$app->get('/sc_model_results/', function() use ($app) {
	require './ws/sc_model_results.php';
	process_get_request($app);
});

// --- a test

$app->get('/test/', function () use ($app) {
	require './ws/_test.php';
	//do_your_job($name);
});

// ------------------------------{ CALL }----------------------------- //

$app->response->headers->set('Content-Type', 'application/json');
$app->run();

?>
