# Decompiles UTF files to XML and then back again for version control.
import concurrent.futures
import os
import subprocess
import time

from utils import *

utf_types = ".ale", ".txm", ".mat", ".utf"
utf_path = f"{root_copy_path}\\mod-assets\\DATA\\FX\\"
xml_path = f"{root_copy_path}\\mod-assets\\XML\\FX\\"

from concurrent.futures import ThreadPoolExecutor

#This uses brute force to convert UTF and XML because I couldn't be bothered to figure out queues.
def run_io_tasks_in_parallel(tasks):
    with ThreadPoolExecutor(max_workers=5000) as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        return running_tasks

def utf_to_xml_thread():
    for file in os.listdir(utf_path):
            if file.endswith(utf_types):
                yield lambda: subprocess.Popen(["build-tools\\UTFXML.exe", "-agi" ,"-o", xml_path, f"{utf_path}\\{file}"]).wait()

def xml_to_utf_thread():
    for file in os.listdir(xml_path):
            if file.endswith(".xml"):
                yield lambda: subprocess.Popen(["build-tools\\XMLUTF.exe", "-o", f"{utf_path}\\..", f"{xml_path}\\{file}"]).wait()

def utf_to_xml():
    utf_xml_start_time = time.perf_counter() 
    print(f"Converting UTF files at '{utf_path}' to XML format...")                         
    tasks = run_io_tasks_in_parallel(utf_to_xml_thread())
    results = [future.result() for future in concurrent.futures.as_completed(tasks)]
    utf_xml_end_time = time.perf_counter() 
    print(f"Converted UTF files at '{utf_path}' to XML in {utf_xml_end_time - utf_xml_start_time:0.4f} seconds")

def xml_to_utf():
    xml_utf_start_time = time.perf_counter() 
    print(f"Converting XML files at '{xml_path}' to UTF format...")                         
    tasks = run_io_tasks_in_parallel(xml_to_utf_thread())
    results = [future.result() for future in concurrent.futures.as_completed(tasks)]
    xml_utf_end_time = time.perf_counter() 
    print(f"Converted XML files at '{xml_path}' to UTF in {xml_utf_end_time - xml_utf_start_time:0.4f} seconds")