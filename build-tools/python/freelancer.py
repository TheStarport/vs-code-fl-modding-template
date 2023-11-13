# Starts Freelancer from FL_PATH and tails FLSpew. Terminates the process when 'Trailing References' are detected and pipes the crash offset into the console if the game closes unexpectedly
import json
import os
import pythoncom
import threading
import time
import urllib.request, json
import win32evtlog
import wmi

from utils import *
    
flspew_log_path = f"{os.getenv('LOCALAPPDATA')}\\Freelancer\\FLSpew.txt"

def start_freelancer():    
    print(bcolors.OKBLUE + f"Starting Freelancer in windowed mode..." + bcolors.ENDC)
    from subprocess import Popen
    Popen([f"{fl_path}\\Freelancer.exe", "-w"])
    global fl_running_start_time 
    fl_running_start_time = time.perf_counter() 
    
    # Initializes COM interface to make use of Windows API threading
    pythoncom.CoInitialize()
    wmiC = wmi.WMI()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    for process in wmiC.Win32_Process():
        if "freelancer" in process.Name.lower():
            global freelancer_pid 
            freelancer_pid = process.ProcessId
            global freelancer_name 
            freelancer_name = process.Name
            print(bcolors.OKGREEN + f"Started {freelancer_name}, PID {freelancer_pid} at at {current_time}" + bcolors.ENDC)

    def follow(file):
        # Seek the end of the file
        file.seek(0)
        # Start infinite loop
        while True:
            global stop_threads
            if stop_threads is True:
                raise SystemExit
            # Read the whole file
            line = file.readline()
            # Sleep if file hasn't been updated
            if not line:
                time.sleep(0.5)
                continue
        
            if "DEBUG" in line:
                line = bcolors.OKCYAN + line + bcolors.ENDC

            if "WARNING" in line:
                line = bcolors.WARNING + line + bcolors.ENDC

            if "Failed" in line:
                line = bcolors.WARNING + line + bcolors.ENDC

            if "failed" in line:
                line = bcolors.WARNING + line + bcolors.ENDC

            if "ERROR" in line:
                line = bcolors.FAIL + line + bcolors.ENDC

            if "E:\\FL\\Scratch\\Source\\DALib\\DALib.cpp(376) : WARNING:General:******* DA SYSTEM: trailing references *******" in line:
                yield line
                global trailing_references
                trailing_references = True
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                fl_running_end_time = time.perf_counter() 
                print(bcolors.HEADER + f"Stopping {freelancer_name}, PID {freelancer_pid} at {current_time} gracefully, the application has been running for {fl_running_end_time - fl_running_start_time:0.4f} seconds" + bcolors.ENDC)
                os.system(f"taskkill /F /PID {freelancer_pid}")
                stop_threads = True
                raise SystemExit
            yield line

    if tail_flspew == True:
        
        log_file = open(f"{flspew_log_path}")
        log_lines = follow(log_file)
        # Iterate over the generator
        for line in log_lines:
            print(line, end='')

# This function grabs the latest Freelancer crash event it can find that matches the PID of the tailed and launched thread. It's possible that this might grab a duplicate PID, but it works through the first 100 events and will grab the latest one with a PID matching the freelancer_pid variable so the chances of it grabbing the wrong one are pretty slim.
def fetch_crash_offset():
    global stop_threads
    server = 'localhost'
    logtype = 'Application'
    hex_pid = hex(freelancer_pid).lstrip("0x")
    hand = win32evtlog.OpenEventLog(server,logtype)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    iterate = 0
    data = False
    while iterate < 100:
        events = win32evtlog.ReadEventLog(hand, flags,0)
        iterate =  iterate + 1
        if events:
            for event in events:           
                    if event.EventID == 1000 and "Freelancer.exe" and f"{hex_pid}" in event.StringInserts:
                        data = event.StringInserts
                        iterate = 101
                        break

    if data:
        print('Time Generated:', event.TimeGenerated)
        print('Source Name:', event.SourceName)
        print('Event ID:', event.EventID)
        print(f'Exception Code: 0x{data[6]}')
        print(f'Faulting Application Name: {data[0]}, version {data[1]}, PID {int(data[8], 16)}')
        print(f'Faulting Application Path: {data[10]}')
        print(bcolors.BOLD + f'Faulting Module Name: {data[3]}, version {data[4]}' + bcolors.ENDC)
        print(f'Faulting Module Path: {data[11]}')
        print(bcolors.BOLD + f'Fault Offset: 0x{data[7]}' + bcolors.ENDC)                            

        full_offset = "0x" + data[7].lower()
        faulting_module = data[3].lower()

        try:
            print(bcolors.HEADER + "Attempting to fetch JSON crash information from the Starport KnowledgeBase..." + bcolors.ENDC)
            with urllib.request.urlopen("https://raw.githubusercontent.com/TheStarport/KnowledgeBase/master/static/payloads/crash-offsets.json") as url:
                crash_data = json.load(url)
        except:
            print(bcolors.FAIL + "Unable to reach the Starport Knowledgebase, Falling back on local file..." + bcolors.ENDC)
            file = open('crash_offsets.json')
            crash_data = json.load(file)

        for r in crash_data:
            if (r["offset"].lower() == full_offset) and (r["moduleName"].lower() == faulting_module):
                print(bcolors.OKBLUE + f"Offset Description: {r['description']}" + bcolors.ENDC)
                print(bcolors.OKBLUE + f"Found By: {r['author']}" + bcolors.ENDC)
                from datetime import datetime
                print(bcolors.OKBLUE + f"Date Added: {datetime.fromtimestamp(r['dateAdded'])}" + bcolors.ENDC)
                print(bcolors.FAIL + 'For further debugging, please reference the fault offset and faulting module name against https://wiki.the-starport.net/wiki/fl-binaries/crash-offsets' + bcolors.ENDC)
                stop_threads = True 
                raise SystemExit
            
        print(bcolors.FAIL + f"No crash offset at {full_offset} in {faulting_module} has been documented previously. Please determine the cause of the crash and submit an update to the Starport KnowledgeBase" + bcolors.ENDC)
        stop_threads = True    
        raise SystemExit
        
    else:
        print(bcolors.FAIL + f"No crash offset corresponding to PID {freelancer_pid} was found. It\'s likely the Freelancer process was killed manually, or something else unusual has happened. Please check your Windows Application logs if it's not clear what killed the process in this instance." + bcolors.ENDC)
        stop_threads = True    
        raise SystemExit

def crash_check():
    global stop_threads
    pythoncom.CoInitialize()
    wmiC = wmi.WMI()
    while True:
        found_freelancer = False
        time.sleep(1)
        for process in wmiC.Win32_Process():
            if process.ProcessId == freelancer_pid:
                found_freelancer = True
                break
        if found_freelancer is True:
            continue
        global trailing_references
        if trailing_references != True and found_freelancer is False:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            fl_running_end_time = time.perf_counter() 
            print(bcolors.FAIL + f"{freelancer_name}, PID {freelancer_pid} has stopped unexpectedly at {current_time} after running for {fl_running_end_time - fl_running_start_time:0.4f} seconds. Fetching crash event from Application logs... " + bcolors.ENDC)
            fetch_crash_offset()
            stop_threads = True
            raise SystemExit
        if trailing_references is True:
            stop_threads = True
            raise SystemExit
        if stop_threads is True:
            raise SystemExit

def start_freelancer_main():
    fl_tailed_process = threading.Thread(target=start_freelancer)
    fl_tailed_process.start()
    fl_crash_handler = threading.Thread(target=crash_check)
    fl_crash_handler.start()