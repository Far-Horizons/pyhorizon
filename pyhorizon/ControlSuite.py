# This class will control the overall flow of the tool
from ArgManager import ArgManager
from ConfigManager import ConfigManager
from SubdomainEnumerator import SubdomainEnumerator

class ControlSuite:
    def __init__(self):
        args = ArgManager().parser.parse_args()
        self.config = ConfigManager(
            target = args.target,
            verbosity = args.verbosity,
            silent = args.silent
        )
        
    def run(self):
        try:
            self.run_SubdomainEnumerator()
        except Exception as e:
            print(f"An error occurred: {e}")

    def run_SubdomainEnumerator(self):
        SubdomainEnumerator(self.config).run()