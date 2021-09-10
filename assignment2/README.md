# Assignment 2
## move.sh
A small program which moves the contents of one folder to another, optionally filtered by filetype. If the destination folder doesn't exist, the program will offer to create it for you, with or without a timestamp.
The program is used in the following way
```bash
bash move.sh <source directory> <destination directory> <extension (optional)>
```
The extension argument lets you optionally only move files ending in i.e ".txt", ".dat".

## track.sh
A simple program which lets you track when you start and stop a task, but please not that the program will only track a single task at the time. The program can also report the time you spent on each task.
To begin using the program, please run
```bash
source ./track.sh
```
the program can then be ran in the folliwng way
```bash
track <ARGUMENT>
```
where the folliwng are valid arguments
```
 start <LABEL>    Starts a new task with a label. Prints an error message if a task is already running" Example usage: start "having fun"
 stop             Stops the current task if one is running"
 status           Tells you which task is currently running, or if there is no active task."
 log              Lets you know how  much time you've spent on each completed task"
```
If no valid argument is supplied to the program, a reminder of these will be given.
