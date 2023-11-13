import argparse
import time

from checks import *
from copy_assets import *
from freelancer import *
from infocards import *
from utf import *
from utils import *

parser = argparse.ArgumentParser()
parser.add_argument("--no_start", help="Runs the script but does not start Freelancer.exe on finish.", action="store_true")
parser.add_argument("--no_copy", help="Runs the script but does not copy files.", action="store_true")
parser.add_argument("--skip_checks", help="Skips validation and checking stages.", action="store_true")
parser.add_argument("--ignore_xml", help="Skips the conversion of XML into UTF.", action="store_true")
parser.add_argument("--ignore_utf", help="Skips the conversion of UTF into XML.", action="store_true")
parser.add_argument("--ignore_infocards", help="Skips the compiling of infocards from infocard_imports.frc", action="store_true")

args = parser.parse_args()

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(bcolors.HEADER + f"Starting build and copy script at {current_time}" + bcolors.ENDC)
build_script_start_time = time.perf_counter() 

if not args.skip_checks:
    validate_path()
else:
    print(bcolors.WARNING + "Warning, checks have been disabled. You may experience errors if the the FL_PATH environment variable has not been set" + bcolors.ENDC)

if not args.ignore_infocards:
    compile_infocards()

if not args.ignore_utf:
    utf_to_xml()

if not args.ignore_xml:
    xml_to_utf()

if not args.skip_checks:
    validate_process_stopped()
else:
    print(bcolors.WARNING + "Warning, checks have been disabled. You may experience copy errors if any instances of Freelancer are still running" + bcolors.ENDC)

if not args.no_copy:
    copy_files()

build_script_end_time = time.perf_counter() 
print(bcolors.HEADER + f"Build script completed in {build_script_end_time - build_script_start_time:0.4f} seconds" + bcolors.ENDC)

if not args.no_start:
    start_freelancer_main()