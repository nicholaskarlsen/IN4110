#!/bin/bash

LOGFILE="~/.local/share/in4110_logfile.txt"


# Starts a new task with a label. Prints an error message if a task is already running
function __start() {
    # If the logfile doesn't exist yet, create it.
    if [ ! -f "$LOGFILE" ]
    then
        touch $LOGFILE
    fi

    if [ $(tail -1 $LOGFILE | cut -d " " -f1)=="LABEL" ]
    then
        echo "A task is already running"
    else
        echo $(date '+START %a %b %d %R %Z %Y') >> $LOGFILE
        echo "LABEL $1" >> $LOGFILE
    fi
}


# Stops the current task if one is running
function __stop() {
    if [ ! -f "$LOGFILE" ]
    then
        echo "Logfile $LOGFILE does not exist!"
        return 1
    fi

    if [ $(tail -1 $LOGFILE | cut -d " " -f1)=="LABEL" ]; then
        echo $(date '+END %a %b %d %R %Z %Y') >> $LOGFILE
    else
        echo "No task is currently active."
    fi
}


# Tells the user which task is currently running, or if there is no active task.
function __status() {
    if [ ! -f "$LOGFILE" ]
    then
        echo "Logfile $LOGFILE does not exist!"
        return 1
    fi

    # Check if the last line in the logfile starts with "LABEL" indicating that there is an active task
    if [ $(tail -1 $LOGFILE | cut -d " " -f1)=="LABEL" ]; then
        # If there is an active task, print its note
        echo Running task: $(tail -n 1 $LOGFILE | cut -d " " -f 2-) 
    else
        echo "No task is currently running."
    fi
}

function __log() {
    if [ ! -f "$LOGFILE" ]
    then
        echo "Logfile $LOGFILE does not exist!"
        return 1
    fi
}

function track() {
    case $1 in
        "start") 
            __start $2  
            ;;
        "stop") 
            __stop      
            ;;
        "status") 
            __status    
            ;; 
        "log") 
            __log       
            ;;
        *) 
            echo "Incorrect usage. Please supply one of the following arguments" 
            echo " start <LABEL>    Starts a new task with a label. Prints an error message if a task is already running"
            echo " stop             Stops the current task if one is running"
            echo " status           Tells you which task is currently running, or if there is no active task."
            echo " log              Lets you know how  much time you've spent on each completed task"
            ;;
    esac
}

