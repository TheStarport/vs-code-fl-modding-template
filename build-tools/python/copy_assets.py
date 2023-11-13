# Sets the root copy path and copies assets over from the mod-assets folder to the install located at the FL_PATH variable location.
import distutils.dir_util
import time
from utils import *

fl_path = os.environ["FL_PATH"] 

def copy_files():
    print(bcolors.OKBLUE + f'Copying asset files from {root_copy_path}\\mod-assets to installation located at {fl_path}' + bcolors.ENDC)
    asset_copy_start_time = time.perf_counter() 
    distutils.dir_util.copy_tree(f'{root_copy_path}\\mod-assets\\EXE', f'{fl_path}')
    distutils.dir_util.copy_tree(f'{root_copy_path}\\mod-assets\\DATA', f'{fl_path}\\..\\DATA')
    distutils.dir_util.copy_tree(f'{root_copy_path}\\mod-assets\\DLLS', f'{fl_path}\\..\\DLLS')
    asset_copy_end_time = time.perf_counter() 
    print(bcolors.OKGREEN + f"Asset files copied over in {asset_copy_end_time - asset_copy_start_time:0.4f} seconds" + bcolors.ENDC)