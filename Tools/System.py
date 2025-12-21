from langchain.tools import tool
from langchain_community.tools.file_management import (
    ReadFileTool, WriteFileTool, ListDirectoryTool,
    CopyFileTool, DeleteFileTool, FileSearchTool,
    MoveFileTool
)
import os
from PIL import Image
import mss
import mss.tools
import pygetwindow as gw
import platform
import base64

@tool
def get_current_directory():
    """
    Get the current working directory.
    :return:
    str: The current working directory.
    """
    return os.getcwd()

@tool
def get_current_date():
    """
    Get the current date.
    :return:
    str: The current date in YYYY-MM-DD format.
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")

@tool
def get_current_time():
    """
    Get the current time.
    :return:
    str: The current time in HH:MM:SS format.
    """
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

read_file = ReadFileTool()

write_file = WriteFileTool()

list_directory = ListDirectoryTool()

copy_file = CopyFileTool()

delete_file = DeleteFileTool()

file_search = FileSearchTool()

move_file = MoveFileTool()

@tool
def read_file_binary(
        file_path: str,
        offset: int = 0,
        length: int = -1
) -> bytes:
    """
    Read binary data from a specified location in a file.

    :param file_path: File path.
    :param offset: Offset to start(in bytes), calculated from the beginning of the file
    :param length: The length of bytes to read, -1 means the whole file

    :return: Binary data of the specified range
    """
    try:
        with open(file_path, 'rb') as f:
            f.seek(offset)  # move ptr to specified location
            binary_data = f.read(length)  # read data in specified range
        return binary_data
    except Exception as e:
        raise Exception(f"Failed to read data from the specified range：{str(e)}")

@tool
def read_image_file_as_base64(
        file_path: str,
        offset: int = 0,
        length: int = -1,
        add_prefix: bool = True
) -> str:
    """
    Read data from specified location in an image file and encode into base64 data.
    :param file_path: File path.
    :param offset: Offset to start(in bytes), calculated from the beginning of the file
    :param length: The length of bytes to read, -1 means the whole file
    :param add_prefix: Whether to add the data URI prefix.
    :return: Base64 encoded string.
    """
    try:
        with open(file_path, 'rb') as f:
            f.seek(offset)  # move ptr to specified location
            binary_data = f.read(length)  # read data in specified range
            encoded_data = base64.b64encode(binary_data).decode('utf-8')
            if add_prefix:
                return f"data:image/{format};base64,{encoded_data}"
            return encoded_data
    except Exception as e:
        raise Exception(f"Failed to read data from the specified range：{str(e)}")


@tool
def take_screenshot(
        save_path: str,
        region: tuple = None,  # (x0, y0, x1, y1)
        window_title: str = None,  # specific window title to capture, high priority than region
        quality: int = 95  # quality from 1 to 100
) -> str:
    """
    Take a screenshot and save it to the specified path.
    :param save_path: The path to save the screenshot, e.g. ./Temp/screenshot_name.png, better to use this relative path. Support .png, .jpg, jpeg, .bmp formats.
    :param region: The region to capture (x0, y0, x1, y1). If None, capture the full screen or specific window if window_title is provided.
    :param window_title: The title of the window to capture. If provided, captures this window instead of full screen or region. If None, captures full screen or region.
    :param quality: The quality of the saved image (1-100), only effective for JPEG or JPG format.
    :return: The path where the screenshot is saved or an error message whit Error begin.
    """
    # validate save path is valid
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    if not save_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
        save_path += ".png"  # default to .png if no valid extension provided

    # specific window capture, the highest priority
    if window_title:
        screenshot_path = _capture_window(window_title, save_path, quality)
        if screenshot_path:
            return screenshot_path
        return f"Error: Window with title '{window_title}' not found."

    # specific region or full screen capture
    with mss.mss() as sct:
        # get the region to capture
        if region:
            # transfer format to mss format：{"left": x1, "top": y1, "width": x2-x1, "height": y2-y1}
            monitor = {
                "left": region[0],
                "top": region[1],
                "width": region[2] - region[0],
                "height": region[3] - region[1]
            }
        else:
            monitor = sct.monitors[1]  # 1=main monitor, 0=all monitors

        # capture the screen
        sct_img = sct.grab(monitor)
        # convert to PIL image and save
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        # save pic (distinguish jpg/jpeg quality setting)
        if save_path.lower().endswith((".jpg", ".jpeg")):
            img.save(save_path, quality=quality)
        else:
            img.save(save_path)

    print(f"screenshot save：{save_path}")
    return save_path

def _capture_window(window_title: str, save_path: str, quality: int) -> str:
    """internal function to capture a specific window by title"""
    system = platform.system()
    try:
        # Windows specific implementation
        if system == "Windows":
            # verbally get window by title
            windows = gw.getWindowsWithTitle(window_title)
            if not windows:
                return None
            win = windows[0]
            # make window active
            win.activate()
            # get window region
            region = (win.left, win.top, win.right, win.bottom)
            # call region screenshot function
            with mss.mss() as sct:
                monitor = {
                    "left": region[0],
                    "top": region[1],
                    "width": region[2] - region[0],
                    "height": region[3] - region[1]
                }
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                if save_path.lower().endswith((".jpg", ".jpeg")):
                    img.save(save_path, quality=quality)
                else:
                    img.save(save_path)
            return save_path

        # macOS specific implementation, need pyobjc-framework-Quartz
        elif system == "Darwin":
            from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
            import Quartz

            # get all windows info
            window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
            target_window = None
            for win in window_list:
                win_name = win.get('kCGWindowName', '') or ''
                if window_title.lower() in win_name.lower():
                    target_window = win
                    break
            if not target_window:
                return None

            # get window bounds
            bounds = target_window['kCGWindowBounds']
            x, y, w, h = bounds['X'], bounds['Y'], bounds['Width'], bounds['Height']
            # macOS coordinate system adjustment
            screen_height = Quartz.CGDisplayBounds(Quartz.CGMainDisplayID()).size.height
            y = screen_height - y - h

            # region screenshot
            with mss.mss() as sct:
                monitor = {"left": x, "top": y, "width": w, "height": h}
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                if save_path.lower().endswith((".jpg", ".jpeg")):
                    img.save(save_path, quality=quality)
                else:
                    img.save(save_path)
            return save_path

        # Linux specific implementation, need imagemagick and xwd installed
        elif system == "Linux":
            import subprocess
            # verbally get window id by title
            cmd = f"xwininfo -root -children | grep -i {window_title} | awk '{{print $1}}'"
            win_id = subprocess.check_output(cmd, shell=True).decode().strip()
            if not win_id:
                return None
            # get window and transfer to image
            subprocess.run(f"xwd -id {win_id} -out /tmp/temp.xwd", shell=True)
            img = Image.open("/tmp/temp.xwd")
            img.save(save_path, quality=quality if save_path.lower().endswith((".jpg", ".jpeg")) else None)
            os.remove("/tmp/temp.xwd")
            return save_path

    except Exception as e:
        print(f"screen capture fail：{e}")
        return None
    return None