# Uses the 𝘞𝘪𝘯𝘥𝘰𝘸𝘴 𝘎𝘳𝘢𝘱𝘩𝘪𝘤𝘴 𝘋𝘦𝘷𝘪𝘤𝘦 𝘐𝘯𝘵𝘦𝘳𝘧𝘢𝘤𝘦 to determine the screen properties
# This gives us teh advantage of getting a full-screen pictures

import base64
import win32api
import win32con
import win32gui
import win32ui


def get_dimensions(): # Gets screen dimentions
    
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    
    return (width, height, left, top)


def screenshot(name='screenshot'):
    
    hdesktop = win32gui.GetDesktopWindow() # Get handle to the entire Desktop
    # Includes the entire viewable area across monitors ᕕ( ᐛ )ᕗ
    width, height, left, top = get_dimensions()
    
    desktop_dc = win32gui.GetWindowDC(hdesktop) # Create 𝘥𝘦𝘷𝘪𝘤𝘦 𝘤𝘰𝘯𝘵𝘦𝘯𝘹𝘵
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC() # 𝘔𝘦𝘮 𝘣𝘢𝘴𝘦𝘥 device context
    # Will store the bitmap until it is writen to a file

    screenshot = win32ui.CreateBitmap() # Create bitmap obj
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot) # Sets the mem_dc to point at the bitmap
    mem_dc.BitBlt((0,0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
    # Creates a 𝘣𝘪𝘵-𝘧𝘰𝘳-𝘣𝘪𝘵 𝘤𝘰𝘱𝘺 of the desktop img and stores it in the mem_dc
    screenshot.SaveBitmapFile(mem_dc, f'{name}.bmp') # Dump img to disk
    
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())


def run():
    screenshot()
    with open('screenshot.bmp', 'rb') as f:
        img = f.read()
    return img


if __name__ == '__main__':
    screenshot()

# 𝗧𝗲𝘀𝘁:
# 
# cd C:\User\Documents <to wherever the file is>
# python3 screenshotter.py 
# 
# Check for img in script folder
