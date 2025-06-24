# Uses the 𝘞𝘪𝘯𝘥𝘰𝘸𝘴 𝘎𝘳𝘢𝘱𝘩𝘪𝘤𝘴 𝘋𝘦𝘷𝘪𝘤𝘦 𝘐𝘯𝘵𝘦𝘳𝘧𝘢𝘤𝘦 to determine the screen properties
# This gives us teh advantage of getting a full-screen pictures

import base64
import win32api
import win32con
import win32gui
import win32ui

def get_dimensions():
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    return (width, height, left, top)

 