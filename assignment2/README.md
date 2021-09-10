# Assignment 2
## move.sh

A small program which moves the contents of one folder to another, optionally filtered by filetype. If the destination folder doesn't exist, the program will offer to create it for you, with or without a timestamp.
```bash
./move.sh <source directory> <destination directory> <extension (optional)>
```
The extension argument lets you optionally only move files ending in i.e ".txt", ".dat".

## track.sh
To begin using the file, please run
```bash
source ./track.sh
```
the program can then be ran in the folliwng way
```
track <ARGUMENT>
```
where the folliwng are valid arguments
```
 start <LABEL>    Starts a new task with a label. Prints an error message if a task is already running" Example usage: start "having fun"
 stop             Stops the current task if one is running"
 status           Tells you which task is currently running, or if there is no active task."
 log              Lets you know how  much time you've spent on each completed task"
```
If no valid argument is supplied, a reminder of these will be given.
