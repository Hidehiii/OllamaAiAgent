from langchain.tools import tool
import getpass
import os

@tool
def bing_search_with_simple_result()