# Backend - Model Run

This component is responsible for:
- processing *Runset Requests* submited by the *frontend*,
- executting Asynch simulations, and 
- submitting the outputs for the *backend-postprocess*.

It was originally designed to be hosted on UIowa clusters such as *Argon*.

## Setting up the environment

### Git sparse checkout

Suppose you will host your application on `[SYS-ROOT]/` directory for development.

Create the empty directory, move to there and initiate a git repository there:
```
$ mkdir [SYS-ROOT]/
$ cd [SYS-ROOT]/
$ git init
```

Add the IHMIS GitHub repository as the *origin* remote Git repository:
```
$ git remote add -f origin https://github.com/.../IHMIS.git
```

Activate sparse checkout and limit the versioned content to the *backend-modelrun* directory:
```
$ git config core.sparseCheckout true
$ echo 'backend-modelrun/' > .git/info/sparse-checkout
```

Pull the code from the origin repository, *develop* branch:
```
git pull origin develop
```

### Setting up configuration files

Copy all the content from the `conf-TEMPLATE/` folder to the `conf/` directory.

Go over each file in the `conf/` directory tree structure, adapting their content to your system's particularities. Replace the following inner terms:

- ```[RAW_ROOT]```: folder path for the ```/raw``` data folder; 
- ```[CODE_ROOT]```: folder path for the ```/dev/backend-modelrun/code``` data folder;
- ```[URL_PAGE]```: URL for the main page of the system (```http://...```);
- ```[URL_WAIT]```: URL for the waiting room for runset requests folder of the system (```http://...```);
- ```[ADD_SERV]```: username on ```backend-postprocess``` component;  
- ```[USR_SERV]```: address of the ```backend-postprocess``` component.

After each file is changed, rename the file by removing the `-TEMPLATE` prefix (example: `filesys-TEMPLATE.json` -> `filesys.json`).

### Setting up crontab 

In the *backend-modelrun* component, it is necessary a user which has his/her crontab set up following the instructions and the example described in ```backend-modelrun/code/cron```.    