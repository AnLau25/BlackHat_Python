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
    
    @classmethod # handles the optional pIDs, checking wich ones are in the list
    def create_pid_filter(cls, pid_list: List[int] = None) -> Callable[[interfaces.objects.ObjectInterface], bool]:
        filter_func = lambda _: False
        pid_list = pid_list or []
        filter_list = [x for x in pid_list if x is not None]
        if filter_list:
            filter_func = lambda x: x.UniqueProcessId not in filter_list
        return filter_func

    def _generator(self, procs):
        # Structure where we store the Proces Env. Block(PEB) of each proc
        pe_table_name = intermed.IntermediateSymbolTable.create(
            self.context, 
            self.config_path,
            "windows", 
            "pe", 
            class_types=extensions.pe.class_types)

        procnames = list()
        for proc in procs:
            procname = proc.ImageFileName.cast("string", max_length=proc.ImageFileName.vol.count, errors='replace')
            if procname in procnames:
                continue
            procnames.append(procname)

            proc_id = "Unknown"
            try:
                proc_id = proc.UniqueProcessId
                proc_layer_name = proc.add_process_layer()
            except exceptions.InvalidAddressException as e:
                vollog.error(f"Process {proc_id}: invalid address {e} in layer {e.layer_name}")
                continue

            peb = self.context.object( # create peb obj
                    self.config['nt_symbols'] + constants.BANG + "_PEB",
                    layer_name = proc_layer_name,
                    offset = proc.Peb)
           
            try:
                dos_header = self.context.object(
                        pe_table_name + constants.BANG + "_IMAGE_DOS_HEADER",
                        offset=peb.ImageBaseAddress, 
                        layer_name=proc_layer_name)
            except Exception as e:
                continue

            pe_data = io.BytesIO()
            for offset, data in dos_header.reconstruct():
                pe_data.seek(offset)
                pe_data.write(data)
            pe_data_raw = pe_data.getvalue()
            # The retreived PEB gets stored into a file
            # As it is the intel src of a proc
            pe_data.close()

            try:
                pe = pefile.PE(data=pe_data_raw)
            except Exception as e:
                continue
            
            # Result of trating 𝘱𝘦𝘣 goes into check_asrl as pe
            aslr = check_aslr(pe)

            # Yield tupple result containing pID, proc name, proc mem addr and bool return of ASRL 
            yield (0, (proc_id, 
                        procname, 
                        format_hints.Hex(pe.OPTIONAL_HEADER.ImageBase),
                        aslr,
                        ))
            
    def run(self):
        # use 𝘱𝘭𝘪𝘴𝘵 plug in to get proc list
        procs = pslist.PsList.list_processes(self.context, 
                                             self.config["primary"], 
                                             self.config["nt_symbols"],
                                             filter_func = self.create_pid_filter(self.config.get('pid', None)))
        # return results ussing the 𝘛𝘳𝘦𝘦𝘎𝘳𝘪𝘥 renderer, so each proc output show in one line
        return renderers.TreeGrid([
            ("PID", int), 
            ("Filename", str), 
            ("Base", format_hints.Hex), 
            ("ASLR", bool)],
            self._generator(procs))