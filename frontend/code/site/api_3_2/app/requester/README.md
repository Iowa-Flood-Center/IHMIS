# Frontend - Site - API - App - Requester

This is the server-side sub-component of the *Runset Requester* tool.

A *Runset Request* is currently defined as an "incomplete" *Runset Result* - i. e., a folder-structured set of files.

In the particular case of the *Runset Request*, the set of files presents the basic structure:   


    [ROOT]⊦---metafiles_sandbox/
          ∣    ⊦---cross_matrices/
          ∣    ∣    ⊦---Comparison_matrix.json
          ∣    ∣    ∟---Evaluation_matrix.json
          ∣    ⊦---sc_modelcombinations/
          ∣    ⊦---sc_models/
          ∣    ∣    ⊦---<MDL_N_id>.gbl
          ∣    ∣    ∟---<MDL_N_id>prevqpe.gbl
          ∣    ∟---sc_runset/
          ∣    ∣    ∟---Runset.gbl
          ⊦---outputs/
          ∣    ∟---<MDL_N_id>/
          ∟-email.txt
          ⊦-<MDL_N_id>.gbl
          ∟-<RST_id>.gbl

where:

- ```<MDL_N_id>``` is the *model id* for the *Nth* model in the Runset;
- ```<RST_id>``` is the *Runset id* of the Runset.

After created, the hierarchy of folders and files is compressed into a file named ```<TIMESTAMP>.zip```, with ```<TIMESTAMP>``` as the epoch timestamp, in milliseconds, of the creation of *Runset Request*. If it is specified that the model execution is expected, that a copy of such file is copied to the ```waiting_room``` folder still in the *Frontend*.