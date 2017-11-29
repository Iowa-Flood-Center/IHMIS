# Backend - Model Run - Tools

Due to the fact that most of tools required by the ```Backend - Model Run``` component are flexible enought for being used in different circunstances, they were versioned into a separated project named ```Asynch Tools```.

## Setting up *regular initial conditions*

For each Hillslope-Link Model a set of initial conditions must be made available in advance in the ```Backend - Model Run``` component of the system.
 
It was arbitrarily defined that each year since 2008 must have initial conditions at 00:00 am (UTC) of the 1st, 11th and 21st days of the months between (and including) April and November. As these initial conditions are expected to be available at an almost regular base of 10-days interval, they are named *regular initial conditions*. The months of December, January, February and March were excluded because snow condition is still not supported by the model and it plays major role during the Winter season.

To obtain the *regular initial conditions* for a specific year, the following steps are performed:

- create a *baseflow initial condition* for the whole state for April 1st;
- perform an 1-year-long Asynch simulation using *Top Layer* model and generating multiple outputs;
- select and move the *regular initial conditions* to the proper repository;
- convert outputs from *Top Layer* to another model (if needed). 

Each of these steps are described as following.

### Creating the *baseflow initial condition*

Use the ```initialcondition_generator_254_baseflow.py``` script of ```Asynch Tools``` project. Use the initial date of March 20th, the final date of April 1st and the soil water column value of 0.02. 

Suppose you are going to set up the initial conditions for 2010 and will save the temporary output into a the folder ```~/baseflow_init_cond```. A typical call would be:

```
$ python initialcondition_generator_254_baseflow.py 2010-03-20 2010-04-01 ~/baseflow_init_cond -swc 0.02
```

The output format will be in ```.rec``` plain text format. You may want to convert it into ```.h5``` binary format. For doing so, the tool ```file_converter_rec_to_h5.py``` may be used.

**Tip:** As sometimes issues related to the rainfall input may happen, you can use the ```plot_timeseries_h5_outputs.py``` tool (```Asynch Tools```) to check if any input was registered. A typical call would be 

```$ python plot_timeseries_h5_outputs.py -linkid 434514 -h5_file <FIRST H5 FILE> -field 4```, 

in which the rainfall accumulation for the output link of the Turkey watershed is displayed. If *Field 4* gets different from *0.0*, then success.  

**Note:** Some pre-calculated *baseflow initial conditions* are available at the ```IHMIS Ancillary Files``` project.

### Performing 1-year-long Asynch simulation

Perform an *Asynch simulation* using a *global file* with the main following characteristics:

- Model type: *254*;
- Simulation period: from *YYYY-04-01 00:00* to *YYYY-12-02* 00:00;
- Global parameters: the ones adopted as standard for *254* by IFC;
- Topology / parameters: for the entire state of Iowa\*;
- Initial states: the path for the *baseflow initial condition* created previously;
- Rainfall forcing: database connector file for *Stage-IV* QPE\*;
- Evapo-transpiration forcing: monthly recurring file\*;
- Reservoirs forcing: no;
- Dams: no;
- Reservoirs forcing feeds: no;
- Timeseries / peakflows: no;
- Snapshot information: 
  - type: 4 (.h5 recurrent)
  - time interval: 1440 (equivalent to 24 hours)
  - output name: state254.h5

( **\*** : file available in the ```IHMIS Ancillary Files``` project )  

### Selecting the *regular initial conditions*

After the 1-year simulation (which may take about 2 hours to complete), around 275 snapshot files are expected to be produced, each of them related to the 00:00 (UTC) of a day in the year.

To select only the files associated to the 1st, 11th and 21st days of each month, use the ```initialcondition_selector_10days.py``` script of ```Asynch Tools TEMP``` project. A typical call would be:

```$ python initialcondition_selector_10days.py -folder <FOLDER_PATH>/ -fn```

### Convert outputs from *Top Layer* to another model

Usually, the model 254 has enough states to allow the "translation" of an *Top-Layer* initial condition file to other HLM models. For doing so, it can be used the ```file_converter_hlmodels_h5.py``` script of ```Asynch Tools``` project.

A typical call to obtain and initial condition for 190 (Constant Runoff) from an 254 (Top Layer) initial condition would be:

```
$ python file_converter_hlmodels_h5.py -mode d -in_path <IN_FOLDER_PATH> -out_path <OUT_FOLDER_PATH> -out_hl 190
```