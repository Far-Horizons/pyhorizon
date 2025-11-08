# This class will manage configuration settings for the tool
from dataclasses import dataclass

@dataclass(frozen=True)
class ConfigManager:
    target: str # mandatory!
    silent: bool = False # default arg = False
    if silent: verbosity: int = -1
    else: verbosity: int = 0 # default arg = 0

