#!/bin/bash

LOGFILE=~/.local/share/in4110_logfile.txt

# Note: functions prefixed with __ are assumed to be private. User not expected to call them directly.

# Starts a new task with a label. Prints an error message if a task is already running
function __start() {
    # Create an empty logfile if none exists (else tail command below throws an error)
    if [ ! -f "$LOGFILE" ]
    then 
        touch $LOGFILE
    fi
    # Fetch the first word of the current last line in the LOGFILE
    case $(tail -1 $LOGFILE | cut -d " " -f1) in
        "LABEL" ) 
            echo "A task is already running"
            ;;
        * ) 
            echo "START $(date)" >> $LOGFILE
            args=("$@")
            echo "LABEL ${args[*]}" >> $LOGFILE
            ;;
    esac
}


# Stops the current task if one is running
function __stop() {
    # Ensure that the logfile exists, if not, exit.
    if [ ! -f "$LOGFILE" ]
    then
        echo "Logfile $LOGFILE does not exist!"
        return 1
    fi
    # Fetch the first word of the current last line in the LOGFILE
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
    # Ensure that the logfile exists, if not, exit.
    if [ ! -f "$LOGFILE" ]
    then
        echo "Logfile $LOGFILE does not exist!"
        return 1
    fi
    # Fetch the first word of the current last line in the LOGFILE
    case $(tail -1 $LOGFILE | cut -d " " -f1) in
        "LABEL" )
            echo Running task: $(tail -n 1 $LOGFILE | cut -d " " -f 2-) 
            ;;
        * ) 
            echo "No task is currently running"
            ;;
    esac
}

# Command that displays the time spend on each task.
function __log() {
    # Ensure that the logfile exists, if not, exit.
    if [ ! -f "$LOGFILE" ]
    then
        echo "Logfile $LOGFILE does not exist!"
        return 1
    fi
    # Loop through the number of completed tasks
    N_COMPLETED=$(grep 'STOP' $LOGFILE | wc -l)
    for i in $(seq 1 $N_COMPLETED)
    do
        # "Clever way" of preparing the correct argument to pass to sed
        arg=$i
        arg+=p
        # Grep the i-th line containing the word "START" then remove the "START", leaving only the timestamp 
        START_T="$(grep 'START' $LOGFILE | sed -n $arg | cut -d " " -f 2-)" 
        STOP_T="$(grep 'STOP' $LOGFILE | sed -n $arg | cut -d " " -f 2-)" 
        # Convert the timestamps into seconds
        t1=$(date -d "$START_T" '+%s')
        t2=$(date -d "$STOP_T" '+%s')
        # Use date to format the time difference in HH:MM:SS
        echo "$(date -u -d @"$(($t2-$t1))" +"Task $i: %-T")"
    done
}

# Main function of the program. User is only ever expected to call this one directly.
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
            echo "  start \"<Task Label>\"     Starts a new task with a label. Prints an error message if a task is already running"
            echo "  stop                     Stops the current task if one is running"
            echo "  status                   Tells you which task is currently running, or if there is no active task."
            echo "  log                      Lets you know how  much time you've spent on each completed task"
            ;;
    esac
}

