## Setup

- Download and install [Visual Studio Code](https://code.visualstudio.com).
- Download and install the latest version of (Python)[https://www.python.org/downloads/].
- Launch VS Code and install the Python Extension from Microsoft.
- Clone and then copy this repository to the location of your choice. The folder structure and included files are set up with git in mind. 
- Open a terminal window in Visual Studio Code and run `pip install -r requirements.txt`.
- You're ready to go! See below for usage.
- (Optional) A number of demo and placeholder files can be found in the `mod-assets` directory. You may wish to remove them before proceeding.

## Usage

The intended workflow for this script is to have an installation of vanilla Freelancer set up somewhere that this script copies files over to. Using utf.py, the script allows for proper version control and tracking of infocard .dlls and many Freelancer .utf files that are usually compiled binary by compiling them to binary and copying them over at runtime. The script also tails the game's log into the Visual Studio Code console window, and attempts to fetch relevant information when Freelancer.exe crashes unexpectedly.

Once set up in Visual Studio Code, you can start the script by using the 'Start Debugging' option under 'Run' (F5). You can adjust how much the script actually does on run by adding and removing arguments in launch.json. Arguments are as follows:

- `--no_start`: Don't run the game after running the build script section of the script.
- `--no_copy`: Don't copy any files from mod-assets over to the location specified by the `FL_PATH` environment variable.
- `--skip_checks`: Don't validate FL_PATH or check for existing Freelancer processes before proceeding with the copy action. This may cause errors depending on how your environment has been configured.
- `--ignore_xml`: Don't convert any UTF files into XML. If your mod has a lot of UTF files, using this option can save a substantial amount of build time.
- `--ignore_utf`: Don't convert any XML files into UTF. If you're not building UTFs from XML source using this option can save a substantial amount of build time.
- `--ignore_infocards`: Don't build any infocards from infocard_imports.frc. This is unlikely to save much time, but if you're not working with custom strings there isn't much point in using the infocard module.

Log tailing is set up to work with the default FLSpew.txt location. If your mod moves FLSpew, you'll need to adjust the `flspew_log_path` variable in freelancer.py. Crash handling will attempt to correlate the offset and module from a crash with [the list on the Starport KnowledgeBase](https://wiki.the-starport.net/wiki/fl-binaries/crash-offsets), but will fall back to a local file included with this repository if it's unable to reach the remote site.

## Credit

- Many thanks to Adoxa and Sir Lancelot for creating the [Freelancer XML Project](http://adoxa.altervista.org/freelancer/tools.html#xmlproject), and [Freelancer Resource Compiler](http://adoxa.altervista.org/freelancer/tools.html#frc), which this set of scripts uses to handle .utf files and infocards respectively.

- Huge thanks to [Laz](https://github.com/orgs/TheStarport/people/Lazrius) for helping write the original PowerShell scripts this project started as, and also in translating them to Python.