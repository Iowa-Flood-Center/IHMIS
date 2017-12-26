# Backend - Model Run - Code - Cron

The Bash files in this folder were developed to be executed continuously by job scheduling tools such as Cronjob.

A typical Crontab configuration would be:

	SHELL=/bin/bash

	IHMIS_BASH=<THIS_FOLDER>

    #minute (0-59)
    #|   hour (0-23)
    #|   |    day of the month (1-31)
    #|   |    |   month of the year (1-12 or Jan-Dec)
    #|   |    |   |   day of the week (0-6 with 0=Sun or Sun-Sat)
    #|   |    |   |   |   commands
    #|   |    |   |   |   |

    ## retrieve runsets from waiting room
    24,40,56 * * * *  bash $IHMIS_BASH"retrieve_runset_requests.sh"

    ## process retrieved runsets generating their representations
    16,32,48 * * * *  bash $IHMIS_BASH"process_runset_requests.sh"

	## retrieve and process runset merge requests
	28,52 * * * * bash $IHMIS_BASH"retrieve_runsetmerge_requests.sh"

    ## update list of available initial conditions in server IIHR-50
    23 16 * * * bash $IHMIS_BASH"initcond_availability_informer.sh"

**Note**: replace ```<THIS_FOLDER>``` (in 3rd line) by the folder to which the scripts were deployed. 

As a standard, the execution of each script will generate log files in the folders or file prefixes defined by variables in the ```conf/system.conf``` file. All ```CAPITAL_LETTERS``` variables described in this document must be defined in such configuration file.

**Important**: when the files are be stored and triggered on UIowa HPC, they will be executed in the *login node* of the clusters. Because of that, they are designed to preform minimum processing load. It is important to have it into consideration when performing changes or when considering including new scheduled jobs in the loop.     

## Retrieving Runset Requests

Execute ```retrieve_runset_requests.sh```. The main procedure of this script is to properly call ```call/retrieve_runset_requests.py``` script, which will look for *Runset Requests* in the frontend server, download/extract them to the ```RREQUEST_FOLDER``` folder and delete them from the frontend server. After downloaded, the ```.job``` file within is triggered to be executed by the processing nodes in the cluster (```qsub``` command).     

**Log folder/prefix**: defined on ```FPH_PREF_RETRIV```.

## Processing Runset Requests

Execute ```process_runset_requests.sh```. It logs files with  folder/prefix.

It will internally call ```process_runset_requests_remotely.sh``` when a non-processed runset in found. It logs into  folder.

**Log folder/prefix**: defined on ```FPH_PREF_PROCES``` (```process_runset_requests.sh```) and on ```FPH_INNE_PROCES``` (```process_runset_requests_remotely.sh```).

## Retrieving & Processing Runset Merge Requests

Execute ```retrieve_runsetmerge_requests.sh```.

It this script basically:

- performs the merge in the runsets on ```Backend - Model Run``` component; 
- calls the runset merger script on ```Backend - Post Processing``` component;
- deletes the Runset Request on ```Frontend``` component.

## Updating *regular initial conditions* information

This script keeps the *frontend* component informed about available initial conditions in the *Backend - Model Run* component.

```TODO```

**Log folder/prefix**: ```TODO``` 

## Log rotate

As log files are continuously being generated, an additional script is needed in order to perform regular *cleaning* activities.

```TODO```

**Log folder/prefix**: None