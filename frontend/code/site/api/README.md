# Frontend - API

```
TODO - introduction
```

A javascript interface for the API is implemented on ```/common/scripts/modelplus.api.js```.

## The API endpoints

The API adopts an RESTful interface.

```
TODO - more details
```

## Resources

### Runset Requests

#### Create

Submits a new Runset Request. 
Is expected to be used only with the Runset Requester interface.

*Usage*:

```POST``` on

```
http://.../api/public/sc_runset_requests/new
```

with a long set of global and model-specific parameter.

Global parameters:

- **runset_id**: *String*. ```TODO```
- **runset_title**: *String*. ```TODO```
- **timestamp_ini**: *Integer*. ```TODO```
- **timestamp_end**: *Integer*. ```TODO```
- **reference_ids**: *String*. Comma-separated Reference IDs.
- **server_addr**: *String*. ```TODO```
- **email**: *String*. ```TODO```
- **num_models**: Integer. ```TODO```
- **asynch_ver**: String. ```TODO```

Model-specific parameters for the *N-th* model:

- **model\_id\_N**: *String*. ```TODO```
- **model\_title\_N**: *String*. ```TODO```
- **model\_desc\_N**: *String*. ```TODO```
- **hillslope\_model\_N** : *Integer*. ```TODO```
- **forcing\_source\_N\_i**: *Integer*. Source id for *i-th* forcing
- **model\_par\_N\_i**: *Float*. Value for the *i-th* global parameter
- **model\_parlbl\_N\_i**: *String*. Label for the *i-th* global parameter
- **model\_repr\_N**: *String*. Comma-separated Representation IDs
- **model\_eval\_N**: *String*. ```TODO``` 

### Runsets

#### Obtain available ID

Provides an ID that can be used to uniquely identify a new Runset.  

*Usage*:

```GET``` on

```
http://.../api/public/sc_runsets?do=get_new_runset_id
```

#### Reserve Runset iD

Instantly creates a dummy entry in the file system in order to 'reserve' the ID for a Runset being run and post-processed.

``` POST``` on

```
http://.../api/public/sc_runset_results
```

with the following argument:
- **runset_id**: *String*. Runset ID to be reserved.

### Forcings

#### Obtain available Forcings for a simulation time interval

*Usage*:

```GET``` on

```
http://.../api/public/forcing_sources?from_type=[TODO]&timestamp_ini=[TIMESTAMP]&timestamp_end=[TIMESTAMP]
``` 

Where *[TODO]* is expected to be ```TODO``` and *[TIMESTAMP]* is expected to be replaced by independent integer values indicating the initial and final unix timestamps, in seconds, of a time interval.

### Representations

#### Obtain Representations related to a Hillslope Model

*Usage*:

```GET``` on

```
http://.../api/public/sc_runsets?from_hlmodel=[HLM-id]
``` 

Where *[HLM-id]* is expected to be replaced by values such as *190*, *254*, ...

#### Obtain Representations related to comparisons between Hillslope Models

```GET``` on

```
http://.../api/sc_runsets?from_hlmodel=[HLM-id]&from_hlmodel_compareto=[HLM-id]  
```

Where each *[HLM-id]* is expected to be replaced by independent values such as *190*, *254*, ...

## Development

The RESful interface was created using Eloquent ORM. This framework acts as an PHP abstraction level for the data (be it in the database or in the filesystem) and is built/deplyed using Composer Dependency Manager.

### Models and namespaces

Object-Role Models (OR Models) are representations of data entities in PHP. For example, *RunsetRequester* is a class in PHP which has methods for managing specifically the files that compose runset requests present in the frontend server, while *HlModel* is a class that presents functionalities for accessing the static data that describes HLM-Models present in the database.

The OR Models are logically clustered into PHP namespaces, which are reflected into subdirectories within ```api/app/``` folder.

For adding or editing such namespaces, it is necessary to edit the file ```api/composer.json```, specifically the section ```autoload.psr-4``` after the code was implemented. Later, for the changes to take effect, execute the command in the ```api/``` directory for updating Composer definitions:

```
php composer.phar update
```

### Connections to the database

Each different database accessed in must be described by a *.json* file, stored on ```frontend/conf/site/api/dbconnection```, with the following general structure:

```
{
  "host": [HOST_ADDRESS],
  "port": [HOST_DB_PORT],
  "driver": [DB-DRIVE],
  "database": [DB_NAME],
  "username": [DB_USER],
  "password": [DB_PASS],
  "charset": "utf8"
}
```

where:
- ```[DB-DRIVE]``` is the driver to be used in the connection (current standard values is *"pgsql"*, for PostGreSQL), 
- ```[HOST_ADDRESS]``` is the database host address,
- ```[HOST_DB_PORT]``` is the port used for the database host (current standar value is *5432*),
- ```[DB_NAME]``` is the database name to be accessed,
- ```[DB_USER]``` and ```[DB_PASS]``` are the username and password to be used for acessing the dataabse.

After created, such file must be referenced as a database connection, and identified by an ID, in the ```api/app/dbconnection/database.php``` file by a pair of lines such as:

```
$conn_def = json_decode(file_get_contents($base_folder_path.[FILE_NAME]), true);
$capsule->addConnection($conn_def, [CONNECTION_ID]);
```

Changes become effective after Composer is updated (as described in the previous subsection).

### Entry points

Entry points are managed in the ```api/public/api.php```. Basically, each entry point is implemented by an individual file in ```api/public/ws/``` folder.
