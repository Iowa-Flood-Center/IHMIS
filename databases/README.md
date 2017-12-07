# Databases

This folder contains the scheme of different databases accessed by the system. Some of them (the smaller ones) have their content also stored.

## How to generate the backup of a scheme  

On *pgAdmin III*:

- *Right click* over the database name, then hit *Backup...*;
- In tab *File Options*:
  - Select as output filename: *schema.sql*;
  - Format: *Plain*;
  - Encoding: *UTF8*.
- In tab *Dump Options #1*:
  - Check *Type of Objects* > *Only schema*;
  - Check all on *Don't save*.
- In tab *Dump Options #2*:
  - Check *Include CREATE DATABASE statement*. 

## How to generate the backup of data content

```
TODO
```