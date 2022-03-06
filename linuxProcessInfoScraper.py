#!usr/bin/python3

# Filename: m4p1.py
# Author: Mandeep Parihar
# Course: ITSC-204
# Details: A program that will parse all running processes and display status information for each of them.
# Resources: https://www.debuggex.com/cheatsheet/regex/python, https://docs.python.org/3/library/re.html,
    # https://man7.org/linux/man-pages/man5/procfs.5.html

import os
import binascii


# A class that is used for gathering status information on currently running Linux processes
class LinuxProcess:
    def __init__(self, name, state, pid, ppid, rss, rsslim, start_code, end_code, start_stack, start_data, end_data,
                 start_brk, arg_start, arg_end, env_start, env_end):
        self.name = name
        self.state = state
        self.pid = pid
        self.ppid = ppid
        self.rss = rss
        self.rsslim = rsslim
        self.start_code = start_code
        self.end_code = end_code
        self.start_stack = start_stack
        self.start_data = start_data
        self.end_data = end_data
        self.start_brk = start_brk
        self.arg_start = arg_start
        self.arg_end = arg_end
        self.env_start = env_start
        self.env_end = env_end

    def get_attr(self):
        return self.name, self.state, self.pid, self.ppid, self.rss, self.rsslim, self.start_code, self.end_code, \
               self.start_stack, self.start_data, self.end_data, self.start_brk, self.arg_start, self.arg_end, \
               self.env_start, self.env_end

    def set_attr(self, name, state, pid, ppid, rss, rsslim, start_code, end_code, start_stack, start_data, end_data,
                 start_brk, arg_start, arg_end, env_start, env_end):
        self.name = name
        self.state = state
        self.pid = pid
        self.ppid = ppid
        self.rss = rss
        self.rsslim = rsslim
        self.start_code = start_code
        self.end_code = end_code
        self.start_stack = start_stack
        self.start_data = start_data
        self.end_data = end_data
        self.start_brk = start_brk
        self.arg_start = arg_start
        self.arg_end = arg_end
        self.env_start = env_start
        self.env_end = env_end


# Function to format and print the gathered process information
def printer(name, state, pid, ppid, rss, rsslim, start_code, end_code, start_stack, start_data, end_data,
            start_brk, arg_start, arg_end, env_start, env_end):
    # Dictionary that uses the state as a key and the full state name as the value
    state_dict = {
        "R": "R\tRunning",
        "S": "S\tSleeping in an interruptible wait",
        "D": "D\tWaiting in uninterruptible disk sleep",
        "Z": "Z\tZombie",
        "T": "T\tStopped (on a signal)",
        "t": "t\tTracing stop",
        "W": "W\tPaging",
        "X": "X\tDead",
        "x": "x\tDead",
        "K": "K\tWakekill",
        "P": "P\tParked"
    }

    # Takes the single character state and assigns a variable to the full state name
    state_full = ""
    if state in state_dict:
        proc.state = state_dict.get(state)
        state_full = proc.state

    # I've learned that I really don't like formatting text in programming at all
    # I'm sorry it's so plain, but at least it's readable
    print("Process Name:", name, "\nState:", state_full, "\nPID:", pid, "\nPPID:", ppid,
          "\nRSS:", rss, "\nRSSLIM:", rsslim, "\nStart Code:", start_code,
          "\nEnd Code:", end_code, "\nStart Stack:", start_stack, "\nStart Data:", start_data,
          "\nEnd Data:", end_data, "\nStart Brk:", start_brk, "\nArg Start:", arg_start,
          "\nArg End:", arg_end, "\nEnvironment Start:", env_start, "\nEnvironment End:", env_end, "\n")


proc_increment = 0
# Gets a list of all process folders in the /proc folder by using the fact that they start with a digit
proc_ids = [proc_id for proc_id in os.listdir("/proc") if proc_id.isdigit()]
skip_flag = 0

