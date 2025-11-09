# This class will manage configuration settings for the tool
from dataclasses import dataclass

@dataclass(frozen=True)
class ConfigManager:
    target: str # mandatory!
    mode: str = "full" # defaults to "full"
    verbosity: int = 0
    silent: bool = False
    source: str = "all"
    keep_temp: bool = False