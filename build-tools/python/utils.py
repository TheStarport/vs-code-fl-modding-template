import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#root_copy_path = {os.path.dirname(os.path.realpath(__file__))}
root_copy_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..\\..'))
fl_path = os.environ["FL_PATH"]
trailing_references = False
freelancer_name = "Freelancer.exe"
freelancer_pid = 0
fl_running_start_time = 0
stop_threads = False
tail_flspew = True