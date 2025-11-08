# This class will control the argument parsing for the pyhorizon tool
import argparse

class ArgManager:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="pyhorizon - A recon tool by Horizon")
        self._configure_arguments()

    # Define the arguments here
    def _configure_arguments(self):
        self.parser.add_argument( #set the target domain
            "-t", "--target",
            required=True,
            help="Target domain for subdomain enumeration"
        )

        self.parser.add_argument( #set the verbosity level, -1 for silent mode
            "-v", "--verbosity",
            default=0,
            type=int,
            help = "set the verbosity level, 0 (default) is the default verbosity, 2 is the most verbose, and -1 is silent mode"
        )

        self.parser.add_argument( #set silent mode
            "-s", "--silent",
            default=False,
            action="store_true",
            help="Run in silent mode, which gives no output to the console (this is the same as setting verbosity to -1)"
        )