# IHMIS

IHMIS stands for Iowa Hydrologic Model Information System.

## The IHMIS sub-systems

IHMIS is composed by three major components - *frontend*, *backend-modelrun* and *backend-postprocessing* - defined following the separation of concerns approach.

Each component is composed by two parts: the *system* (what is tracked: codes, configuration files, assets) and the *raw* (untracked elements: data, logs, ancillary files...)

The general folder structure for all the *systems* of the three components follow the general hierarchy:

```
[SYS_ROOT]⊦---code
          ∣    ⊦---call
          ∣    ⊦---cron
          ∣    ∟---tool
          ⊦---assets
          ∣    ⊦---src
          ∣    ∟---dist
          ∟---conf
```

while the *data* is organized as:

```
[RAW_ROOT]⊦---data
          ⊦---anci
          ∟---logs
```

Each component is expected to be cloned independently through *sparse checkouts*.

More information is available in the inner documentation of each component.

## Branches

**master**: Contains the code currently deployed.

**develop**: Contains the newly added features of the code still under evaluation phase.