# While there are still processes folders to read
while len(proc_ids):
    try:
        # Gets only the process number as a string
        proc = str(proc_ids[proc_increment])
    except IndexError:
        # If the process list has been iterated through, then return message and break loop
        print("\nAll processes have been traversed and detailed.")
        break

    # Opens process's status file from within the process's folder
    with open("/proc/" + proc + "/stat", "r") as reader:
        # Reads stat file of current process and converts contents into list for easier parsing
        stat_reader = reader.read()
        stat_reader_list = stat_reader.split(" ")

        # Collecting information from stat file into variables
        proc_name = stat_reader_list[1].strip("("). strip(")")
        proc_state = stat_reader_list[2]
        proc_pid = stat_reader_list[0]
        proc_ppid = stat_reader_list[3]
        proc_rss = stat_reader_list[23]
        proc_rsslim = stat_reader_list[24]
        proc_start_code = stat_reader_list[25]
        proc_end_code = stat_reader_list[26]
        proc_start_stack = stat_reader_list[27]
        proc_start_data = stat_reader_list[44]
        proc_end_data = stat_reader_list[45]
        proc_start_brk = stat_reader_list[46]
        proc_arg_start = stat_reader_list[47]
        proc_arg_end = stat_reader_list[48]
        proc_env_start = stat_reader_list[49]
        proc_env_end = stat_reader_list[50]

        proc = LinuxProcess(proc_name, proc_state, proc_pid, proc_ppid, proc_rss, proc_rsslim, proc_start_code,
                            proc_end_code, proc_start_stack, proc_start_data, proc_end_data, proc_start_brk,
                            proc_arg_start, proc_arg_start, proc_env_start, proc_env_end)

        # Set attributes of current process
        proc.set_attr(proc_name, proc_state, proc_pid, proc_ppid, proc_rss, proc_rsslim, proc_start_code,
                      proc_end_code, proc_start_stack, proc_start_data, proc_end_data, proc_start_brk,
                      proc_arg_start, proc_arg_start, proc_env_start, proc_env_end)

        # Call printer function to print and display all current process information
        printer(proc_name, proc_state, proc_pid, proc_ppid, proc_rss, proc_rsslim, proc_start_code,
                proc_end_code, proc_start_stack, proc_start_data, proc_end_data, proc_start_brk,
                proc_arg_start, proc_arg_start, proc_env_start, proc_env_end)

        proc_increment += 1

    # This code block exists in the while loop after closing the file stream
    if skip_flag == 0:
        user_input = str(input("Display a specific attribute? [Y/N] "))

        if user_input == "Y" or user_input == "y":
            attr_select = str(input("Which attribute do you wish to see?\n"
                                    "Available: [Name, State, PID, PPID, RSS, RSSLIM, Start code, End code, "
                                    "Start stack, Start data, End data, Start Brk, Arg start, Arg end, "
                                    "ENV start, ENV end]\n"))

            # I, regrettably, didn't consider making this simpler until I was already too far in
            # .lower() would have saved me a lot of copy/paste work
            if attr_select == "name" or attr_select == "Name":
                print("Current process name is:", proc.name, "\n")
            elif attr_select == "state" or attr_select == "State":
                print("Current process state is:", proc.state, "\n")
            elif attr_select == "pid" or attr_select == "PID" or attr_select == "Pid":
                print("Current process PID is:", proc.pid, "\n")
            elif attr_select == "ppid" or attr_select == "PPID" or attr_select == "Ppid":
                print("Current process PPID is:", proc.ppid, "\n")
            elif attr_select == "rss" or attr_select == "RSS" or attr_select == "Rss":
                print("Current process RSS is:", proc.rss, "\n")
            elif attr_select == "rsslim" or attr_select == "RSSLIM" or attr_select == "Rsslim":
                print("Current process RSSLIM is:", proc.rsslim, "\n")
            elif attr_select == "start code" or attr_select == "Start Code" or attr_select == "Start code" or attr_select == "END CODE":
                print("Current process start code is:", proc.start_code, "\n")
            elif attr_select == "end code" or attr_select == "End Code" or attr_select == "End code" or attr_select == "END CODE":
                print("Current process end code is:", proc.state, "\n")
            elif attr_select == "start stack" or attr_select == "Start Stack" or attr_select == "Start stack" or attr_select == "START STACK":
                print("Current process start stack is:", proc.start_stack, "\n")
            elif attr_select == "start data" or attr_select == "Start Data" or attr_select == "Start data" or attr_select == "START DATA":
                print("Current process start data is:", proc.start_data, "\n")
            elif attr_select == "end data" or attr_select == "End Data" or attr_select == "end data" or attr_select == "END DATA":
                print("Current process end data is:", proc.end_data, "\n")
            elif attr_select == "start brk" or attr_select == "Start BRK" or attr_select == "Start Brk" or attr_select == "START BRK":
                print("Current process start brk is:", proc.start_brk, "\n")
            elif attr_select == "arg start" or attr_select == "Arg Start " or attr_select == "Arg start" or attr_select == "ARG START":
                print("Current process argument start is:", proc.arg_start, "\n")
            elif attr_select == "arg end" or attr_select == "Arg End " or attr_select == "Arg end" or attr_select == "ARG END":
                print("Current process argument end is:", proc.arg_end, "\n")
            elif attr_select == "env start" or attr_select == "Env Start " or attr_select == "Env start" or attr_select == "ENV START":
                print("Current process environment start is:", proc.env_start, "\n")
            elif attr_select == "env end" or attr_select == "Env End " or attr_select == "Env end" or attr_select == "ENV END":
                print("Current process environment end is:", proc.env_end, "\n")
            else:
                print("Invalid entry made.")
        elif user_input == "N" or user_input == "n":
            skip_all_input = str(input("Do you wish to skip all further prompts and only see the standard process printout? [Y/N] "))

            if skip_all_input == "Y" or skip_all_input == "y":
                skip_flag = 1
