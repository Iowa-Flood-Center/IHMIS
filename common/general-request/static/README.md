# General Request - Static

Set of files holding static definitions for the tool.

## valid_options.json

Description of all actions that can be requested and expected arguments for each of them.

Is it structured as an hierarchical JSON file with all the options for:

- the ```target``` field (values starting with ```~```), 
- the ```action``` field (values starting with ```-```), and 
- all mandatory fields for ```argument``` (values starting with ```+```).

This document should not be taken as a template for a Generic Request, but as a descriptor.

Two valid General Requests are given in the following examples.

### Create a new runset 

Suppose a runset with the title "Event 123456" will be created.

    {
      "general_request":{
        "target":"runset",
        "action":"create",
        "arguments":{
          "runset_id":"rset123456",
          "title":"Event 123456"
        }
      }
    }

### Add a model to a representation combined

Suppose we are in the context of a runset with id *rset123456* and there is a pre existing *model combination* (id: ```mymodelcomb```) that contain a *representation combined* (id: ```myreprcomb```) to which we want to add the models ```mdl7``` and ```mdl9```.

    {
      "general_request":{
        "target":"model_combination",
        "action":"add_to_representation_combined",
        "arguments":{
          "runset_id":"rset123456",
          "modelcomb_id":"mymodelcomb",
          "representation_combined_id":"myreprcomb"
          "model_ids":["mdl7", "mdl9"],
          "reference_ids":[]
        }
      }
    }