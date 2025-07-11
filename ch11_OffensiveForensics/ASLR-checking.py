from typing import Callable, List

from volatility.framework import constants, exceptions, interfaces, renderers
from volatility.framework.configuration import requirements
from volatility.framework.renderers import format_hints
from volatility.framework.symbols import intermed
from volatility.framework.symbols.windows import extensions
from volatility.plugins.windows import pslist

import io
import logging
import os
import pefile

vollog = logging.getLogger(__name__)

IMAGE_DLL_CHARACTERISTICS_DYNAMIC_BASE = 0x0040
IMAGE_FILE_RELOCS_STRIPPED = 0x0001

def check_aslr(pe): # pass pe to check_asrl
    # parse pe
    pe.parse_data_directories([pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_LOAD_CONFIG']])
    dynamic = False
    stripped = False
    
    if (pe.OPTIONAL_HEADER.DllCharacteristics & IMAGE_DLL_CHARACTERISTICS_DYNAMIC_BASE):
        dynamic = True # Check if compiled with dynamic base setting
    if (pe.FILE_HEADER.Characteristics & IMAGE_FILE_RELOCS_STRIPPED):
        stripped = True # Check if relocation data has been stripped out
    if not dynamic or (dynamic and stripped):
        aslr = False # if NOT dynamic, or dynamic and stripped, then no ASLR
    else:
        aslr = True
    return aslr

class AslrCheck(interfaces.plugins.PluginInterface):
# Inherits from from the PlugInInterface obj
    @classmethod
    def get_requirements(cls):
       # Define requirements
        return [
            requirements.TranslationLayerRequirement( # Mem layer requirement
                name='primary', description='Memory layer for the kernel',
                architectures=["Intel32", "Intel64"]),

            requirements.SymbolTableRequirement( # Symbols table
                name="nt_symbols", description="Windows kernel symbols"),
                
            requirements.PluginRequirement( # Get all process from memory dump to create PE file
                name='pslist', plugin=pslist.PsList, version=(1, 0, 0)),
            
            requirements.ListRequirement( # Pass a list for pIDs, limiting the check to those processes
                name = 'pid', 
                element_type = int,  description = "Process ID to include (all other processes are excluded)",
                optional = True),
            ]
