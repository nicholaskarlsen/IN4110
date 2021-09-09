#!/bin/bash

LOGFILE=~/.local/share/in4110_logfile.txt


# Starts a new task with a label. Prints an error message if a task is already running
function __start() {
    if [ ! -f "$LOGFILE" ]
    then 
        touch $LOGFILE
    fi

    case $(tail -1 $LOGFILE | cut -d " " -f1) in
        "LABEL" ) 
            echo "A task is already running"
            ;;
        * ) 
            echo "START $(date)" >> $LOGFILE
            echo "LABEL $1" >> $LOGFILE
            ;;
    esac
}


# Stops the current task if one is running
function __stop() {
    if [ ! -f "$LOGFILE" ]
    then
        echo "Logfile $LOGFILE does not exist!"
        return 1
    fi

    case $(tail -1 $LOGFILE | cut -d " " -f1) in
        "LABEL" )
            echo "STOP $(date)" >> $LOGFILE
            ;;
        * ) 
            echo "No task is currently active."
            ;;
    esac
}


# Tells the user which task is currently running, or if there is no active task.
function __status() {
    if [ ! -f "$LOGFILE" ]
    then
        echo "Logfile $LOGFILE does not exist!"
        return 1
    fi

    case $(tail -1 $LOGFILE | cut -d " " -f1) in
        "LABEL" )
            echo Running task: $(tail -n 1 $LOGFILE | cut -d " " -f 2-) 
            ;;
        * ) 
            echo "No task is currently running"
            ;;
    esac
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

