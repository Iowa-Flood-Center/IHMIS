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
http://.../api/sc_runset_requests/new
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
http://.../api/sc_runsets?do=get_new_runset_id
```

### Forcings

#### Obtain available Forcings for a simulation time interval

*Usage*:

```GET``` on

```
http://.../api/forcing_sources?from_type=[TODO]&timestamp_ini=[TIMESTAMP]&timestamp_end=[TIMESTAMP]
``` 

Where *[TODO]* is expected to be ```TODO``` and *[TIMESTAMP]* is expected to be replaced by independent integer values indicating the initial and final unix timestamps, in seconds, of a time interval.

### Representations

#### Obtain Representations related to a Hillslope Model

*Usage*:

```GET``` on

```
http://.../api/sc_runsets?from_hlmodel=[HLM-id]
``` 

Where *[HLM-id]* is expected to be replaced by values such as *190*, *254*, ...

#### Obtain Representations related to comparisons between Hillslope Models

```GET``` on

```
http://.../api/sc_runsets?from_hlmodel=[HLM-id]&from_hlmodel_compareto=[HLM-id]  
```

Where each *[HLM-id]* is expected to be replaced by independent values such as *190*, *254*, ...