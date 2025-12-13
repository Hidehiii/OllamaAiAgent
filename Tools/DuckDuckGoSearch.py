from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults

@tool
def duck_duck_go_search_simple_result(query: str) -> str:
    """
    Perform a simple DuckDuckGo search and return the results.
    :param query: The search query.
    :return: The search results as a string.
    """
    search_tool = DuckDuckGoSearchRun()
    results = search_tool.invoke(query)
    return results

@tool
def duck_duck_go_search_detail_result(query: str) -> str:
    """
    Perform a detailed DuckDuckGo search and return the results.
    :param query: The search query.
    :return: The detailed search results as a string.
    """
    search_tool = DuckDuckGoSearchResults()
    results = search_tool.invoke(query)
    return results
