# Since antiviruses started using Sandboxing to determine sus behaviour, we need to learn to avoid falling in a sandbox
# This, whether the sandbox runs on network perimeter, popular option, or directly on the target machine

from ctypes import byref, c_uint, c_ulong, sizeof, Structure, windll
import random
import sys
import time
import win32api
