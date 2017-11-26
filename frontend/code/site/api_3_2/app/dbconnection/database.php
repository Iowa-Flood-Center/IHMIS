<?php

use Illuminate\Database\Capsule\Manager as Capsule;

$capsule = new Capsule;

$base_folder_path = "../../../../conf/site/api_3_2/dbconnection/";

// add the connection to the static database
$conn_def = json_decode(file_get_contents($base_folder_path."dbdefinition_modelbacktime.json"), true);
$capsule->addConnection($conn_def, "model_backtime");

// add the connection to the precipitation database
$conn_def = json_decode(file_get_contents($base_folder_path."dbdefinition_precipitation.json"), true);
$capsule->addConnection($conn_def, "precipitation");

// add the connection to the artefacts database
$conn_def = json_decode(file_get_contents($base_folder_path."dbdefinition_artefacts.json"), true);
$capsule->addConnection($conn_def, "artefacts");

$capsule->setAsGlobal();
$capsule->bootEloquent();

?>