from langchain.tools import tool
from langchain_community.tools.file_management import (
    ReadFileTool, WriteFileTool, ListDirectoryTool,
    CopyFileTool, DeleteFileTool, FileSearchTool,
    MoveFileTool
)
import os

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